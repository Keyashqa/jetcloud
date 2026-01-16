import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import SequentialAgent
from google.adk.apps import App
from google.adk.models import Gemini
from app.sub_agents.data_acquisition_agent.agent import data_acquisition_agent
from app.sub_agents.parallel_agent.agent import parallel_agent
from app.sub_agents.summarizer_agent.agent import summarizer_agent

import os

MODEL_NAME = "gemini-2.5-flash"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")




root_agent = SequentialAgent(
    name="MainPipeline",
    sub_agents=[
        data_acquisition_agent,
        parallel_agent,
        summarizer_agent,
    ],
)


app = App(root_agent=root_agent, name="app")
