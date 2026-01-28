import React from 'react';
import useStreamStore from '../../state/streamStore';
import ScrollBox from '../common/ScrollBox';
import './ManagerView.css';

/* ─────────────────────────────
   Shared Section Wrapper
───────────────────────────── */

const Section = ({ title, confidence, children }) => (
    <div className="manager-section">
        <div className="manager-section-header">
            <h3 className="manager-section-title">{title}</h3>

            {typeof confidence === 'number' && (
                <div className="confidence-badge">
                    <span className="conf-label">Confidence</span>
                    <span className="conf-value">
                        {(confidence * 100).toFixed(0)}%
                    </span>
                </div>
            )}
        </div>

        <div className="manager-section-body">
            {children}
        </div>
    </div>
);

/* ─────────────────────────────
   Block Renderers (NEW)
───────────────────────────── */

const OpponentStability = ({ data = {} }) => (
    <div className="stability-grid">
        <div className="stability-card">
            <div className="label">Stability Rating</div>
            <div className="value">
                {data.stability_rating || 'N/A'}
            </div>
        </div>

        <div className="stability-card">
            <div className="label">Assessment</div>
            <div className="description">
                {data.reasoning || 'No stability assessment provided.'}
            </div>
        </div>
    </div>
);

const DependencyProfile = ({ data = {} }) => (
    <div className="dependency-grid">
        <div className="dependency-card">
            <div className="label">Dependency Type</div>
            <div className="value">
                {data.dependency_type || 'N/A'}
            </div>
        </div>

        <div className="dependency-card">
            <div className="label">Top Dependency Share</div>
            <div className="value highlight">
                {typeof data.top_dependency_share === 'number'
                    ? `${Math.round(data.top_dependency_share * 100)}%`
                    : 'N/A'}
            </div>
        </div>

        <div className="dependency-wide">
            {data.reasoning || 'No dependency reasoning provided.'}
        </div>
    </div>
);

const RiskExposure = ({ data = {} }) => (
    <div className="risk-card">
        <div className="risk-header">
            <span className="risk-type">
                {data.risk_type || 'Unknown Risk'}
            </span>
            <span className={`risk-severity ${data.severity?.toLowerCase() || ''}`}>
                {data.severity || 'N/A'}
            </span>
        </div>

        <div className="risk-confidence">
            Confidence: {typeof data.confidence === 'number'
                ? `${Math.round(data.confidence * 100)}%`
                : 'N/A'}
        </div>
    </div>
);

const PreparationCost = ({ data = {} }) => (
    <div className="prep-grid">
        <div className="prep-card">
            <div className="label">Preparation Complexity</div>
            <div className="value">
                {data.prep_complexity || 'N/A'}
            </div>
        </div>

        <div className="prep-card">
            <div className="label">Adaptation Risk</div>
            <div className="value">
                {data.adaptation_risk || 'N/A'}
            </div>
        </div>

        <div className="prep-wide">
            {data.reasoning || 'No preparation insight provided.'}
        </div>
    </div>
);

const ExploitSustainability = ({ data = {} }) => (
    <div className="exploit-card">
        <div className="exploit-header">
            <span className="exploit-type">
                {data.exploit_type || 'Unnamed Exploit'}
            </span>
            <span className={`exploit-sustainability ${data.sustainability?.toLowerCase() || ''}`}>
                {data.sustainability || 'N/A'}
            </span>
        </div>

        <div className="exploit-confidence">
            Confidence: {typeof data.confidence === 'number'
                ? `${Math.round(data.confidence * 100)}%`
                : 'N/A'}
        </div>
    </div>
);

const ManagementSummary = ({ data = {} }) => (
    <div className="summary-grid">
        <div className="summary-card risk">
            <div className="label">Primary Long-Term Risk</div>
            <div className="content">
                {data.primary_long_term_risk || 'No risk identified.'}
            </div>
        </div>

        <div className="summary-card weakness">
            <div className="label">Weakness Likely to Self-Correct</div>
            <div className="content">
                {data.primary_weakness_self_correct || 'No weakness noted.'}
            </div>
        </div>

        <div className="summary-card question">
            <div className="label">Monitoring Question</div>
            <div className="content">
                {data.monitoring_question || 'No monitoring question provided.'}
            </div>
        </div>
    </div>
);

/* ─────────────────────────────
   Main View
───────────────────────────── */

const ManagerView = () => {
    const blocks =
        useStreamStore((s) => s.manager_visual_blocks?.blocks) || [];

    if (!blocks.length) {
        return (
            <div className="manager-empty-state">
                Awaiting Management Review…
            </div>
        );
    }

    const renderBlock = (block, idx) => {
        const { type, title, confidence, data } = block;

        const map = {
            opponent_stability: <OpponentStability data={data} />,
            dependency_profile: <DependencyProfile data={data} />,
            risk_exposure: <RiskExposure data={data} />,
            prep_cost: <PreparationCost data={data} />,
            exploit_sustainability: <ExploitSustainability data={data} />,
            management_summary: <ManagementSummary data={data} />
        };

        const content = map[type];
        if (!content) return null;

        return (
            <Section key={idx} title={title} confidence={confidence}>
                {content}
            </Section>
        );
    };

    return (
        <ScrollBox className="manager-scroll-area">
            <div className="manager-content-wrapper">
                {blocks.map(renderBlock)}
            </div>
        </ScrollBox>
    );
};

export default ManagerView;
