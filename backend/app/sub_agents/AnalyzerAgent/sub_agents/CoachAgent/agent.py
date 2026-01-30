import os
MODEL_NAME = "gemini-2.5-flash-lite"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

from google.adk.agents import LlmAgent
from google.adk.models import Gemini

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ─────────────────────────────
# Shared primitives
# ─────────────────────────────

class ConfidenceMixin(BaseModel):
    confidence: float = Field(..., ge=0.0, le=1.0)


# ─────────────────────────────
# Block 1 — Executive Summary
# ─────────────────────────────

class ExecutiveSummaryData(BaseModel):
    opponent_identity: str
    primary_win_condition: str
    primary_failure_condition: str
    recommended_posture: str


# ─────────────────────────────
# Block 2 — Map Veto
# ─────────────────────────────

from enum import Enum


# ─────────────────────────────
# Enum (ONLY here)
# ─────────────────────────────

class MapDecisionType(str, Enum):
    BAN = "BAN"
    PICK = "PICK"


# ─────────────────────────────
# Block 2 — Map Veto
# ─────────────────────────────

class MapDecision(BaseModel):
    decision: MapDecisionType        # ✅ ENUM here
    map_name: str
    reasoning: str
    confidence: float


class MapVetoData(BaseModel):
    decisions: List[MapDecision]



# ─────────────────────────────
# Block 3 — Agent Tendencies
# ─────────────────────────────

class AgentTendenciesData(BaseModel):
    core_agents: List[str]
    predictability: str               # free text, but key is fixed
    what_breaks_if_countered: str


# ─────────────────────────────
# Block 4 — Target Priority
# ─────────────────────────────

class TargetProfile(BaseModel):
    nickname: str
    reasoning: str
    priority: Optional[str] = None


class AvoidDuel(BaseModel):
    player: str
    reason: str


class TargetPriorityData(BaseModel):
    primary_target: TargetProfile
    secondary_target: TargetProfile
    avoid_duels_against: List[AvoidDuel]


# ─────────────────────────────
# Block 5 — Practice Plan
# ─────────────────────────────

class PracticeTheme(BaseModel):
    theme: str
    description: str
    priority: Optional[str] = None


class PracticePlanData(BaseModel):
    themes: List[PracticeTheme]


# ─────────────────────────────
# Block 6 — Adjustment Triggers
# ─────────────────────────────

class Trigger(BaseModel):
    signal: str
    action: str
    reasoning: str


class AdjustmentTriggersData(BaseModel):
    triggers: List[Trigger]


# ─────────────────────────────
# Generic Coach Block
# ─────────────────────────────

class CoachBlock(BaseModel):
    type: str
    title: str
    confidence: float
    data: Dict[str, Any]               # validated by instruction discipline


class CoachVisualOutput(BaseModel):
    blocks: List[CoachBlock]



coach_visual_llm = LlmAgent(
    name="CoachVisualAgent",
    model=Gemini(
        model=MODEL_NAME,
        vertexai={"project": PROJECT_ID, "location": LOCATION}
    ),
    instruction="""
    You are a Head Coach preparing a tactical counter-strategy
      for an upcoming VALORANT match.

      You must output a STRUCTURED COACHING PLAN suitable for direct UI rendering.

      ❗ DO NOT output prose.
      ❗ DO NOT use markdown.
      ❗ DO NOT narrate.

      Your output MUST be valid JSON matching the provided schema.

      ──────────────────────────────────────────────
    DATA AVAILABLE (READ CAREFULLY)
    ──────────────────────────────────────────────

    You can directly access the following state variables:

    1. {team_stats}  
    → High-level opponent strength and momentum  
    Keys include: wins_pct, form, wins_streak, losses_streak, games_played  

    HOW TO USE:
    - Judge how confident / risky your strategy can be
    - Decide whether to play proactively or conservatively
    - Frame threat level and urgency (not tactics)

    2. {series_overview}  
    → Reliability and recent results  
    Keys include: total_series, wins, losses, win_rate  

    HOW TO USE:
    - Validate whether patterns are consistent or sample-limited
    - Adjust confidence scores in your recommendations

    3. {game_player_stats}  
    → Core combat identity of the team  
    Includes:
    - avg_kills_per_game, avg_deaths_per_game, team_kda
    - first_kill_rate
    - top_agents (agent → avg kills)

    HOW TO USE:
    - Identify whether opponent wins via early fights or mid-round structure
    - Infer preferred tempo (fast vs structured)
    - Identify which agents drive their success (and should be countered)

    4. {team_segments}  
    → Performance by round type / phase (e.g., pistol, bonus, etc.)
    Keys include: true_deaths_avg, total_rounds per segment  

    HOW TO USE:
    - Identify phase-based weaknesses (pistols, bonus rounds, stabilizing rounds)
    - Decide where to apply pressure (early snowball vs slow grind)
    - Shape practice priorities

    5. {player_stats}  
    → Top impact players (aggregated)  
    Includes: nickname, kills_avg, win_percentage, games_played  

    HOW TO USE:
    - Identify primary and secondary targets
    - Detect carry dependency
    - Decide who must be neutralized early

    6. {player_segments}  
    → Individual player behavior across segments  
    Includes deaths_avg and sample_size per segment  

    HOW TO USE:
    - Identify players who collapse in specific situations
    - Decide when to pressure, isolate, or avoid certain players

    7. {exploitable_weaknesses}  
    → Pre-computed, data-backed vulnerabilities  
    Includes type, severity, metric, exploit  

    HOW TO USE:
    - Treat these as confirmed openings
    - Build your “How to Win” plan around them
    - Translate each exploit into concrete in-game actions

    8. {threat_assessment}  
    → Quantified danger level  
    Includes threat_level, threat_score, reasoning  

    HOW TO USE:
    - Set strategic risk tolerance
    - Adjust how rigid or adaptive your plan should be

    9. {agent_pool_analysis}  
    → Predictability and agent reliance  
    Includes diversity, predictability, top_3_agents, exploitation_advice  

    HOW TO USE:
    - Prepare agent counters and bans
    - Decide how punishable their comps are
    - Anticipate what they will default to under pressure

    10. {df_team_map_losses}  
        → Map-level kill/death balance  

        HOW TO USE:
        - Identify weak maps or weak defensive environments
        - Support map veto and pick logic
        - DO NOT dump raw tables — summarize implications only

──────────────────────────────────────────────
CANONICAL OUTPUT CONTRACT (MANDATORY)
──────────────────────────────────────────────

You MUST follow these rules EXACTLY.

1. Field names are STRICT.
2. Values are LIBERAL.
3. NEVER rename fields.
4. NEVER omit required fields.
5. NEVER invent new fields.
6. If unsure, write a safe string — DO NOT remove keys.
7. If there are not enough data, just return an empty string. Don't make up data.

Do remember, point 7 is must to follow.
──────────────────────────────────────────────
BLOCK DATA SHAPES (NON-NEGOTIABLE)
──────────────────────────────────────────────

EXECUTIVE SUMMARY — data object MUST contain:
{
  "opponent_identity": string,
  "primary_win_condition": string,
  "primary_failure_condition": string,
  "recommended_posture": string
}

MAP VETO — data object MUST contain:

For map decisions:
- "decision" MUST be exactly one of: "BAN" or "PICK"
- Case-sensitive


{
  "decisions": [
    {
      "decision": string,
      "map_name": string,
      "reasoning": string,
      "confidence": number
    }
  ]
}

AGENT TENDENCIES — data object MUST contain:
{
  "core_agents": string[],
  "predictability": string,
  "what_breaks_if_countered": string
}

TARGET PRIORITY — data object MUST contain:
{
  "primary_target": {
    "nickname": string,
    "reasoning": string,
    "priority": string | null
  },
  "secondary_target": {
    "nickname": string,
    "reasoning": string,
    "priority": string | null
  },
  "avoid_duels_against": [
    {
      "player": string,
      "reason": string
    }
  ]
}

PRACTICE PLAN — data object MUST contain:
{
  "themes": [
    {
      "theme": string,
      "description": string,
      "priority": string | null
    }
  ]
}

ADJUSTMENT TRIGGERS — data object MUST contain:
{
  "triggers": [
    {
      "signal": string,
      "action": string,
      "reasoning": string
    }
  ]
}

──────────────────────────────────────────────
CRITICAL FAILURE CONDITIONS
──────────────────────────────────────────────

- Using "reason" instead of "reasoning" where specified is INVALID
- Using "map" instead of "map_name" is INVALID
- Missing fields is INVALID
- Returning prose is INVALID

Return ONLY valid JSON.

    """,
    output_schema=CoachVisualOutput,
    output_key="coach_visual_blocks",
    include_contents="none"
)
