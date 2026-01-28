const opponentMock = {
    blocks: [
        {
            type: "performance_experience",
            title: "Performance Experience",
            confidence: 0.8,
            insights: [
                {
                    insight:
                        "Performance can feel volatile against opponents with a consistently high win rate.",
                    reason:
                        "The opponent holds a ~66.7% win rate across 6 series, which correlates with higher round-to-round variance against similarly strong teams.",
                    confidence: 0.7
                },
                {
                    insight:
                        "Early-round engagements can feel difficult to stabilize.",
                    reason:
                        "The opponent shows a first-kill success rate of only ~11.1%, indicating frequent early-round losses that distort round flow.",
                    confidence: 0.9
                }
            ]
        },
        {
            type: "stable_signals",
            title: "Stable Signals",
            confidence: 0.7,
            insights: [
                {
                    insight:
                        "Overall opponent performance remains steady across a meaningful sample.",
                    reason:
                        "Their win rate stays around ~67.5% over 40 games and 14 series, suggesting results are not driven by short-term variance.",
                    confidence: 0.8
                },
                {
                    insight:
                        "Individual deaths tend to stay within a narrow and predictable range.",
                    reason:
                        "Most players average between ~0.61 and ~0.71 deaths per round across approximately 866 rounds.",
                    confidence: 0.7
                }
            ]
        },
        {
            type: "pressure_fracture_points",
            title: "Pressure Fracture Points",
            confidence: 0.9,
            insights: [
                {
                    insight:
                        "Opening duels represent a recurring pressure fracture point.",
                    reason:
                        "A first-kill rate of ~11.1% is flagged as a high-severity exploit, indicating repeated early-round disadvantages.",
                    confidence: 0.9
                },
                {
                    insight:
                        "Performance degrades when early engagements are repeatedly lost.",
                    reason:
                        "The same opening-duel weakness appears consistently across series rather than isolated matches.",
                    confidence: 0.8
                }
            ]
        },
        {
            type: "consistency_windows",
            title: "Consistency Windows",
            confidence: 0.7,
            insights: [
                {
                    insight:
                        "Consistency improves when the opponent secures early momentum.",
                    reason:
                        "In matches where they convert early advantages, their win rate remains near ~67.5% across a large sample.",
                    confidence: 0.8
                },
                {
                    insight:
                        "Instability increases when early duels are lost repeatedly.",
                    reason:
                        "High-severity opening-duel weaknesses amplify variance when early rounds swing negatively.",
                    confidence: 0.8
                }
            ]
        },
        {
            type: "player_self_checks",
            title: "Player Self-Checks",
            confidence: 0.8,
            insights: [
                {
                    insight:
                        "Does the opening of the round feel harder than usual?",
                    reason:
                        "The opponent converts first kills at only ~11.1%, creating frequent early-round chaos.",
                    confidence: 0.9
                },
                {
                    insight:
                        "Are deaths clustering more than expected in early phases?",
                    reason:
                        "Opponent player deaths typically sit between ~0.61–0.71 per round across ~866 rounds, setting a clear baseline.",
                    confidence: 0.7
                },
                {
                    insight:
                        "Do early losses make the match feel harder to recover?",
                    reason:
                        "Against teams winning ~67.5% of their games, recovery after early deficits becomes statistically less reliable.",
                    confidence: 0.8
                }
            ]
        }
    ]
};

export default opponentMock;
