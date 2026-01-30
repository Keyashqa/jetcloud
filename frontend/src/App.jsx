import "./dashboard.css";
import TopBar from "./components/TopBar/TopBar";
import LogsPanel from "./components/Loggy/Log";
import StakeholderView from "./components/Stakeholders/StakeholderView";

function App() {
  return (
    <div className="dashboard-root">
      <div style={{ maxWidth: "100%" }}>
        <TopBar />

        <div
          style={{
            marginTop: "2px",
            display: "grid",
            gridTemplateColumns: "7.5fr 2.5fr",
            gap: "2px",
          }}
        >
          <StakeholderView />
          <LogsPanel />
        </div>
      </div>
    </div>
  );
}

export default App;
