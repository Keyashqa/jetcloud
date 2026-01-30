import asyncio
import os
from dotenv import load_dotenv

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from app.agent import root_agent

# ─────────────────────────────────────────
# Environment
# ─────────────────────────────────────────

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY is not set")

# ─────────────────────────────────────────
# Config
# ─────────────────────────────────────────

APP_NAME = "simple_app"
USER_ID = "user_1"
SESSION_ID = "session_1"
INITIAL_STATE = {
    "team_name" : "NRG"
}

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# ─────────────────────────────────────────
# Run once
# ─────────────────────────────────────────

async def main():
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=INITIAL_STATE,
    )

    content = types.Content(
        role="user",
        parts=[types.Part(text="Start")]
    )

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content,
    ):
        if event.is_final_response():
            print("\n=== FINAL OUTPUT ===")
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())
