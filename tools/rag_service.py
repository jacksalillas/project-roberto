
import os
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import Settings
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

class RAGService:
    def __init__(self, persist_dir="./chroma_db"):
        self.persist_dir = persist_dir
        self.llm = Ollama(model="mistral", request_timeout=300.0)
        self.embed_model = OllamaEmbedding(model_name="mistral")
        
        Settings.llm = self.llm
        Settings.embed_model = self.embed_model

        db = chromadb.PersistentClient(path=self.persist_dir)
        chroma_collection = db.get_or_create_collection("roberto_vault")
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        self.index = None

    def load_and_index_documents(self, documents_path):
        if not os.path.exists(documents_path):
            raise FileNotFoundError(f"Documents path does not exist: {documents_path}")

        print(f"Loading documents from: {documents_path}")
        reader = SimpleDirectoryReader(input_dir=documents_path, recursive=True)
        documents = reader.load_data()
        
        if documents:
            print(f"Loaded {len(documents)} documents. Starting indexing...")
            self.index = VectorStoreIndex.from_documents(
                documents, storage_context=self.storage_context
            )
            print(f"Successfully indexed {len(documents)} documents from {documents_path}")
        else:
            print(f"No documents found in {documents_path}")

    def get_query_engine(self, filters=None):
        if self.index:
            return self.index.as_query_engine(filters=filters)
        else:
            # Load index from storage if it exists
            try:
                self.index = VectorStoreIndex.from_vector_store(
                    vector_store=self.storage_context.vector_store
                )
                return self.index.as_query_engine(filters=filters)
            except Exception as e:
                print(f"Could not load index from storage: {e}")
                return None

