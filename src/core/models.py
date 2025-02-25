from typing import Any, List, TypedDict, Dict, Optional
from pydantic import BaseModel, Field


class ExecutionResult(BaseModel):
    success: bool
    data: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None

class ValidationResult(BaseModel):
    is_sql_valid: bool = Field(description="Whether the SQL query is valid and safe to execute")
    issues: List[str] = Field(default_factory=list, description="List of identified issues with the SQL query")
    suggested_fix: str = Field(default="", description="Suggested fix for the SQL query if issues are found")

class EvaluationResult(BaseModel):
    is_result_relevant: bool = Field(description="Whether the generated SQL query is relevant to the user query")
    explanation: str = Field(default="", description="Explanation of why the SQL query is or is not relevant")
    improvement_suggestion: str = Field(default="", description="Suggestion on how to improve the SQL query for relevance")

class SQLCorrectionResult(BaseModel):
    analysis: str = Field(default="No analysis provided", description="Analysis of why the current SQL query is not producing relevant results")
    identified_issues: List[str] = Field(default="No issues identified", description="List of specific issues identified in the current SQL query")
    corrected_sql_query: str = Field(default="", description="A corrected SQL query that addresses the identified issues")



class AgentState(TypedDict):
    user_query: str
    sql_reasoning: Optional[str]
    db_info: Optional[Dict]
    generated_sql: Optional[str]
    validation_result: Optional[ValidationResult]
    execution_result: Optional[ExecutionResult]
    evaluation_result: Optional[EvaluationResult]
    correction_result: Optional[SQLCorrectionResult]
    report_summary: Optional[str]
    attempts: int = 0
    correct_attempts: int = 0
    
