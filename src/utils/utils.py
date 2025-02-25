from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from src.core.config import Config
import json

def get_llm(model_name):
    temperature = Config.LLM_TEMPERATURE
    if Config.USE_OPENAI:
        return ChatOpenAI(model=model_name,temperature=temperature)
    elif Config.USE_OLLAMA:
        return ChatOllama(model=model_name,temperature=temperature)
    else:
        raise ValueError(f"Unsupported provider")


def json_util(text)->dict:
    return json.loads(text)

