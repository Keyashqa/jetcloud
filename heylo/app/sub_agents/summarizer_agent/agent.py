

from google.adk.agents import Agent
from google.adk.models import Gemini
import os

MODEL_NAME = "gemini-2.5-flash-lite"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

summarizer_agent = Agent(
    name="SummarizerAgent",
    model=Gemini(
        model=MODEL_NAME,
        vertexai={"project": PROJECT_ID, "location": LOCATION}
    ),
    instruction="""
Combine the following analyses into a clear, well-structured summary:

Combined analysis :
{combined_analysis}

Produce a concise, easy-to-understand final explanation.
""",
    output_key="final_summary",
)
