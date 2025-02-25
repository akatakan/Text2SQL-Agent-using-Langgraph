import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///salaries.db')

    LLM_MODEL = os.getenv('LLM_MODEL', 'llama3.1:latest')
    LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.1'))

    MAX_TABLES_TO_SELECT = int(os.getenv('MAX_TABLES_TO_SELECT', '5'))
    MAX_SQL_REFINEMENT_ATTEMPTS = int(os.getenv('MAX_SQL_REFINEMENT_ATTEMPTS', '3'))

    LANGCHAIN_TRACING_V2 = os.getenv('LANGCHAIN_TRACING_V2', 'false').lower() == 'true'
    LANGSMITH_API_KEY = os.getenv('LANGSMITH_API_KEY')  

    GRAPH_RECURSION_LIMIT = int(os.getenv('GRAPH_RECURSION_LIMIT', '20'))

    USE_OLLAMA = os.getenv('USE_OLLAMA', 'true').lower() == 'true'
    USE_OPENAI = os.getenv('USE_OPENAI', 'true').lower() == 'true'

    CHROMA_COLLECTION_NAME = os.getenv('CHROMA_COLLECTION_NAME', 'sql_agent_memory')
    CHROMA_PERSIST_DIRECTORY = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')