import React from "react";
import useStreamStore from "../../state/streamStore";
import ScrollBox from "../common/ScrollBox";
import "./VisualView.css";

/* ─────────────────────────────
   Probability Bar
───────────────────────────── */
const ProbabilityBar = ({ value }) => {
    const pct = Math.round(value * 100);

    let color = "#22c55e";
    let label = "High likelihood";

    if (value < 0.6) {
        color = "#facc15";
        label = "Moderate likelihood";
    }
    if (value < 0.4) {
        color = "#f87171";
        label = "Low likelihood";
    }

    return (
        <div className="probability-wrapper">
            <div className="probability-title">
                Likelihood this scenario occurs
            </div>

            <div className="probability-bar">
                <div
                    className="probability-fill"
                    style={{
                        width: `${pct}%`,
                        backgroundColor: color
                    }}
                />
                <span className="probability-label">{pct}%</span>
            </div>

            <div className="probability-meaning">
                {label}
            </div>
        </div>
    );
};


/* ─────────────────────────────
   Scenario Card
───────────────────────────── */
const ScenarioCard = ({ scenario, index }) => (
    <div className="scenario-card">
        <div className="scenario-header">
            <span className="scenario-index">
                Scenario {index + 1}
            </span>
            <span className="scenario-driver">
                Driver: {scenario.primary_driver.replaceAll("_", " ")}
            </span>
        </div>

        <div className="scenario-body">
            <p className="scenario-text">
                {scenario.scenario}
            </p>

            <ProbabilityBar value={scenario.likelihood} />

            <div className="scenario-basis">
                {scenario.quantitative_basis}
            </div>

            <div className="scenario-neutralization">
                <div className="neutralization-title">
                    Winning Lever to Beat This Scenario
                </div>
                <div className="neutralization-text">
                    {scenario.winning_lever}
                </div>
            </div>
        </div>
    </div>
);


/* ─────────────────────────────
   Main View
───────────────────────────── */
const StakeholderVisualView = () => {
    // ✅ FIX: read from player_visual_blocks
    const scenarios = useStreamStore(
        s => s.player_visual_blocks?.scenarios
    );

    if (!Array.isArray(scenarios) || scenarios.length === 0) {
        return (
            <div className="simulation-empty">
                Awaiting simulation outcomes…
            </div>
        );
    }

    return (
        <ScrollBox className="simulation-scroll">
            <div className="simulation-container">
                <header className="simulation-header">
                    <h1>Simulated Match Outcomes</h1>
                    <p>
                        Probabilistic scenarios derived from analyst, coach,
                        executive, and player intelligence.
                    </p>
                </header>

                <div className="scenario-grid">
                    {scenarios.map((s, i) => (
                        <ScenarioCard
                            key={i}
                            scenario={s}
                            index={i}
                        />
                    ))}
                </div>
            </div>
        </ScrollBox>
    );
};

export default StakeholderVisualView;
