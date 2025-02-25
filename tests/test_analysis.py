import pytest
from src.analysis.reasoning import create_reasoning_steps
from src.analysis.summarizer import summarize
from src.analysis.graph import create_graph, should_execute_correction, should_sumarize, should_regenerate_sql
from src.core.models import AgentState, ExecutionResult, ValidationResult, EvaluationResult

def test_reasoning_steps(sample_state, sample_db_info):
    """Mantıksal adımların oluşturulmasını test eder."""
    state = sample_state
    state["db_info"] = sample_db_info
    
    result_state = create_reasoning_steps(state)
    
    assert "sql_reasoning" in result_state
    assert isinstance(result_state["sql_reasoning"], str)
    assert len(result_state["sql_reasoning"]) > 0

def test_summarizer(sample_state, sample_execution_result):
    """Özet oluşturma işlemini test eder."""
    state = sample_state
    state["execution_result"] = type('obj', (object,), sample_execution_result)
    
    result_state = summarize(state)
    
    assert "summarizer_result" in result_state
    assert isinstance(result_state["summarizer_result"], str)
    assert len(result_state["summarizer_result"]) > 0

def test_graph_creation():
    """Graf oluşturma işlemini test eder."""
    graph = create_graph()
    
    assert graph is not None
    assert hasattr(graph, "invoke")

def test_should_execute_correction():
    """Düzeltme yapılıp yapılmayacağını kontrol eden fonksiyonu test eder."""
    state = AgentState(user_query="test")
    state["evaluation_result"] = EvaluationResult(
        is_result_relevant=True,
        explanation="Good results"
    )
    
    result = should_execute_correction(state)
    assert result == "summarize"
    
    state["evaluation_result"].is_result_relevant = False
    result = should_execute_correction(state)
    assert result == "sql_correction"

def test_should_summarize():
    """Özetleme yapılıp yapılmayacağını kontrol eden fonksiyonu test eder."""
    state = AgentState(user_query="test")
    state["execution_result"] = ExecutionResult(
        success=True,
        data=[],
        error=None
    )
    
    result = should_sumarize(state)
    assert result == "summarize"
    
    state["execution_result"].error = "Some error"
    result = should_sumarize(state)
    assert result == "sql_correction"

def test_should_regenerate_sql():
    """SQL'in yeniden oluşturulup oluşturulmayacağını kontrol eden fonksiyonu test eder."""
    state = AgentState(user_query="test")
    state["validation_result"] = ValidationResult(
        is_sql_valid=True,
        issues=[],
        suggested_fix=""
    )
    
    result = should_regenerate_sql(state)
    assert result == "execute_sql"
    
    state["validation_result"].is_sql_valid = False
    result = should_regenerate_sql(state)
    assert result == "sql_regeneration" 