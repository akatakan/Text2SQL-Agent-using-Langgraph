import pytest
from src.sql.generator import create_sql_query
from src.sql.validator import sql_validator
from src.sql.evaluator import evaluate_sql
from src.sql.correction import sql_correction
from src.core.models import ValidationResult, EvaluationResult, SQLCorrectionResult

def test_sql_generator(sample_state, sample_db_info):
    """SQL sorgusu oluşturma işlemini test eder."""
    state = sample_state
    state["db_info"] = sample_db_info
    state["sql_reasoning"] = "1. Çalışan seviyelerini grupla\n2. Her seviye için toplam çalışan sayısını hesapla"
    
    result_state = create_sql_query(state)
    
    assert "generated_sql" in result_state
    assert isinstance(result_state["generated_sql"], str)
    assert "SELECT" in result_state["generated_sql"].upper()
    assert "FROM" in result_state["generated_sql"].upper()

def test_sql_validator(sample_state, sample_sql_query):
    """SQL doğrulama işlemini test eder."""
    state = sample_state
    state["generated_sql"] = sample_sql_query
    state["db_info"] = {"employees": {"columns": {"level": "VARCHAR"}}}
    
    result_state = sql_validator(state)
    
    assert "validation_result" in result_state
    assert isinstance(result_state["validation_result"], ValidationResult)
    assert hasattr(result_state["validation_result"], "is_sql_valid")
    assert hasattr(result_state["validation_result"], "issues")

def test_sql_evaluator(sample_state, sample_sql_query, sample_execution_result):
    """SQL değerlendirme işlemini test eder."""
    state = sample_state
    state["generated_sql"] = sample_sql_query
    state["execution_result"] = type('obj', (object,), sample_execution_result)
    
    result_state = evaluate_sql(state)
    
    assert "evaluation_result" in result_state
    assert isinstance(result_state["evaluation_result"], EvaluationResult)
    assert hasattr(result_state["evaluation_result"], "is_result_relevant")
    assert hasattr(result_state["evaluation_result"], "explanation")

def test_sql_correction(sample_state, sample_sql_query):
    """SQL düzeltme işlemini test eder."""
    state = sample_state
    state["generated_sql"] = sample_sql_query
    state["sql_reasoning"] = "Çalışan seviyelerine göre gruplama"
    state["evaluation_result"] = EvaluationResult(
        is_result_relevant=False,
        explanation="Sonuçlar yetersiz",
        improvement_suggestion="Gruplama ekle"
    )
    state["db_info"] = {"employees": {"columns": {"level": "VARCHAR"}}}
    
    result_state = sql_correction(state)
    
    assert "correction_result" in result_state
    assert isinstance(result_state["correction_result"], SQLCorrectionResult)
    assert hasattr(result_state["correction_result"], "analysis")
    assert hasattr(result_state["correction_result"], "identified_issues")
    assert hasattr(result_state["correction_result"], "corrected_sql_query") 