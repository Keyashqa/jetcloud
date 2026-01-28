const coachMock = {
    blocks: [
        {
            type: "executive_summary",
            title: "Cloud9 vs 100 Thieves — Coach Read",
            confidence: 0.78,
            data: {
                opponent_identity:
                    "100 Thieves rely heavily on individual firepower over structured mid-round systems. When early engagements fail, their coordination degrades rapidly.",
                primary_win_condition:
                    "Deny early duel confidence and isolate their primary fragger before mid-round structure forms.",
                primary_failure_condition:
                    "Allowing early multi-kill openings that unlock momentum-driven executes.",
                recommended_posture: "PRESSURE"
            }
        },

        {
            type: "map_veto",
            title: "Map Veto & Picks",
            confidence: 0.72,
            data: {
                decisions: [
                    {
                        map_name: "Bind",
                        decision: "BAN",
                        reasoning:
                            "Consistent defensive collapses under early pressure make this map unstable for controlled play.",
                        confidence: 0.7
                    },
                    {
                        map_name: "Haven",
                        decision: "BAN",
                        reasoning:
                            "Weak cross-site coordination leads to low retake success in mid-round scenarios.",
                        confidence: 0.68
                    },
                    {
                        map_name: "Icebox",
                        decision: "PICK",
                        reasoning:
                            "Linear site executions allow us to punish predictable defensive positioning.",
                        confidence: 0.75
                    }
                ]
            }
        },

        {
            type: "agent_tendencies",
            title: "Agent Tendencies",
            confidence: 0.83,
            data: {
                core_agents: ["Jett", "Chamber", "Raze"],
                predictability: "MEDIUM",
                what_breaks_if_countered:
                    "Their round flow collapses when primary duelists are denied early space and forced into late decisions."
            }
        },

        {
            type: "target_priority",
            title: "Target Priority",
            confidence: 0.86,
            data: {
                primary_target: {
                    nickname: "Timotino",
                    reasoning:
                        "Primary carry and emotional momentum driver. Early shutdown significantly reduces team effectiveness."
                },
                secondary_target: {
                    nickname: "Vora",
                    reasoning:
                        "Fallback fragger when pressure mounts. Slower reactions under coordinated utility."
                },
                avoid_duels_against: [
                    {
                        player: "Asuna",
                        reason:
                            "Thrives in isolated dry duels and converts space aggressively when unchecked."
                    }
                ]
            }
        },

        {
            type: "practice_plan",
            title: "Practice Plan",
            confidence: 0.8,
            data: {
                themes: [
                    {
                        name: "Opening Duel Denial",
                        description:
                            "Rehearse layered utility and double-peek protocols to deny first-contact advantages."
                    },
                    {
                        name: "Carry Isolation",
                        description:
                            "Drill fast information reads and collapse timings to isolate Timotino before trades develop."
                    },
                    {
                        name: "Punish Predictable Compositions",
                        description:
                            "Mid-round adaptations against Jett/Chamber defaults using delayed flanks and utility traps."
                    }
                ]
            }
        },

        {
            type: "adjustment_triggers",
            title: "Live Adjustment Triggers",
            confidence: 0.74,
            data: {
                triggers: [
                    {
                        signal: "Opponent secures first blood in three consecutive rounds",
                        action:
                            "Slow default pace and stack early utility denial on entry lanes.",
                        reasoning:
                            "Indicates confidence spike in opening duel patterns."
                    },
                    {
                        signal: "Timotino achieves multi-kill rounds twice in a half",
                        action:
                            "Shift to early information plays and targeted utility usage.",
                        reasoning:
                            "Carry snowball must be broken immediately."
                    },
                    {
                        signal: "Opponent wins pistol with aggressive pushes",
                        action:
                            "Force tempo on anti-eco rounds to punish overextension.",
                        reasoning:
                            "Aggression is likely to continue without discipline."
                    }
                ]
            }
        }
    ]
};

export default coachMock;
