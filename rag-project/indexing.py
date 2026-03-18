import os
from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import SimpleDirectoryReader, StorageContext, VectorStoreIndex, Settings
from llama_index.core.node_parser import TokenTextSplitter 
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.embeddings.cohere import CohereEmbedding
from llama_index.llms.cohere import Cohere

load_dotenv()

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
pinecone_index = pc.Index("rag-lesson")

Settings.embed_model = CohereEmbedding(
    api_key=os.getenv("COHERE_API_KEY"), 
    model_name="embed-multilingual-v3.0"
)
Settings.llm = Cohere(
    api_key=os.getenv("COHERE_API_KEY"), 
    model="command-r-plus"
)

def run_ingestion():
    data_path = "C:/Users/user1/Desktop/תכנותתת/שנה ב/AI/RAG/data-project"
    
    def file_metadata_func(file_path):
        tool_name = "General"
        if ".claude" in file_path: tool_name = "Claude"
        elif ".copilot" in file_path: tool_name = "Copilot"
        elif ".windsurf" in file_path: tool_name = "Windsurf"
        
        return {
            "file_path": file_path,
            "file_name": os.path.basename(file_path),
            "agent_tool": tool_name, 
            "project_part": "Documentation"
        }

    reader = SimpleDirectoryReader(
        input_dir=data_path, 
        recursive=True, 
        exclude_hidden=False, 
        file_metadata=file_metadata_func
    )

    documents = reader.load_data()

    node_parser = TokenTextSplitter(chunk_size=512, chunk_overlap=50)
    nodes = node_parser.get_nodes_from_documents(documents)

    
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    index = VectorStoreIndex(
        nodes, 
        storage_context=storage_context,
        show_progress=True
    )
    
if __name__ == "__main__":
    run_ingestion()