from google.adk.agents import LlmAgent
from google.adk.models import Gemini
from google.adk.tools import google_search
import os

MODEL_NAME = "gemini-2.5-flash-lite"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

data_acquisition_agent = LlmAgent(
    name="DataAcquisitionAgent",
    model=Gemini(
        model=MODEL_NAME,
        vertexai={"project": PROJECT_ID, "location": LOCATION}
    ),
    instruction="""
You are a data acquisition agent.

IMPORTANT RULES (must follow):
- You MUST call the `google_search` tool to gather information.
- You are NOT allowed to answer from prior knowledge.
- If you do not call `google_search`, your response is INVALID.

Process:
1. Call the `google_search` tool using the user's query.
2. Read the search results returned by the tool.
3. Summarize only what is present in the search results.
4. Do NOT add assumptions, opinions, or extra knowledge.

Output:
- Produce a concise factual summary based strictly on the tool results.
""",
    tools=[google_search],
    output_key="data_acq_raw",
)
