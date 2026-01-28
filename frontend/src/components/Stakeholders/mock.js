const managerVisualBlocks = {
    blocks: [
        {
            type: "opponent_stability",
            title: "Opponent Stability Profile",
            confidence: 0.85,
            data: {
                stability_rating: "Structurally Stable",
                reasoning:
                    "The team exhibits a dominant form with a consistent win rate across a significant number of games and series, suggesting sustained performance rather than a short-term spike."
            }
        },
        {
            type: "dependency_profile",
            title: "Dependency Profile",
            confidence: 0.70,
            data: {
                dependency_type: "Functions as a system",
                top_dependency_share: 0.675,
                reasoning:
                    "Player win percentages closely mirror team results, indicating distributed responsibility rather than reliance on a single carry."
            }
        },
        {
            type: "risk_exposure",
            title: "Risk Exposure Signals",
            confidence: 0.75,
            data: {
                risk_type: "Potential pressure-related collapse",
                severity: "Medium",
                confidence: 0.70
            }
        },
        {
            type: "prep_cost",
            title: "Preparation Cost & Adaptability",
            confidence: 0.80,
            data: {
                prep_complexity: "Medium",
                adaptation_risk: "Low",
                reasoning:
                    "The opponent demonstrates moderate predictability with sufficient depth to adapt, requiring focused but not exhaustive preparation."
            }
        },
        {
            type: "exploit_sustainability",
            title: "Exploit Sustainability",
            confidence: 0.90,
            data: {
                exploit_type: "Weakness in opening engagements",
                sustainability: "High",
                confidence: 0.90
            }
        },
        {
            type: "management_summary",
            title: "Management Summary",
            confidence: 0.80,
            data: {
                primary_long_term_risk:
                    "Consistently strong performance suggests the opponent will remain a top-tier threat across future competitive cycles.",
                primary_weakness_self_correct:
                    "Opening engagement issues may improve with experience and structural adjustments.",
                monitoring_question:
                    "Does their performance stability persist when facing sustained pressure from top-tier opponents?"
            }
        }
    ]
};

export default managerVisualBlocks;
