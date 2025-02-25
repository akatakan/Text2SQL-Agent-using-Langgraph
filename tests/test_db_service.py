import pytest
from src.database.db_service import DatabaseService
from src.core.models import ExecutionResult, AgentState

def test_get_database_info(sample_state, db_engine):
    """Veritabanı şema bilgisinin doğru şekilde alındığını test eder."""
    state = DatabaseService.get_database_info(sample_state)
    
    assert "db_info" in state
    assert isinstance(state["db_info"], dict)
    assert len(state["db_info"]) > 0
    
    # En az bir tablo olmalı
    for table_name, table_info in state["db_info"].items():
        assert "columns" in table_info
        assert "foreign_keys" in table_info
        assert isinstance(table_info["columns"], dict)
        assert isinstance(table_info["foreign_keys"], list)

def test_execute_sql_success(sample_state, sample_sql_query):
    """SQL sorgusu başarılı şekilde çalıştığında doğru sonuç döndüğünü test eder."""
    state = sample_state
    state["generated_sql"] = sample_sql_query
    
    result_state = DatabaseService.execute_sql(state)
    
    assert "execution_result" in result_state
    assert isinstance(result_state["execution_result"], ExecutionResult)
    assert result_state["execution_result"].success
    assert isinstance(result_state["execution_result"].data, list)

def test_execute_sql_failure(sample_state):
    """Hatalı SQL sorgusu durumunda doğru hata döndüğünü test eder."""
    state = sample_state
    state["generated_sql"] = "SELECT * FROM nonexistent_table"
    
    result_state = DatabaseService.execute_sql(state)
    
    assert "execution_result" in result_state
    assert isinstance(result_state["execution_result"], ExecutionResult)
    assert not result_state["execution_result"].success
    assert result_state["execution_result"].error is not None

def test_execute_sql_correction(sample_state, sample_sql_query):
    """SQL düzeltme sorgusunun doğru çalıştığını test eder."""
    state = sample_state
    state["correction_result"] = type('obj', (object,), {
        'corrected_sql_query': sample_sql_query
    })
    
    result_state = DatabaseService.execute_sql_correction(state)
    
    assert "execution_result" in result_state
    assert isinstance(result_state["execution_result"], ExecutionResult)
    assert result_state["execution_result"].success
    assert isinstance(result_state["execution_result"].data, list) 