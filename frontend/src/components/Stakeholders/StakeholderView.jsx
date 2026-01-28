import useStreamStore from "../../state/streamStore";
import StakeholderTabs from "./StakeholderTabs";
import AnalystView from "./AnalystView";
import ManagerView from "./ManagerView";
import OpponentView from "./OpponentView";
import DownloadCSVView from "./DownloadCSVView";
import DataExplorerView from "./DataExplorerView";
import StakeholderVisualView from "./VisualView";
import CoachView from "./CoachView";

const StakeholderView = () => {
    const activeTab = useStreamStore((state) => state.activeTab);

    return (
        <div className="dashboard-shell">
            <StakeholderTabs />

            <div className="dashboard-content">
                {activeTab === "visuals" && <StakeholderVisualView />}
                {activeTab === "coach" && <CoachView />}
                {activeTab === "analyst" && <AnalystView />}
                {activeTab === "player" && <OpponentView />}
                {activeTab === "manager" && <ManagerView />}
                {activeTab === "download" && <DownloadCSVView />}
                {activeTab === "data" && <DataExplorerView />}

            </div>
        </div>
    );
};

export default StakeholderView;
