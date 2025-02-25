from langchain.prompts import ChatPromptTemplate
from src.utils.utils import get_llm
from src.core.config import Config
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def create_reasoning_steps(state):
    logger.info("Creating reasoning steps")
    logger.info(f"User query: {state['user_query']}")

    llm = get_llm(Config.LLM_MODEL)

    prompt = ChatPromptTemplate.from_template("""
        You are a helpful data analyst who is great at thinking deeply and reasoning about the user's question and the database schema, and you provide a step-by-step reasoning plan in order to answer the user's question.
                                              
        1. Think deeply and reason about the user's question and the database schema.
        2. Give a step by step reasoning plan in order to answer user's question.
        3. The reasoning plan should be in the language same as the language user provided in the input.
        4. Make sure to consider the current time provided in the input if the user's question is related to the date/time.
        5. Don't include SQL in the reasoning plan.
        6. Each step in the reasoning plan must start with a number, and a reasoning for the step.
        7. If SQL SAMPLES are provided, make sure to consider them in the reasoning plan.
        8. Do not include ```markdown or ``` in the answer.

        The final answer must be a reasoning plan in plain Markdown string format.

        Database Schema:
        {db_schema}
          
        User's Question: {user_query}

        Let's think step by step.
        """
    )

    chain = prompt | llm

    try:
        response = chain.invoke({
            "db_schema": state["db_info"],
            "user_query": state["user_query"],
        })

        logger.info(f"Raw LLM response: {response.content}")

        state["sql_reasoning"] = response.content
    
    except Exception as e:
        logger.error(f"Error in reasoning: {e}")
        state["sql_reasoning"] = None
    
    return state