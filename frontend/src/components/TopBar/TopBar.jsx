import React, { useState } from 'react';
import useStreamStore from '../../state/streamStore';
import { startStream } from '../../utils/streamParser';
import { Crosshair } from 'lucide-react';
import './TopBarCss.css';

const TopBar = () => {
    const [localTarget, setLocalTarget] = useState('');
    const { isStreaming, userId, sessionId } = useStreamStore();
    const [showMockNotice, setShowMockNotice] = useState(true);


    const handleRun = () => {
        if (!localTarget.trim()) return;
        const initialState = { team_name: localTarget };
        startStream(userId, sessionId, localTarget, initialState);
    };

    return (
        <header className="topbar-header">
            {showMockNotice && (
                <div className="mock-data-popup">
                    <span>
                        ⚠ Initial response from agents are running on <strong>mock data</strong>
                        ...Execute with a valid team name to get real-time data.
                    </span>
                    <button
                        className="mock-data-close"
                        onClick={() => setShowMockNotice(false)}
                    >
                        ✕
                    </button>
                </div>
            )}

            {/* Branding - Stacked Layout */}
            <div className="topbar-brand">
                <div className="flex flex-col items-start">
                    <h1 className="topbar-logo-text leading-tight">
                        Jet<span className="topbar-logo-accent">Cloud</span>
                    </h1>
                    <span className="text-[12px] tracking-[0.35em] text-[#ffffff] uppercase font-bold opacity-90 -mt-1">
                        SCOUT. BREACH. CONQUER
                    </span>
                </div>
            </div>

            {/* Tactical Search */}
            <div className="topbar-search-area">
                <div className="topbar-input-wrapper">
                    <Crosshair
                        size={16}
                        className={isStreaming ? "animate-spin-custom" : ""}
                        style={{ color: '#e5484d' }}
                    />
                    <input
                        className="topbar-input"
                        placeholder="ENTER OPPONENT TEAM..."
                        value={localTarget}
                        onChange={(e) => setLocalTarget(e.target.value)}
                        onKeyDown={(e) => e.key === 'Enter' && handleRun()}
                        disabled={isStreaming}
                    />
                </div>

                <button
                    onClick={handleRun}
                    disabled={isStreaming || !localTarget}
                    className="topbar-btn"
                >
                    {isStreaming ? 'SCANNING' : 'EXECUTE'}
                </button>
            </div>

            {/* Metadata HUD */}
            <div className="topbar-metadata">
                <div className="topbar-session-hud">
                    <span className="topbar-id-label">ID:</span>
                    <span className="topbar-id-value">{sessionId || 'NULL'}</span>
                </div>

                {isStreaming && (
                    <span className="topbar-status">
                        ● LIVE FEED
                    </span>
                )}
            </div>
        </header>
    );
};

export default TopBar;