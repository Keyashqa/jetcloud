from google.adk.agents import SequentialAgent
from .sub_agents.ScoutingAgent import ScoutingAgent
from .sub_agents.AnalyzerAgent import AnalyzerAgent
from .sub_agents.SimulationAgent import player_visual_llm

root_agent = SequentialAgent(
    name="RootAgent",
    sub_agents=[ ScoutingAgent, AnalyzerAgent, player_visual_llm]
)
