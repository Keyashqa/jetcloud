import React from "react";
import useStreamStore from "../../state/streamStore";
import ScrollBox from "../common/ScrollBox";
import "./OpponentView.css";

/* ─────────────────────────────
   Section Wrapper
───────────────────────────── */
const Section = ({ title, confidence, children }) => {
    return (
        <div className="player-section">
            <div className="player-section-header">
                <h3 className="player-section-title">
                    {title}
                </h3>

                {typeof confidence === "number" && (
                    <span className="player-section-confidence">
                        {(confidence * 100).toFixed(0)}%
                    </span>
                )}
            </div>

            <div className="player-section-body">
                {children}
            </div>
        </div>
    );
};

/* ─────────────────────────────
   Insight Row
───────────────────────────── */
const InsightRow = ({ insight }) => {
    if (!insight?.insight || !insight?.reason) return null;

    return (
        <div className="insight-row">
            <div className="insight-row-header">
                <span className="insight-text">
                    {insight.insight}
                </span>

                {typeof insight.confidence === "number" && (
                    <span className="insight-confidence">
                        {(insight.confidence * 100).toFixed(0)}%
                    </span>
                )}
            </div>

            <div className="insight-reason">
                {insight.reason}
            </div>
        </div>
    );
};

/* ─────────────────────────────
   Generic Insight Block
───────────────────────────── */
const InsightBlock = ({ block }) => {
    if (!block || !Array.isArray(block.insights)) {
        console.warn("Invalid scouting block:", block);
        return null;
    }

    return (
        <Section
            title={block.title}
            confidence={block.confidence}
        >
            <div className="insight-list">
                {block.insights.map((insight, idx) => (
                    <InsightRow
                        key={idx}
                        insight={insight}
                    />
                ))}
            </div>
        </Section>
    );
};

/* ─────────────────────────────
   Opponent View (Player Facing)
───────────────────────────── */
const OpponentView = () => {
    const blocks = useStreamStore(
        s => s.opponent_visual_blocks?.blocks
    );

    if (!Array.isArray(blocks) || blocks.length === 0) {
        return (
            <div className="player-empty">
                Awaiting Player Intel…
            </div>
        );
    }

    return (
        <ScrollBox className="player-scroll">
            <div className="player-container">
                {blocks.map((block, idx) => (
                    <InsightBlock
                        key={idx}
                        block={block}
                    />
                ))}
            </div>
        </ScrollBox>
    );
};

export default OpponentView;
