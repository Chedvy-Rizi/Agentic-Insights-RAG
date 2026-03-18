import os
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.llms.cohere import Cohere
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.core import VectorStoreIndex, StorageContext, Settings, PromptTemplate, get_response_synthesizer
from llama_index.vector_stores.pinecone import PineconeVectorStore


load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


Settings.llm = Cohere(
    api_key=COHERE_API_KEY, 
    model="command-r-08-2024",
    temperature=0.1,
    max_tokens=8000
)

Settings.embed_model = CohereEmbedding(
    api_key=COHERE_API_KEY,
    model_name="embed-multilingual-v3.0",
)


pc = Pinecone(api_key=PINECONE_API_KEY, ssl_verify=False)
pinecone_index = pc.Index("rag-lesson")
vector_store = PineconeVectorStore(pinecone_index=pinecone_index, namespace="")
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)


qa_prompt_tmpl_str = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "You are a professional technical assistant. Based ONLY on the context provided above (and not your general knowledge), "
    "answer the following query. \n"
    "CRITICAL RULES:\n"
    "1. If the answer is not in the context, say: 'מצטער, המידע הזה לא מופיע בתיעוד הפרויקט'.\n"
    "2. Always respond in the SAME LANGUAGE as the user's question.\n"
    "3. If there are contradictions between tools, highlight them.\n"
    "Query: {query_str}\n"
    "Answer: "
)
qa_prompt_tmpl = PromptTemplate(qa_prompt_tmpl_str)

response_synthesizer = get_response_synthesizer(
    response_mode="tree_summarize",
    text_qa_template=qa_prompt_tmpl
)