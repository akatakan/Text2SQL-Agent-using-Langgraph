from src.core.config import Config
from langchain.prompts import ChatPromptTemplate
from src.core.models import AgentState
from src.utils.utils import get_llm, json_util
import logging

logger = logging.getLogger(__name__)


def summarize(state: AgentState):
    logger.info("Summarizer Started")

    llm = get_llm(Config.LLM_MODEL)

    prompt = ChatPromptTemplate.from_template("""
    Given the following information:
        1. Data Result: {data_result}

        Task: Write a report based on given data result. Summarize the key insights, trends, or patterns in the data.
        Explain lean, clear, and concise manner to help the user understand the data better.

        Respond only the following JSON format:
        {{
            "summary": "Your summary of the evaluation result and relevance of the SQL query"
        }}
    """)

    chain = prompt | llm

    try:
        response = chain.invoke({
            "data_result": state["execution_result"].data
        })

        logger.info(f"Summarizer Raw Response: {response.content}")
        result = json_util(response.content)

        state["report_summary"] = result['summary']

    except Exception as e:
        logger.error(f"Error in Summarizer: {e}")
        state["report_summary"] = "No summary provided"

    return state
