from langchain.prompts import ChatPromptTemplate
from src.core.models import AgentState, SQLCorrectionResult
from src.utils.utils import get_llm, json_util
from src.core.config import Config
import logging

logger = logging.getLogger(__name__)


def sql_correction(state: AgentState):

    logger.info("SQL Correction Started")

    llm = get_llm(Config.LLM_MODEL)

    prompt = ChatPromptTemplate.from_template("""
        **Task:**  
        Analyze why the given SQL query does not produce the correct results, identify the issues, and provide a corrected SQL query that properly answers the user's request.  

        **Provided Information:**  
        - **User Query:** `{original_query}` (The original request made by the user.)  
        - **Reasoning:** `{reasoning}` (The logic behind the construction of the current SQL query.)  
        - **Current SQL Query:**  
        {current_sql}
        - **Error:**
        {error}
        - **Improvement Suggestion:** {improvement_suggestion}
        - **Evaluation Result:** `{evaluation_result}` (Assessment of why the query is incorrect or ineffective.)  
        - **Database Schema (Tables and Columns):**  
        {db_schema}

        **What You Need to Do:**  
        1. **Analyze:** Explain why the current SQL query fails to produce the correct results.  
        2. **Identify Issues:** List specific problems in the query (e.g., incorrect joins, missing filters, wrong conditions).  
        3. **Provide a Corrected SQL Query:** Write a revised query that returns the correct results.  
                                              
        IMPORTANT:
        - Ensure the corrected SQL query conforms to the database schema.

        **Response Format (Strictly JSON, No Additional Explanations):**  
        {{
            "analysis": "Explanation of why the current SQL query is incorrect.",
            "identified_issues": [
                "Issue 1: Explanation",
                "Issue 2: Explanation"
            ],
            "corrected_sql_query": "The corrected SQL query should be placed here."
        }}

        **Note:** Your response must be in the exact JSON format shown above. Do not include any extra explanations or formatting.
    """)

    chain = prompt | llm

    try:
        response = chain.invoke({
            "original_query": state["user_query"],
            "reasoning": state["sql_reasoning"],
            "current_sql": state["generated_sql"],
            "evaluation_result": state["evaluation_result"].explanation,
            "error": state["execution_result"].error if state["execution_result"] else "", 
            "db_schema": state["db_info"],
            "improvement_suggestion": state["evaluation_result"].improvement_suggestion if state["evaluation_result"].improvement_suggestion else "No improvement suggestion provided"
        })
        logger.info(f"Database Schema: {state['db_info']}")
        logger.info(f"SQL Correction Raw Response: {response.content}")
        result = json_util(response.content)

        logger.info(f"SQL Correction Attempt: {state["correct_attempts"]}")
        state["correct_attempts"] += 1
        
        state["correction_result"] = SQLCorrectionResult(
            analysis=result.get("analysis", "No analysis provided"),
            identified_issues=result.get("identified_issues", "No issues identified"),
            corrected_sql_query=result.get("corrected_sql_query", state["generated_sql"] if state["generated_sql"] else "")
        )


    except Exception as e:
        logger.error(f"Error in SQL Correction: {e}")
        state["correction_result"] = {
            "error": f"An error occurred while generating SQL correction: {e}",
            "corrected_sql_query": state["generated_sql"] if state["generated_sql"] else ""
        }
    return state
    