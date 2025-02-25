from langchain.prompts import ChatPromptTemplate
from src.core.models import AgentState, ValidationResult
from src.utils.utils import get_llm, json_util
from src.core.config import Config
import json
import logging

logger = logging.getLogger(__name__)

def sql_validator(state: AgentState):
    logger.info("Entering SQL validator")
    
    llm = get_llm(Config.LLM_MODEL)

    prompt = ChatPromptTemplate.from_template("""
    Given the following:
    1. Original user query: {original_query}
    2. Generated SQL query: {sql_query}
    3. Database schema:
    {table_schemas}

    ### TASK ###
    Your task is to validate the given SQL query for correctness, security, and relevance.

    #### CHECK FOR:
    - SQL syntax errors
    - SQL injection vulnerabilities
    - Non-existent tables or columns
    - Logical errors in JOIN conditions or WHERE clauses
    - Incorrect use of GROUP BY and aggregation functions
    - Relevance of the query to the user question
    - Performance issues (e.g., missing indexes, inefficient JOINs)
    - Avoid selecting entire tables without limits.

    ### RESPONSE FORMAT ###
    **Your response MUST be in valid JSON format.**
    Do not include any explanations, markdown, or additional text.  
    If the query is valid, return:  
    
    {{
        "is_sql_valid": true/false,
        "issues": ["Issue 1", "Issue 2"],
        "suggested_fix": ""
    }}
    """)

    sql_query = state["generated_sql"]

    chain = prompt | llm
    try:
        response = chain.invoke({
            "original_query": state["user_query"],
            "sql_query": sql_query,
            "table_schemas": json.dumps(state["db_info"], indent=2)
        })
        
        try:
            result = json_util(response.content)
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON response: {response.content}")

        state['validation_result'] = ValidationResult(
            is_sql_valid=result.get('is_sql_valid', False),
            issues=result.get('issues', []),
            suggested_fix=result.get('suggested_fix', '')
        )

    except Exception as e:
        logger.error(f"Error in SQL validation: {e}")
        state['validation_result'] = ValidationResult(
            is_sql_valid=False,
            issues=["Unexpected error in validation process"],
            suggested_fix="Please review the SQL query and try again."
        )
    logger.info(f"SQL validation result: {state['validation_result'].is_sql_valid}")
    return state
