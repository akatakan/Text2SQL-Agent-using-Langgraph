import pytest
from src.core.models import AgentState
from src.analysis.graph import create_graph

def test_full_workflow():
    """Tüm iş akışını baştan sona test eder."""
    # Başlangıç durumu
    initial_state = AgentState(
        user_query="Show me the total number of employees for each level"
    )
    
    # Graf oluştur
    graph = create_graph()
    
    # İş akışını çalıştır
    final_state = graph.invoke(initial_state)
    
    # Sonuçları kontrol et
    assert "db_info" in final_state
    assert "sql_reasoning" in final_state
    assert "generated_sql" in final_state
    assert "validation_result" in final_state
    assert "execution_result" in final_state
    assert "summarizer_result" in final_state

def test_error_workflow():
    """Hata durumunda iş akışını test eder."""
    # Hatalı sorgu ile başlangıç durumu
    initial_state = AgentState(
        user_query="Show me something that doesn't exist in the database"
    )
    
    # Graf oluştur
    graph = create_graph()
    
    # İş akışını çalıştır
    final_state = graph.invoke(initial_state)
    
    # Hata durumunda bile tüm adımların çalıştığını kontrol et
    assert "db_info" in final_state
    assert "sql_reasoning" in final_state
    assert "generated_sql" in final_state
    assert "validation_result" in final_state
    
    # Hata durumunda düzeltme mekanizmasının devreye girdiğini kontrol et
    if not final_state["validation_result"].is_sql_valid:
        assert "correction_result" in final_state

def test_complex_query_workflow():
    """Karmaşık sorgular için iş akışını test eder."""
    # Karmaşık bir sorgu ile başlangıç durumu
    initial_state = AgentState(
        user_query="Show me the average salary for each level, but only include levels with more than 5 employees"
    )
    
    # Graf oluştur
    graph = create_graph()
    
    # İş akışını çalıştır
    final_state = graph.invoke(initial_state)
    
    # Karmaşık sorgu sonuçlarını kontrol et
    assert "db_info" in final_state
    assert "sql_reasoning" in final_state
    assert "generated_sql" in final_state
    assert "validation_result" in final_state
    assert "execution_result" in final_state
    assert "summarizer_result" in final_state
    
    # SQL sorgusunun karmaşık yapıları içerdiğini kontrol et
    assert "GROUP BY" in final_state["generated_sql"].upper()
    assert "HAVING" in final_state["generated_sql"].upper()
    assert "COUNT" in final_state["generated_sql"].upper() 