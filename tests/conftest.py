import pytest
from src.core.models import AgentState
from sqlalchemy import create_engine, text
from src.core.config import Config
import pandas as pd

@pytest.fixture
def sample_state():
    """Test için örnek bir AgentState nesnesi döndürür."""
    return AgentState(
        user_query="Show me the total number of employees for each level"
    )

@pytest.fixture
def db_engine():
    """Test için veritabanı bağlantısı oluşturur."""
    engine = create_engine(Config.DATABASE_URL)
    return engine

@pytest.fixture
def sample_db_info():
    """Test için örnek veritabanı şema bilgisi döndürür."""
    return {
        "employees": {
            "columns": {
                "id": "INTEGER",
                "name": "VARCHAR",
                "level": "VARCHAR",
                "salary": "INTEGER"
            },
            "foreign_keys": []
        }
    }

@pytest.fixture
def sample_sql_query():
    """Test için örnek bir SQL sorgusu döndürür."""
    return "SELECT level, COUNT(*) as total_employees FROM employees GROUP BY level"

@pytest.fixture
def sample_execution_result():
    """Test için örnek bir sorgu sonucu döndürür."""
    data = [
        {"level": "Junior", "total_employees": 10},
        {"level": "Senior", "total_employees": 5}
    ]
    return {"success": True, "data": data, "error": None} 