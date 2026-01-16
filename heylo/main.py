import asyncio
import os
from dotenv import load_dotenv

# -------------------
# Environment setup
# -------------------

load_dotenv()

# HARD disable Vertex / Cloud inference
os.environ.pop("GOOGLE_GENAI_USE_VERTEXAI", None)
os.environ.pop("GOOGLE_CLOUD_PROJECT", None)
os.environ.pop("GOOGLE_CLOUD_LOCATION", None)

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY is not set in environment")

# -------------------
# ADK imports
# -------------------

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from google.adk.models.google_llm import Gemini
from app.agent import root_agent


# -------------------
# App / session config
# -------------------

APP_NAME = "scout_app"
USER_ID = "user_1"
SESSION_ID = "session_001"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


# -------------------
# Async call helper
# -------------------

async def call_agent_async(query: str):
    print(f"\n>>> User: {query}")

    content = types.Content(
        role="user",
        parts=[types.Part(text=query)]
    )

    final_response_text = "Agent did not produce a final response."

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            break

    print(f"<<< Agent: {final_response_text}")


# -------------------
# Main loop
# -------------------

async def run_conversation():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    print("🤖 Agent running (API key mode). Type 'exit' to stop.\n")

    while True:
        user_query = input("You: ").strip()

        if user_query.lower() in {"exit", "quit"}:
            print("👋 Conversation ended.")
            break

        if user_query:
            await call_agent_async(user_query)


# -------------------
# Entry point
# -------------------

if __name__ == "__main__":
    try:
        asyncio.run(run_conversation())
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user.")
