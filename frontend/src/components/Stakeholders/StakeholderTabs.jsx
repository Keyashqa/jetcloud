import React from 'react';
import { User, Users, Briefcase, TrendingUp, Download, BarChart } from 'lucide-react';
import useStreamStore from '../../state/streamStore';
import './Stakeholder.css';

const TABS = [
    { id: 'visuals', label: 'Simulation', icon: BarChart },
    { id: 'coach', label: 'Coach', icon: TrendingUp },
    { id: 'analyst', label: 'Analyst', icon: Briefcase },
    { id: 'player', label: 'Player', icon: User },
    { id: 'manager', label: 'Manager', icon: Users },
    { id: 'download', label: 'Download CSV', icon: Download },
];

const StakeholderTabs = () => {
    const { activeTab, setActiveTab, csvReady } = useStreamStore();

    return (
        <div className="tabs-container">
            {TABS.map((tab) => {
                const Icon = tab.icon;
                const isActive = activeTab === tab.id;
                const isDisabled = tab.id === 'download' && !csvReady;

                return (
                    <button
                        key={tab.id}
                        disabled={isDisabled}
                        onClick={() => setActiveTab(tab.id)}
                        className={`tabs-btn ${isActive ? 'is-active' : ''} ${isDisabled ? 'is-disabled' : ''}`}
                    >
                        <Icon size={14} className="tabs-icon" />
                        <span>{tab.label}</span>
                    </button>
                );
            })}
        </div>
    );
};

export default StakeholderTabs;