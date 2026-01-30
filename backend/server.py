import os
import asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
import json
import pandas as pd

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
# FastAPI app
# ─────────────────────────────────────────

app = FastAPI(title="Agent Backend API")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────
# ADK setup (GLOBAL, reused across requests)
# ─────────────────────────────────────────

APP_NAME = "simple_app"

session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)

# ─────────────────────────────────────────
# Request / Response models
# ─────────────────────────────────────────

class RunRequest(BaseModel):
    user_id: str
    session_id: str
    message: str
    initial_state: dict | None = None


class RunResponse(BaseModel):
    final_output: str
    session_state: dict


# ─────────────────────────────────────────
# Helper to ensure session exists
# ─────────────────────────────────────────

async def ensure_session(app_name, user_id, session_id, initial_state):
    session = await session_service.get_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id,
    )

    if session is None:
        await session_service.create_session(
            app_name=app_name,
            user_id=user_id,
            session_id=session_id,
            state=initial_state or {},
        )



@app.post("/run/stream")
async def run_agent_stream(req: RunRequest):
    async def event_generator():
        try:
            await ensure_session(
                app_name=APP_NAME,
                user_id=req.user_id,
                session_id=req.session_id,
                initial_state=req.initial_state,
            )

            content = types.Content(
                role="user",
                parts=[types.Part(text=req.message)],
            )

            async for event in runner.run_async(
                user_id=req.user_id,
                session_id=req.session_id,
                new_message=content,
            ):
                payload = {
                    "author": event.author,
                    "is_final": event.is_final_response(),
                    "kind": "text",
                }

                if event.content and event.content.parts:
                    raw_text = event.content.parts[0].text
                    payload["text"] = raw_text

                    if raw_text and raw_text.strip().startswith("{"):
                        payload["kind"] = "structured"
                    else:
                        payload["kind"] = "text"

                yield f"data: {json.dumps(payload)}\n\n"

            yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )



# ─────────────────────────────────────────
# Download Endpoint
# ─────────────────────────────────────────

import zipfile
import io
from fastapi.responses import Response

@app.get("/download_scouting_data")
async def download_scouting_data():
    scouting_dir = os.path.join("app", "scouting_outputs")

    if not os.path.exists(scouting_dir):
        raise HTTPException(
            status_code=404,
            detail="Scouting data directory not found"
        )

    zip_buffer = io.BytesIO()
    csv_files = []

    # 1️⃣ Create ZIP in memory
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, _, files in os.walk(scouting_dir):
            for file in files:
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file)
                    zip_file.write(file_path, arcname=file)
                    csv_files.append(file_path)

    zip_buffer.seek(0)

    # 2️⃣ Delete CSV files AFTER zip is finalized
    for file_path in csv_files:
        try:
            os.remove(file_path)
        except Exception as e:
            # Optional: log this instead of failing the request
            print(f"Failed to delete {file_path}: {e}")

    # 3️⃣ Return ZIP
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": 'attachment; filename="scouting_data.zip"'
        }
    )





