import React from "react";
import "./AnalystView.css";
import useStreamStore from "../../state/streamStore";

/* ─────────────────────────────
Pure SVG Bar Chart Component
───────────────────────────── */
const BarChart = ({ chartData }) => {
    if (!chartData || !chartData.x_labels || !chartData.series || chartData.series.length === 0) {
        return null;
    }

    const colorMap = {
        BLUE: "#3b82f6",
        GREEN: "#10b981",
        RED: "#ef4444",
        YELLOW: "#f59e0b",
        PURPLE: "#a855f7"
    };

    const series = chartData.series[0];
    const values = series.values;
    const labels = chartData.x_labels;

    const allValues = values.filter(v => typeof v === 'number');
    const maxVal = Math.max(...allValues, 0);
    const minVal = Math.min(...allValues, 0);
    const range = maxVal - minVal || 1;
    const hasNegative = minVal < 0;

    const chartHeight = 250;
    const barWidth = 60;
    const gap = 20;
    const chartWidth = labels.length * (barWidth + gap);

    return (
        <div className="chart-container">
            <div className="chart-title">{series.label}</div>

            <svg width={chartWidth} height={chartHeight + 60} className="bar-chart-svg">
                {hasNegative && (
                    <line
                        x1="0"
                        y1={chartHeight - ((0 - minVal) / range) * chartHeight}
                        x2={chartWidth}
                        y2={chartHeight - ((0 - minVal) / range) * chartHeight}
                        stroke="#374151"
                        strokeWidth="2"
                        strokeDasharray="4 4"
                    />
                )}

                {values.map((value, i) => {
                    if (typeof value !== 'number') return null;

                    const x = i * (barWidth + gap);
                    const barHeight = (Math.abs(value - (hasNegative ? 0 : minVal)) / range) * chartHeight;
                    const y = hasNegative
                        ? (value >= 0
                            ? chartHeight - ((0 - minVal) / range) * chartHeight - barHeight
                            : chartHeight - ((0 - minVal) / range) * chartHeight)
                        : chartHeight - barHeight;

                    return (
                        <g key={i}>
                            <rect
                                x={x}
                                y={y}
                                width={barWidth}
                                height={barHeight}
                                fill={colorMap[series.color_hint] || colorMap.BLUE}
                                opacity="0.9"
                                rx="4"
                            />

                            <text
                                x={x + barWidth / 2}
                                y={y - 8}
                                textAnchor="middle"
                                fill="#e2e8f0"
                                fontSize="12"
                                fontWeight="600"
                            >
                                {value.toFixed(1)}
                            </text>

                            <text
                                x={x + barWidth / 2}
                                y={chartHeight + 20}
                                textAnchor="middle"
                                fill="#94a3b8"
                                fontSize="11"
                                transform={labels[i].length > 8 ? `rotate(-45, ${x + barWidth / 2}, ${chartHeight + 20})` : ''}
                            >
                                {labels[i]}
                            </text>
                        </g>
                    );
                })}
            </svg>
        </div>
    );
};

/* ─────────────────────────────
Confidence Indicator
───────────────────────────── */
const ConfidenceShield = ({ score }) => {
    if (typeof score !== "number") return null;

    const percent = Math.round(score * 100);
    let color = "#f87171";
    if (score >= 0.8) color = "#4ade80";
    else if (score >= 0.6) color = "#fbbf24";

    return (
        <div className="confidence-shield">
            <span className="confidence-label">Confidence</span>
            <span className="confidence-value" style={{ color }}>
                {percent}%
            </span>
        </div>
    );
};

/* ─────────────────────────────
Analyst Section
───────────────────────────── */
const AnalystSection = ({ block }) => {
    if (!block || !block.title) {
        console.warn("Invalid block:", block);
        return null;
    }

    const hasMetrics = Array.isArray(block.metrics) && block.metrics.length > 0;
    const hasFlags = Array.isArray(block.flags) && block.flags.length > 0;
    const hasCharts = Array.isArray(block.charts) && block.charts.length > 0;
    const hasSummary = typeof block.summary === "string" && block.summary.trim() !== "";

    if (!hasMetrics && !hasFlags && !hasCharts && !hasSummary) {
        console.warn("Block has no renderable content:", block.id);
        return null;
    }

    return (
        <section
            className={`analyst-section ${block.type === "map_validation" ? "map-performance" : ""}`}
        >
            <div className="section-divider">
                <div className="divider-line" />
                <h3 className="section-title">{block.summary}</h3>
                <div className="divider-line" />
            </div>

            <div className="block-container">
                <aside className="block-sidebar">
                    <ConfidenceShield score={block.confidence} />

                    {hasSummary ? (
                        <p className="block-summary">{block.summary}</p>
                    ) : (
                        <p className="block-summary muted">
                            No high-level summary available.
                        </p>
                    )}

                    {hasFlags && (
                        <div className="flag-container">
                            {block.flags.map((flag, i) => (
                                <span
                                    key={i}
                                    className={`flag-pill ${flag.includes("WEAK") ||
                                        flag.includes("DEPENDENCY")
                                        ? "warning"
                                        : ""
                                        }`}
                                >
                                    {flag.replaceAll("_", " ")}
                                </span>
                            ))}
                        </div>
                    )}
                </aside>

                <div className="block-main">
                    {hasMetrics ? (
                        <div className="metric-grid">
                            {block.metrics.map((m, i) => {
                                if (!m?.label || m.value === undefined) return null;

                                return (
                                    <div key={i} className="metric-card">
                                        <div className="metric-label">{m.label}</div>
                                        <div className="metric-value-wrap">
                                            <span className="metric-value">
                                                {typeof m.value === 'number'
                                                    ? m.value.toFixed(2)
                                                    : m.value}
                                            </span>
                                            {m.unit && (
                                                <span className="metric-unit">
                                                    {m.unit}
                                                </span>
                                            )}
                                        </div>
                                    </div>
                                );
                            })}
                        </div>
                    ) : (
                        <div className="metric-empty">
                            No quantitative metrics available for this section.
                        </div>
                    )}

                    {hasCharts && block.charts.map((chart, i) => (
                        <BarChart key={i} chartData={chart} />
                    ))}
                </div>
            </div>
        </section>
    );
};

/* ─────────────────────────────
Analyst View Root
───────────────────────────── */
const AnalystView = () => {
    const blocks = useStreamStore(
        (s) => s.analyst_visual_blocks?.blocks
    );

    // Debug logging
    React.useEffect(() => {
        console.log("AnalystView render - blocks:", blocks);
        if (blocks) {
            console.log("Number of blocks:", blocks.length);
            blocks.forEach(b => {
                console.log(`Block ${b.id}:`, {
                    hasMetrics: b.metrics?.length,
                    hasCharts: b.charts?.length,
                    hasFlags: b.flags?.length
                });
            });
        }
    }, [blocks]);

    if (!Array.isArray(blocks) || blocks.length === 0) {
        return (
            <div className="dashboard-wrapper">
                <header className="dashboard-header">
                    <div className="header-title">
                        <div className="header-tagline">
                            Cloud9 Match Analysis Engine
                        </div>
                        <h1>Analytical Validation</h1>
                    </div>
                </header>

                <div className="dashboard-empty">
                    Awaiting analyst data…
                </div>
            </div>
        );
    }

    return (
        <div className="dashboard-wrapper">
            <header className="dashboard-header">
                <div className="header-title">
                    <div className="header-tagline">
                        Match Analysis Engine
                    </div>

                </div>
                <div className="header-meta">
                    <div className="team-name">// VALORANT</div>
                    <div className="match-id">Metrics Dashboard</div>
                </div>
            </header>

            <main className="dashboard-content">
                {blocks.map((block) => (
                    <AnalystSection key={block.id} block={block} />
                ))}
            </main>
        </div>
    );
};

export default AnalystView;