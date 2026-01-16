from google.adk.agents import Agent
from google.adk.models import Gemini
import os

MODEL_NAME = "gemini-2.5-flash-lite"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

parallel_agent = Agent(
    name="ParallelAgent",
    model=Gemini(
        model=MODEL_NAME,
        vertexai={"project": PROJECT_ID, "location": LOCATION}
    ),
    instruction="""
You act as a combined analysis agent.

Using the following collected data:
{data_acq_raw}

Perform:
1. A technical analysis (architecture, system design, engineering considerations)
2. A business analysis (value, impact, productivity, cost)

Clearly separate the two sections in your response.
""",
    output_key="combined_analysis",
)
