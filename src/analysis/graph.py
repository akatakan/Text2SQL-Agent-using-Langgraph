from src.core.models import AgentState
from langgraph.graph import StateGraph, END
from src.database.db_service import DatabaseService
from src.analysis.reasoning import create_reasoning_steps
from src.sql.generator import create_sql_query
from src.sql.validator import sql_validator
from src.sql.evaluator import evaluate_sql
from src.sql.correction import sql_correction
from src.analysis.summarizer import summarize
import logging

logger = logging.getLogger(__name__)

def should_execute_correction(state: AgentState) -> str:
    if not state["evaluation_result"].is_result_relevant and state["correct_attempts"] < 3:
        return "sql_correction" 
    else:
        return "summarize"

def should_sumarize(state: AgentState) -> str:
    if state["execution_result"].error and state["correct_attempts"] < 3:
        return "sql_correction"
    else:
        return "summarize"


def should_regenerate_sql(state: AgentState) -> str:
    if state["validation_result"].is_sql_valid:
        return "execute_sql"
    elif state["attempts"] < 3:
        return "sql_generation"
    else:
        return "summarize"
        

def create_graph() -> AgentState:
    logger.info("Creating graph")
    graph = StateGraph(AgentState)

    #Nodes
    graph.add_node("db_information",DatabaseService.get_database_info)
    graph.add_node("reasoning",create_reasoning_steps)
    graph.add_node("sql_generation",create_sql_query)
    graph.add_node("sql_validator",sql_validator)
    graph.add_node("execute_sql",DatabaseService.execute_sql)
    graph.add_node("result_evaluation",evaluate_sql)
    graph.add_node("sql_correction",sql_correction)
    graph.add_node("execute_sql_correction",DatabaseService.execute_sql_correction)
    graph.add_node("summarize",summarize)

    #Edges
    graph.set_entry_point("db_information")
    graph.add_conditional_edges(
        "db_information",
        lambda state: "reasoning" if state["db_info"] else "summarize",
        {
            "reasoning": "reasoning",
            "summarize": "summarize"
        }
    )
    graph.add_edge("reasoning", "sql_generation")
    graph.add_edge("sql_generation","sql_validator")
    graph.add_conditional_edges(
        "sql_validator",
        should_regenerate_sql,
        {
            "execute_sql": "execute_sql",
            "sql_regeneration": "sql_generation",
            "summarize": "summarize"
        }
    )
    graph.add_edge("execute_sql","result_evaluation")
    graph.add_conditional_edges(
        "result_evaluation",
        should_execute_correction,
        {
            "sql_correction": "sql_correction",
            "summarize": "summarize"
        }
    )
    graph.add_edge("sql_correction","execute_sql_correction")
    graph.add_conditional_edges(
        "execute_sql_correction",
        should_sumarize,
        {
            "sql_correction": "sql_correction",
            "summarize": "summarize"
        }
    )
    graph.add_edge("summarize",END)

    compiled_graph = graph.compile()
    return compiled_graph

def draw_graph(graph: StateGraph):  
    from langchain_core.runnables.graph import MermaidDrawMethod
    img = graph.get_graph().draw_mermaid_png(
            draw_method=MermaidDrawMethod.API,
        )
    with open("graph.png", "wb") as f:
        f.write(img)


