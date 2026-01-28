# JetCloud - Esports Strategic Intelligence Platform

![Status](https://img.shields.io/badge/Status-Development-blue)
![React](https://img.shields.io/badge/React-19.0-61DAFB?logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-7.0-646CFF?logo=vite&logoColor=white)
![Tailwind](https://img.shields.io/badge/Tailwind_CSS-4.0-38B2AC?logo=tailwindcss&logoColor=white)

**JetCloud** is a cutting-edge Esports output analysis dashboard designed to give competitive teams the upper hand. By leveraging advanced AI agents, it aggregates, processes, and visualizes opponent data into actionable strategic insights tailored for different team roles: Coaches, Analysts, and Managers.

## 🚀 Key Features

*   **Multi-Persona Intelligence**: Specialized dashboards tailored to specific strategic roles:
    *   **📋 Coach View**: High-level strategy, team composition analysis, and win-condition modeling.
    *   **📊 Analyst View**: Deep-dive statistics, economy analysis, and player performance metrics.
    *   **💼 Manager View**: Roster oversight and logistical data.
    *   **🎯 Opponent View**: Targeted breakdowns of specific adversary playstyles and tendencies.
*   **Real-time Analysis Streaming**: Connects to a powerful backend Agent Swarm to stream analysis data in real-time as it is generated.
*   **Interactive Visualizations**: Rich visual blocks and charts for easy data consumption.
*   **Tactical "Scout & Breach" Workflow**: Simple input mechanism to target specific opponent teams and initiate comprehensive analysis.
*   **Export Capabilities**: Download analyzed data in CSV format for offline study.

## 🛠 Tech Stack

### Frontend
*   **Framework**: [React 19](https://react.dev/)
*   **Build Tool**: [Vite](https://vitejs.dev/)
*   **Styling**: [Tailwind CSS 4](https://tailwindcss.com/) & Vanilla CSS for custom dashboards
*   **State Management**: [Zustand](https://zustand-demo.pmnd.rs/)
*   **Icons**: [Lucide React](https://lucide.dev/)

### Backend Integration
*   The frontend is designed to consume streaming data from a **FastAPI** backend powering Google Gemini AI agents.

## 📂 Project Structure

```bash
frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # UI Components
│   │   ├── Logs/        # Real-time message logging panel
│   │   ├── Stakeholders/# Dashboard views (Coach, Analyst, Manager, etc.)
│   │   └── TopBar/      # Main navigation and search execution
│   ├── state/           # Global Store (Zustand)
│   ├── utils/           # Helper functions (Stream parsing, etc.)
│   ├── api.jsx          # API Client & EventSource handling
│   ├── App.jsx          # Main application layout
│   └── main.jsx         # Entry point
├── .env                 # Environment variables
├── package.json         # Dependencies & Scripts
└── vite.config.js       # Vite configuration
```

## ⚙️ Prerequisites

*   **Node.js**: v18 or higher recommended.
*   **npm** or **yarn**.

## 🚀 Installation & Setup


1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository-url>
    cd jetbrains/frontend
    ```
2. **Create a virtual environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate

3.  **Install dependencies**:
    ```bash
    npm install
    ```

4.  **Configure Environment**:
    Ensure you have an `.env` file in the root of the `frontend` directory. It should point to your active backend service:
    ```env
    VITE_API_URL=http://localhost:8000
    ```

5.  **Run Development Server**:
    ```bash
    npm run dev
    ```

6.  **Open in Browser**:
    Navigate to `http://localhost:5173` to view the application.

## 🔧 Building for Production

To create a production-ready build:

```bash
npm run build
```

This will generate a `dist` folder containing the optimized static assets ready for deployment.

## 🤝 Contributing

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

---
*Built for the JetBrains Hackathon 2026* 🚀
