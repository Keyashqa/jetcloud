import React from "react";
import useStreamStore from "../../state/streamStore";
import ScrollBox from "../common/ScrollBox";
import "./CoachView.css";

/* ─────────────────────────────
   Normalizers (CRITICAL)
───────────────────────────── */

const normalizeType = (type = "") =>
    type
        .toLowerCase()
        .trim()
        .replace(/\s+/g, "_");

const normalizePracticeThemes = (themes = []) =>
    themes.map((t) => ({
        name: t.name ?? t.theme ?? "Unnamed Focus",
        description: t.description ?? "",
        priority: t.priority ?? null
    }));

/* ─────────────────────────────
   Shared Layout Components
───────────────────────────── */

const Section = ({ title, confidence, children }) => (
    <div className="coach-section">
        <div className="coach-section-header">
            <h3 className="coach-section-title">{title}</h3>
            {typeof confidence === "number" && (
                <span className="coach-section-confidence">
                    {(confidence * 100).toFixed(0)}% Confidence
                </span>
            )}
        </div>
        <div className="coach-section-body">{children}</div>
    </div>
);

/* ─────────────────────────────
   Block Renderers
───────────────────────────── */

const ExecutiveSummary = ({ data }) => (
    <div className="exec-summary">
        <div className="exec-row">
            <span className="exec-label">Opponent Identity</span>
            <div className="exec-value strong">
                {data.opponent_identity}
            </div>
        </div>

        <div className="exec-row">
            <span className="exec-label">Primary Win Condition</span>
            <div className="exec-value">
                {data.primary_win_condition}
            </div>
        </div>

        <div className="exec-row">
            <span className="exec-label">Primary Failure Condition</span>
            <div className="exec-value muted">
                {data.primary_failure_condition}
            </div>
        </div>

        <div className="exec-posture">
            <span className="exec-label">Recommended Posture</span>
            <div className="posture-pill">
                {data.recommended_posture}
            </div>
        </div>
    </div>
);

const MapVeto = ({ data }) => (
    <div className="map-veto">
        {data.decisions.map((d, i) => (
            <div
                key={i}
                className={`map-decision ${d.decision.toLowerCase()}`}
            >
                <div className="map-decision-type">
                    {d.decision}
                </div>

                <div className="map-decision-info">
                    <div className="map-name">{d.map_name}</div>
                    <div className="map-reason">{d.reasoning}</div>
                </div>

                <div className="map-confidence">
                    {(d.confidence * 100).toFixed(0)}%
                </div>
            </div>
        ))}
    </div>
);

const AgentTendencies = ({ data }) => (
    <div className="agent-tendencies">
        <div className="tendency-group">
            <span className="tendency-label">Core Agents</span>
            <div className="agent-badge-list">
                {data.core_agents.map((agent) => (
                    <span key={agent} className="agent-badge">
                        {agent}
                    </span>
                ))}
            </div>
        </div>

        <div className="tendency-group">
            <span className="tendency-label">Predictability</span>
            <span className="tendency-value highlight">
                {data.predictability}
            </span>
        </div>

        <div className="tendency-description">
            {data.what_breaks_if_countered}
        </div>
    </div>
);

const TargetPriority = ({ data }) => (
    <div className="target-priority">
        <div className="target-block primary">
            <div className="target-title">Primary Target</div>
            <div className="target-name">
                {data.primary_target.nickname}
            </div>
            <div className="target-reason">
                {data.primary_target.reasoning}
            </div>
        </div>

        <div className="target-block secondary">
            <div className="target-title">Secondary Target</div>
            <div className="target-name">
                {data.secondary_target.nickname}
            </div>
            <div className="target-reason">
                {data.secondary_target.reasoning}
            </div>
        </div>

        {data.avoid_duels_against.length > 0 && (
            <div className="target-block avoid">
                <div className="target-title">
                    Avoid Isolated Duels
                </div>
                {data.avoid_duels_against.map((p, i) => (
                    <div key={i} className="target-reason">
                        <strong>{p.player}:</strong> {p.reason}
                    </div>
                ))}
            </div>
        )}
    </div>
);

const PracticePlan = ({ data }) => {
    const themes = normalizePracticeThemes(data.themes);

    return (
        <div className="practice-plan">
            {themes.map((theme, i) => (
                <div key={i} className="practice-card">
                    <div className="practice-theme">
                        {theme.name}
                    </div>
                    <div className="practice-desc">
                        {theme.description}
                    </div>
                </div>
            ))}
        </div>
    );
};

const AdjustmentTriggers = ({ data }) => (
    <div className="triggers-list">
        {data.triggers.map((t, i) => (
            <div key={i} className="trigger-item">
                <div className="trigger-signal">{t.signal}</div>
                <div className="trigger-details">
                    <div className="trigger-sub">
                        <strong>Action:</strong> {t.action}
                    </div>
                    <div className="trigger-sub">
                        <strong>Reason:</strong> {t.reasoning}
                    </div>
                </div>
            </div>
        ))}
    </div>
);

/* ─────────────────────────────
   Main Coach View
───────────────────────────── */

const CoachView = () => {
    const blocks =
        useStreamStore((s) => s.coach_visual_blocks?.blocks) || [];

    if (blocks.length === 0) {
        return (
            <div className="coach-empty-state">
                <div className="empty-icon">📡</div>
                <div className="empty-text">
                    Awaiting Coach Strategy…
                </div>
            </div>
        );
    }

    const renderBlock = (block, idx) => {
        const { type, title, confidence, data } = block;

        const blockMap = {
            executive_summary: (
                <ExecutiveSummary data={data} />
            ),
            map_veto: <MapVeto data={data} />,
            agent_tendencies: (
                <AgentTendencies data={data} />
            ),
            target_priority: (
                <TargetPriority data={data} />
            ),
            practice_plan: (
                <PracticePlan data={data} />
            ),
            adjustment_triggers: (
                <AdjustmentTriggers data={data} />
            )
        };

        const normalizedType = normalizeType(type);
        const content = blockMap[normalizedType];

        if (!content) {
            console.warn("Unknown coach block:", block);
            return null;
        }

        return (
            <Section
                key={idx}
                title={title}
                confidence={confidence}
            >
                {content}
            </Section>
        );
    };

    return (
        <div className="coach-view-container">
            <ScrollBox className="coach-scroll-area">
                {blocks.map(renderBlock)}
            </ScrollBox>
        </div>
    );
};

export default CoachView;
