from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from src.core.config import Config
import logging

logger = logging.getLogger(__name__)

class VectorDB:
    def __init__(self):
        self.embedding_function = self._create_embed_func()
        self.vector_db = self._create_vector_db()
        self.memory_buffer = []
        self.memory_buffer_size = 10

    def _create_embed_func(self):
        if Config.USE_OLLAMA:
            logger.info("Using Ollama embeddings")
            return OllamaEmbeddings(
                base_url=Config.OLLAMA_BASE_URL,
                model_name=Config.LLM_MODEL,
            )
        elif Config.USE_OPENAI:
            logger.info("Using OpenAI embeddings")
            return OpenAIEmbeddings()
        else:
            logger.error("No valid embedding function found")
            raise ValueError("No valid embedding function found")
        
    def _create_vector_db(self):
        logger.info("Creating Chroma vector DB")
        return Chroma(
                collection_name=Config.CHROMA_COLLECTION_NAME,
                persist_directory=Config.CHROMA_PERSIST_DIRECTORY,
                embeddings=self.embedding_function,
        )
        
    def add_to_memory(self, text,metadata=None):
        try:
            self.vector_db.add_texts([text],metadata = [metadata] if metadata else None)
            logger.info(f"Added text to memory. Text: {text[:50]}...")
        except Exception as e:
            logger.error(f"Failed to add memory: {str(e)}")
            raise   

    def search_memory(self, query, k=5):
        if not self.vector_db:
            logger.error("Vector DB not initialized")
            return []
        try:
            results = self.vector_db.similarity_search(query, k=k)
            logger.info(f"Found {len(results)} results in memory for query: {query[:50]}...")
            return results
        except Exception as e:
            logger.error(f"Failed to search memory: {str(e)}")
            raise

    def clear_memory(self):
        try:
            self.vector_db.delete_collection()
            self.vector_db = self._create_vector_db()
            logger.info("Memory cleared")
        except Exception as e:
            logger.error(f"Failed to clear memory: {str(e)}")
            raise