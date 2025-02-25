from sqlalchemy import create_engine, inspect, text
from src.core.config import Config
import pandas as pd
import logging

from src.core.models import ExecutionResult

logger = logging.getLogger(__name__)

class DatabaseService:
    @staticmethod
    def get_database_info(state):
        logger.info("Getting database information")
        try:
            engine = create_engine(Config.DATABASE_URL)
            logger.info(f"Connected to database: {engine.url}")
            inspector = inspect(engine)
            table_info = {}

            for table_name in inspector.get_table_names():
                columns = {col['name']: str(col['type']) for col in inspector.get_columns(table_name)}
                foreign_keys = [
                    f"{fk['constrained_columns'][0]} -> {fk['referred_table']}.{fk['referred_columns'][0]}"
                    for fk in inspector.get_foreign_keys(table_name)
                ]

                table_info[table_name] = {
                    "columns": columns,
                    "foreign_keys": foreign_keys
                }

            state["db_info"] = table_info
        except Exception as e:
            logger.error(f"Error getting database information: {e}")
        
        return state
    
    @staticmethod
    def execute_sql(state):
        logger.info("Executing SQL query")
        engine = create_engine(Config.DATABASE_URL)
        try:
            with engine.connect() as connection:
                result = connection.execute(text(state["generated_sql"]))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                state["execution_result"] = ExecutionResult(success=True, data=df.to_dict(orient="records"))
        except Exception as e:
            logger.error(f"Error executing SQL: {e}")
            state["execution_result"] = ExecutionResult(success=False, error=str(e))
        return state
    

    @staticmethod
    def execute_sql_correction(state):
        logger.info("Executing SQL query")
        engine = create_engine(Config.DATABASE_URL)
        try:
            with engine.connect() as connection:
                result = connection.execute(text(state["correction_result"].corrected_sql_query))
                df = pd.DataFrame(result.fetchall(), columns=result.keys())
                state["execution_result"] = ExecutionResult(success=True, data=df.to_dict(orient="records"))
        except Exception as e:
            logger.error(f"Error executing SQL: {e}")
            state["execution_result"] = ExecutionResult(success=False, error=str(e))
        return state
