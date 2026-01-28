const analystMock = {
    blocks: [
        {
            id: "data_reliability",
            type: "data_reliability",
            title: "Data Reliability",
            confidence: 1.0,
            summary: "Overall opponent strength and momentum.",
            metrics: [
                { label: "Games Played", value: 27, unit: "games", confidence: "HIGH" },
                { label: "Series Played", value: 11, unit: "series", confidence: "HIGH" },
                { label: "Win Rate", value: 51.85, unit: "%", confidence: "HIGH" },
                { label: "Form", value: 0, unit: "W/L Streak", confidence: "HIGH" }
            ],
            charts: [],
            flags: []
        },
        {
            id: "team_patterns",
            type: "team_patterns",
            title: "Team Round Phase Performance",
            confidence: 0.7,
            summary: "Identifies team performance trends across different round phases.",
            metrics: [],
            charts: [
                {
                    chart_type: "bar",
                    x_labels: ["Pistol Round", "Mid Round", "Late Round"],
                    series: [
                        {
                            label: "Win Rate",
                            values: [50.0, 50.0, 45.0],
                            color_hint: "BLUE"
                        }
                    ]
                }
            ],
            flags: []
        },
        {
            id: "player_dependency",
            type: "player_dependency",
            title: "Player Contribution Analysis",
            confidence: 0.8,
            summary: "Analysis of individual player impact and potential carry dependency.",
            metrics: [
                { label: "Timotino Kills Avg", value: 50.63, unit: "kills/game", confidence: "HIGH" },
                { label: "Cryo Kills Avg", value: 44.09, unit: "kills/game", confidence: "HIGH" },
                { label: "bang Kills Avg", value: 38.08, unit: "kills/game", confidence: "HIGH" },
                { label: "Vora Kills Avg", value: 37.0, unit: "kills/game", confidence: "HIGH" },
                { label: "Asuna Kills Avg", value: 33.82, unit: "kills/game", confidence: "HIGH" }
            ],
            charts: [
                {
                    chart_type: "bar",
                    x_labels: ["Timotino", "Cryo", "bang", "Vora", "Asuna"],
                    series: [
                        {
                            label: "Average Kills per Game",
                            values: [50.63, 44.09, 38.08, 37.0, 33.82],
                            color_hint: "BLUE"
                        }
                    ]
                }
            ],
            flags: []
        },
        {
            id: "map_validation",
            type: "map_validation",
            title: "Map Performance",
            confidence: 0.8,
            summary: "Map-specific performance metrics.",
            metrics: [
                { label: "Bind K/D Differential", value: 49, unit: "K-D", confidence: "HIGH" },
                { label: "Corrode K/D Differential", value: 12, unit: "K-D", confidence: "HIGH" },
                { label: "Haven K/D Differential", value: -18, unit: "K-D", confidence: "HIGH" },
                { label: "Icebox K/D Differential", value: 0, unit: "K-D", confidence: "HIGH" },
                { label: "Lotus K/D Differential", value: -15, unit: "K-D", confidence: "HIGH" },
                { label: "Sunset K/D Differential", value: -70, unit: "K-D", confidence: "HIGH" }
            ],
            charts: [
                {
                    chart_type: "bar",
                    x_labels: ["Bind", "Corrode", "Haven", "Icebox", "Lotus", "Sunset"],
                    series: [
                        {
                            label: "Kills - Deaths",
                            values: [49, 12, -18, 0, -15, -70],
                            color_hint: "GREEN"
                        }
                    ]
                }
            ],
            flags: []
        },
        {
            id: "agent_pool_audit",
            type: "agent_pool_audit",
            title: "Agent Pool Analysis",
            confidence: 0.9,
            summary: "Agent pick concentration and diversity.",
            metrics: [
                { label: "Agent Diversity Index", value: 0.36, unit: null, confidence: "HIGH" }
            ],
            charts: [
                {
                    chart_type: "bar",
                    x_labels: ["Jett", "Chamber", "Raze"],
                    series: [
                        {
                            label: "Pick Rate",
                            values: [35.0, 24.0, 18.75],
                            color_hint: "BLUE"
                        }
                    ]
                }
            ],
            flags: ["MEDIUM_DIVERSITY"]
        },
        {
            id: "weakness_audit",
            type: "weakness_audit",
            title: "Identified Weaknesses",
            confidence: 0.8,
            summary: "Audit of pre-identified team weaknesses.",
            metrics: [],
            charts: [],
            flags: ["CARRY_DEPENDENCY_MEDIUM", "WEAK_OPENING_DUELS_HIGH"]
        }
    ]
};

export default analystMock;
