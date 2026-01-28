const simulationMock = {
    scenarios: [
        {
            scenario:
                "The opponent converts a strong early-round advantage into a decisive series win.",
            likelihood: 0.65,
            quantitative_basis:
                "Opponent holds a 67.5% series win rate while showing only 11.11% opening-duel success, indicating strong conversion once ahead.",
            primary_driver: "early_round_instability",
            winning_lever:
                "Denying opponent early-round advantage from converting into map control"
        },
        {
            scenario:
                "The opponent absorbs early losses and wins through superior mid-to-late round structure.",
            likelihood: 0.55,
            quantitative_basis:
                "Sustained 67.5% win rate across 14 series reflects strong recovery patterns.",
            primary_driver: "system_stability",
            winning_lever:
                "Preventing opponent from stabilizing after early-round losses"
        },
        {
            scenario:
                "The opponent benefits from a high-variance match with repeated momentum swings.",
            likelihood: 0.45,
            quantitative_basis:
                "Tight deaths-per-round distribution combined with known pressure fracture points.",
            primary_driver: "volatility",
            winning_lever:
                "Maintaining consistency across momentum swings to limit opponent volatility gains"
        },
        {
            scenario:
                "The opponent dictates tempo uncontested and closes the match cleanly.",
            likelihood: 0.35,
            quantitative_basis:
                "Structural stability paired with medium confidence in opponent weaknesses.",
            primary_driver: "adaptation_failure",
            winning_lever:
                "Disrupting opponent tempo control before late-round consolidation"
        },
        {
            scenario:
                "The opponent wins by enabling a single high-impact player to dominate key rounds.",
            likelihood: 0.30,
            quantitative_basis:
                "Top player contributes ~48.21% of total team impact, indicating dependency.",
            primary_driver: "system_dependency",
            winning_lever:
                "Reducing impact concentration from the opponent’s primary carry"
        }
    ]
};

export default simulationMock;
