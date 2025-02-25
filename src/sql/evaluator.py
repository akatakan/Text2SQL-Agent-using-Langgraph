import json
from src.core.config import Config
from langchain.prompts import ChatPromptTemplate
from src.core.models import AgentState, EvaluationResult
import pandas as pd
import logging

from src.utils.utils import get_llm, json_util

logger = logging.getLogger(__name__)



def evaluate_sql(state: AgentState) -> str:
    logger.info("Entering result evaluator")

    if not state["execution_result"].success:
        state["evaluation_result"] = EvaluationResult(
            is_result_relevant=False,
            explanation=f"Query execution failed: {state['execution_result'].error}",
        )
        state["is_result_relevant"] = False
        return state
    
    llm = get_llm(Config.LLM_MODEL)
    df = pd.DataFrame(state["execution_result"].data)

    results = df.describe().to_string() if not df.empty else "No results"

    prompt = ChatPromptTemplate.from_template("""
        Given the following:
        1. Original user query: {original_query}
        2. Generated SQL query: {generated_sql}
        3. Query results:
        {results}
                                              
        Task 1: Evaluate the relevance and quality of the query results to the original user query.
        Task 2: If not relevant, provide explanation and suggestions on how to improve the SQL query to better answer the original user query.

        Respond in the following JSON format:
        {{
            "is_result_relevant": true/false,
            "explanation": "Detailed explanation of your evaluation",
            "improvement_suggestion": "Suggestion on how to improve the SQL query if not relevant",
        }}
    """)

    chain = prompt | llm

    try:
        response = chain.invoke({
            "original_query": state["user_query"],
            "generated_sql": state["generated_sql"],
            "results": results,
        })
        logger.info(f"Raw LLM type: {type(response.content)}")
        logger.info(f"Raw LLM response: {response.content}")

        result = json.loads(response.content)
        
    
        state["evaluation_result"] = EvaluationResult(
                is_result_relevant=result.get('is_result_relevant', False),
                explanation=result.get('explanation', "Failed to generate explanation"),
                improvement_suggestion=result.get('improvement_suggestion', ""),
        )
    
    except Exception as e:
        logger.error(f"Error evaluating SQL results: {e}")
        state["evaluation_result"] = EvaluationResult(
            is_result_relevant=False,
            explanation=f"Error evaluating SQL results: {e}",
        )

    logger.info(f"Result relevance: {state['evaluation_result'].is_result_relevant}")

    return state
