from src.core.models import AgentState
from src.analysis.graph import create_graph, draw_graph
import logging

logging.basicConfig(level=logging.INFO)

initial_state = AgentState(
    user_query="Show me the number of employees for each level",
    attempts=0,
    correct_attempts=0,
)
graph = create_graph()
draw_graph(graph)
# final_state = graph.invoke(initial_state)

# print(final_state['execution_result'].data)
