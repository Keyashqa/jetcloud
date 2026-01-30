import React, { useEffect, useRef } from 'react';
import useStreamStore from '../../state/streamStore';
import { Terminal } from 'lucide-react';
import './Log.css';

const LogsPanel = () => {
    const logs = useStreamStore((state) => state.logs);
    const bottomRef = useRef(null);

    useEffect(() => {
        if (bottomRef.current) {
            bottomRef.current.scrollIntoView({ behavior: 'smooth' });
        }
    }, [logs]); // Added logs to dependency to scroll on update

    return (
        <div className="logs-panel-container">
            {/* Tactical Header */}
            <div className="logs-panel-header">
                <div className="logs-panel-title">
                    <Terminal size={12} strokeWidth={3} />
                    <span>System Whispers</span>
                </div>
                <div className="logs-header-dots">
                    <div className="logs-dot" />
                    <div className="logs-dot" style={{ opacity: 0.1 }} />
                </div>
            </div>

            {/* Main Logs Display */}
            <div className="logs-panel-body">
                {logs.length === 0 && (
                    <div className="logs-empty-state">
                        ... AWAITING TACTICAL DATA UPLINK ...
                    </div>
                )}

                {logs.map((log, i) => (
                    <div key={i} className="logs-entry">
                        <span className="logs-timestamp">
                            [{new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit' })}]
                        </span>
                        <div className="logs-content">
                            <span className="logs-author">
                                {log.author} //
                            </span>
                            <span className="logs-text">
                                {log.text}
                            </span>
                        </div>
                    </div>
                ))}
                <div ref={bottomRef} />
            </div>
        </div>
    );
};

export default LogsPanel;