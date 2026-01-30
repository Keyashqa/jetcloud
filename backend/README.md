# 🎮 Scout - Intelligent E-Sports Analysis Backend

> **Production-Grade Agentic System for Valorant E-Sports Analysis**
> *Hackathon Prototype Version 0.1.0*

## 📚 Overview

**Scout** is a sophisticated backend system designed to provide deep, actionable intelligence for Valorant e-sports teams. By leveraging a multi-agent architecture powered by **Google Vertex AI (Gemini 2.5 Flash)** and **FastAPI**, Scout autonomously fetches, analyzes, and visualizes competitor data.

It ingests real-time match data from the **GRID E-sports API**, processes it through a hierarchy of specialized AI agents, and delivers structured strategic insights, including threat assessments, player volatility analysis, and win-probability simulations.

## 🏗️ Architecture

Scout operates on a sequential multi-agent pipeline orchestrated by the **Google ADK (Agent Development Kit)**.

### 🔄 The Agent Pipeline

1.  **🕵️ ScoutingAgent (Data Ingestion)**
    *   **Role**: The "Eyes" of the system.
    *   **Function**: Connects to the GRID API to fetch raw series data, team rosters, and historical performance (last 6 months).
    *   **Output**: Normalized CSV datasets (Series Overview, Player Stats, Team Segments).

2.  **🧠 AnalyzerAgent (Deep Analysis)**
    *   **Role**: The "Brain" of the system.
    *   **Function**: Performs advanced statistical analysis on the CSV data. It calculates derived metrics like Threat Levels, Exploitable Weaknesses, and Agent Pool Diversity.
    *   **Sub-Agents (Parallel Execution)**:
        *   **📊 AnalystAgent**: Focuses on quantitative validation and pattern recognition.
        *   **♟️ CoachAgent**: Derives tactical posture and preparation emphasis.
        *   **👔 ManagerAgent**: Evaluates opponent stability, dependency, and preparation costs.
        *   **🤺 OpponentAgent**: Analyzes player-facing pressure and volatility.

3.  **🔮 SimulationAgent (Predictive Modeling)**
    *   **Role**: The "Futurist" of the system.
    *   **Function**: Synthesizes all prior intelligence to simulate the top 5 most plausible match scenarios.
    *   **Output**: ROI-based probabilities and "Winning Levers" (conditions required for victory).

## 🛠️ Tech Stack

*   **Language**: Python 3.10+
*   **Framework**: FastAPI (High-performance Async API)
*   **AI Orchestration**: Google ADK (Agent Development Kit)
*   **LLM Model**: Google Gemini 2.5 Flash / Flash-Lite
*   **Data Processing**: Pandas, NumPy
*   **External API**: GRID E-sports Data API (GraphQL)
*   **Environment**: Google Cloud Vertex AI

---

## 🚀 Getting Started

### Prerequisites

*   Python 3.10 or higher
*   A Google Cloud Project with Vertex AI API enabled.
*   A GRID Data API Key (for e-sports data).

### Installation

1.  **Clone the repository** (if not already done).

2.  **Navigate to the backend directory**:
    ```bash
    cd backend
    ```

3.  **Create a virtual environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### ⚙️ Environment Configuration

Create a `.env` file in the `backend` root directory with the following variables:

```ini
# Google Cloud Vertex AI Configuration
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_API_KEY=your-gemini-api-key

# GRID E-Sports API Configuration
GRID_API_KEY=your-grid-api-key
```

### ▶️ Running the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn server:app --reload
```

The API will be available at `http://localhost:8000`.

---

## 🔌 API Documentation

### 1. `POST /run/stream`
The primary endpoint for initiating an analysis session. Streams agent events in real-time (Server-Sent Events).

**Payload:**
```json
{
  "user_id": "user_123",
  "session_id": "session_abc",
  "message": "Start analysis for NRG",
  "initial_state": {
    "team_name": "NRG"
  }
}
```

**Response (Stream):**
*   Returns a stream of JSON events.
*   Events include text logs (`kind: "text"`) and structured agent outputs (`kind: "structured"`).
*   Ends with `data: [DONE]`.

### 2. `GET /download_scouting_data`
Downloads all generated analysis artifacts as a ZIP file.

**Response:**
*   `content-type`: `application/zip`
*   Contains CSV files: `series_overview.csv`, `team_stats.csv`, `player_stats.csv`, `exploitable_weaknesses.csv`, etc.

---

## 📂 Project Structure

```
backend/
├── app/
│   ├── sub_agents/
│   │   ├── ScoutingAgent/       # GRID API integration
│   │   ├── AnalyzerAgent/       # Stats processing & logic
│   │   │   ├── sub_agents/      # Specialized stakeholder agents
│   │   ├── SimulationAgent/     # Scenario simulation
│   ├── agent.py                 # Root sequential agent definition
├── server.py                    # FastAPI application entry point
├── pyproject.toml               # Project configuration
├── requirements.txt             # Python dependencies
└── .env                         # Environment secrets
```

## 🤝 Contributing

1.  Fork the repository.
2.  Create a feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add some amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

---

**Built with ❤️ for the JetBrains Hackathon 2026** 🚀
