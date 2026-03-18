import asyncio
import re
import json
from llama_index.core.schema import NodeWithScore
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core import Settings
from llama_index.core.workflow import Workflow, step, StartEvent, StopEvent, Event
from llama_index.utils.workflow import draw_all_possible_flows
from pathlib import Path

from config import index, response_synthesizer

class InputVerifiedEvent(Event):
    query: str

class SemanticQueryEvent(Event): 
    query: str

class StructuredQueryEvent(Event): 
    query: str

class ContextRetrievedEvent(Event):
    query: str
    nodes: list[NodeWithScore]

class RAGWorkflow(Workflow):

    @step
    async def security_and_validation(self, ev: StartEvent) -> InputVerifiedEvent | StopEvent:
        query = ev.get("query", "").strip()
        if len(query) < 2:
            return StopEvent(result="השאילתה קצרה מדי.")
        
        clean_query = re.sub(r'<[^>]*?>', '', query)
        malicious_patterns = ["ignore previous instructions", "system prompt", "as an admin", "bypass"]
        
        if any(pattern in clean_query.lower() for pattern in malicious_patterns):
            return StopEvent(result="מצטער, השאילתה שלך מכילה פקודות לא מורשות.")

        return InputVerifiedEvent(query=clean_query)

    @step
    async def route_query(self, ev: InputVerifiedEvent) -> SemanticQueryEvent | StructuredQueryEvent:
        print(f"🚦 מנתב שאילתה: {ev.query}")
        
        router_prompt = (
            "You are a routing assistant. Decide if the user query is asking for a LIST of items, "
            "specific architectural DECISIONS, coding RULES, or WARNINGS (reply 'STRUCTURED').\n"
            "If it's a general question about how things work or a specific technical 'how-to', reply 'SEMANTIC'.\n"
            "Reply with ONLY one word: STRUCTURED or SEMANTIC.\n"
            f"Query: {ev.query}"
        )
        
        from llama_index.core.llms import ChatMessage
        response = Settings.llm.chat([ChatMessage(role="user", content=router_prompt)])
        decision = str(response).strip().upper()
        
        if "STRUCTURED" in decision:
            print("➡️ נתיב נבחר: נתונים מובנים (JSON)")
            return StructuredQueryEvent(query=ev.query)
        else:
            print("➡️ נתיב נבחר: חיפוש סמנטי (Vector DB)")
            return SemanticQueryEvent(query=ev.query)

    @step
    async def handle_structured_data(self, ev: StructuredQueryEvent) -> StopEvent:
        try:
            with open("structured_data.json", "r", encoding="utf-8") as f:
                full_data = json.load(f)
            
            items_context = json.dumps(full_data.get("items", {}), ensure_ascii=False, indent=2)
            
            final_prompt = (
                "You are a technical expert. Use the following structured data to answer the query.\n"
                "If the information is not in the data, say you don't know.\n"
                f"Data:\n{items_context}\n\n"
                f"User Query: {ev.query}\n"
                "Answer clearly in the user's language:"
            )
            
            from llama_index.core.llms import ChatMessage
            response = Settings.llm.chat([ChatMessage(role="user", content=final_prompt)])
            return StopEvent(result=str(response))
        except Exception as e:
            return StopEvent(result=f"שגיאה בקריאת הנתונים המובנים: {str(e)}")


    @step
    async def retrieve_semantic(self, ev: SemanticQueryEvent) -> ContextRetrievedEvent:
        retriever = VectorIndexRetriever(index=index, similarity_top_k=3)
        nodes = retriever.retrieve(ev.query)
        return ContextRetrievedEvent(query=ev.query, nodes=nodes)

    @step
    async def generate_semantic_output(self, ev: ContextRetrievedEvent) -> StopEvent:
        response_obj = response_synthesizer.synthesize(query=ev.query, nodes=ev.nodes)
        return StopEvent(result=str(response_obj))

rag_engine = RAGWorkflow(timeout=60)

async def generate_visual_flow():
    draw_all_possible_flows(
        rag_engine, 
        filename=str(Path("workflow_visualization.html").resolve())
    )

if __name__ == "__main__":
    asyncio.run(generate_visual_flow())