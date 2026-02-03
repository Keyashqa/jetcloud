# JetCloud & Scout - Esports Strategic Intelligence Platform

> **Production-Grade Agentic System for Valorant E-Sports Analysis**
> *Hackathon Prototype Version 0.1.0*

![Status](https://img.shields.io/badge/Status-Development-blue)
![React](https://img.shields.io/badge/React-19.0-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-7.0-646CFF?logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-4.0-38B2AC?logo=tailwindcss&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-009688?logo=fastapi&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-4285F4?logo=google&logoColor=white)

## 📚 Overview

Note : Re run the backend server after scouting a team to start over or incase of any unexpected error

This project combines **JetCloud** (Frontend) and **Scout** (Backend) to create a comprehensive Esports Strategic Intelligence Platform.

*   **JetCloud** is the visual dashboard designed to give competitive teams the upper hand. It aggregates, processes, and visualizes opponent data into actionable strategic insights tailored for different team roles (Coaches, Analysts, Managers).
*   **Scout** is the sophisticated backend system that powers JetCloud. It leverages a multi-agent architecture powered by **Google Vertex AI (Gemini 2.5 Flash)** to autonomously fetch match data from the **GRID E-sports API**, analyze it, and deliver structured insights.

## 🚀 Key Features

### Frontend (JetCloud)
*   **Multi-Persona Intelligence**: Specialized dashboards tailored to specific strategic roles:
    *   **📋 Coach View**: High-level strategy, team composition analysis, and win-condition modeling.
    *   **📊 Analyst View**: Deep-dive statistics, economy analysis, and player performance metrics.
    *   **💼 Manager View**: Roster oversight and logistical data.
    *   **🎯 Opponent View**: Targeted breakdowns of specific adversary playstyles and tendencies.
*   **Real-time Analysis Streaming**: Connects to the backend Agent Swarm to stream analysis data in real-time.
*   **Interactive Visualizations**: Rich visual blocks and charts for easy data consumption.
*   **Tactical "Scout & Breach" Workflow**: Simple input mechanism to target specific opponent teams.

### Backend (Scout)
*   **Autonomous Data Ingestion**: Connects to the GRID API to fetch raw series data, team rosters, and historical performance.
*   **Agentic Analysis Pipeline**:
    *   **🕵️ ScoutingAgent**: Fetches and normalizes data.
    *   **🧠 AnalyzerAgent**: Performs advanced statistical analysis and calculates derived metrics (Threat Levels, Weaknesses).
    *   **🔮 SimulationAgent**: Synthesizes intelligence to simulate match scenarios and win probabilities.
*   **Real-time Streaming**: Uses Server-Sent Events (SSE) to stream agent progress and results to the frontend.

## 🏗️ Architecture

The system operates on a sequential multi-agent pipeline orchestrated by the **Google ADK (Agent Development Kit)**.

1.  **Ingestion**: GRID API Data -> ScoutingAgent -> Normalized CSVs.
2.  **Analysis**: AnalyzerAgent -> Sub-Agents (Analyst, Coach, Manager, Opponent) -> Statistical Models.
3.  **Simulation**: SimulationAgent -> Prediction of match scenarios -> Win Probabilities.
4.  **Presentation**: FastAPI -> SSE Stream -> React Frontend (JetCloud).

## 🛠 Tech Stack

### Frontend
*   **Framework**: [React 19](https://react.dev/)
*   **Build Tool**: [Vite](https://vitejs.dev/)
*   **Styling**: [Tailwind CSS 4](https://tailwindcss.com/) & Vanilla CSS
*   **State Management**: [Zustand](https://zustand-demo.pmnd.rs/)
*   **Icons**: [Lucide React](https://lucide.dev/)

### Backend
*   **Language**: Python 3.10+
*   **Framework**: FastAPI
*   **AI Orchestration**: Google ADK (Agent Development Kit)
*   **LLM Model**: Google Gemini 2.5 Flash / Flash-Lite
*   **Data Processing**: Pandas, NumPy
*   **External API**: GRID E-sports Data API (GraphQL)
*   **Environment**: Google Cloud Vertex AI

## 📂 Project Structure

```
jetbrains/
├── frontend/            # React + Vite application
│   ├── src/
│   ├── public/
│   └── ...
├── backend/             # FastAPI + Google ADK application
│   ├── app/
│   ├── server.py
│   └── ...
└── README.md            # This file
```

## 🚀 Getting Started

### Prerequisites
*   **Node.js**: v18 or higher.
*   **Python**: 3.10 or higher.
*   **Google Cloud Project**: With Vertex AI API enabled.
*   **GRID API Key**: For e-sports data.

### Installation & Setup

#### 1. Backend Setup (Scout)

1.  Navigate to the backend directory:
    ```bash
    cd jetcloud
    cd backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    # Windows: .venv\Scripts\activate
    # Mac/Linux: source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Configure Environment (`backend/.env`):
    ```ini
    GOOGLE_GENAI_USE_VERTEXAI=True
    GOOGLE_CLOUD_PROJECT=your-gcp-project-id
    GOOGLE_CLOUD_LOCATION=us-central1
    GOOGLE_API_KEY=your-gemini-api-key
    GRID_API_KEY=your-grid-api-key
    ```
    Enable all permissions to use Vertex AI from Google Cloud Console
5.  Start the Server:
    ```bash
    uvicorn server:app --reload
    ```
    API will be running at `http://localhost:8000`.

#### 2. Frontend Setup (JetCloud)

1.  Open a new terminal and navigate to the frontend directory:
    ```bash
    cd jetcloud
    cd frontend
    ```
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Configure Environment (`frontend/.env`):
    ```env
    VITE_API_URL=http://localhost:8000
    ```
4.  Start Development Server:
    ```bash
    npm run dev
    ```
5.  Open in Browser:
    Navigate to `http://localhost:5173`.

## 🔌 API Documentation

### `POST /run/stream`
The primary endpoint for initiating an analysis session. Streams agent events in real-time.

**Payload:**
```json
{
  "user_id": "user_123",
  "session_id": "session_abc",
  "message": "Start analysis for NRG",
  "initial_state": { "team_name": "NRG" }
}
```

### `GET /download_scouting_data`
Downloads all generated analysis artifacts (CSVs) as a ZIP file.


*Built with ❤️ by JetCloud* 🚀
