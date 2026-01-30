import os
MODEL_NAME = "gemini-2.5-flash"
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION")

from pathlib import Path
import pandas as pd
import logging
from typing import AsyncGenerator
from typing_extensions import override

from google.adk.agents import BaseAgent, LlmAgent, ParallelAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types
from .sub_agents.AnalystAgent import analyst_visual_llm
from .sub_agents.CoachAgent import coach_visual_llm
from .sub_agents.PlayerAgent import opponent_visual_llm
from .sub_agents.ManagerAgent import manager_visual_llm


logger = logging.getLogger(__name__)
from pathlib import Path



class TeamStatsAnalyzerAgent(BaseAgent):
    """
    Performs CSV-derived analysis, then runs stakeholder LLMs in parallel.
    """

    coach_visual_llm: LlmAgent 
    analyst_visual_llm: LlmAgent
    manager_visual_llm: LlmAgent
    opponent_visual_llm: LlmAgent

    stakeholder_parallel: ParallelAgent

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        coach_visual_llm: LlmAgent,
        analyst_visual_llm: LlmAgent,
        manager_visual_llm: LlmAgent,
        opponent_visual_llm: LlmAgent,
    ):
        # 🔹 Create the parallel agent FIRST
        stakeholder_parallel = ParallelAgent(
            name="StakeholderParallelAnalysis",
            sub_agents=[
                coach_visual_llm,
                analyst_visual_llm,
                manager_visual_llm,
                opponent_visual_llm,
            ],
        )

        # 🔹 Register everything with BaseAgent
        super().__init__(
            name=name,
            coach_visual_llm=coach_visual_llm,
            analyst_visual_llm=analyst_visual_llm,
            manager_visual_llm=manager_visual_llm, 
            opponent_visual_llm=opponent_visual_llm,
            stakeholder_parallel=stakeholder_parallel,
            sub_agents=[
                stakeholder_parallel, 
            ],
        )

    # ─────────────────────────────────────────────
    # Helper
    # ─────────────────────────────────────────────
    def _save_df(self, df: pd.DataFrame, filename: str):
        output_dir = Path("app/scouting_outputs")
        output_dir.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_dir / filename, index=False)

    def _num(self, x):
        try:
            return float(x)
        except Exception:
            return None

    # 1️⃣ Team aggregate stats (Improved Form Logic)
    def _analyze_team_stats(self, path: Path) -> dict:
        df = pd.read_csv(path)
        metrics = dict(zip(df["metric"], df["value"]))

        wins_pct = self._num(metrics.get("wins_percentage"))
        w_streak = self._num(metrics.get("wins_streak_current"))
        l_streak = self._num(metrics.get("losses_streak_current"))

        # Enhanced Form Logic: Considering streaks + win rate
        if wins_pct >= 65 and w_streak >= 3:
            form = "on_fire"
        elif wins_pct >= 65:
            form = "dominant"
        elif wins_pct >= 50:
            form = "stable"
        elif l_streak >= 3:
            form = "slumping"
        else:
            form = "inconsistent"

        return {
            "series_count": int(self._num(metrics.get("series_count"))),
            "games_played": int(self._num(metrics.get("games_played"))),
            "kills_avg": self._num(metrics.get("kills_avg")),
            "wins_pct": wins_pct,
            "wins_streak": int(w_streak),
            "losses_streak": int(l_streak),
            "form": form,
        }

    # 2️⃣ Series overview (Added Team Filtering)
    def _analyze_series_overview(self, path: Path, team_name: str) -> dict:
        df = pd.read_csv(path)

        team_df = df[df["team"] == team_name]

        if team_df.empty:
            result = {
                "team_name": team_name,
                "total_series": 0,
                "win_rate": 0,
                "wins": 0,
                "losses": 0,
                "error": f"No data found for team: {team_name}",
            }
        else:
            wins = int(team_df["won"].sum())
            total = len(team_df)

            result = {
                "team_name": team_name,
                "total_series": int(team_df["series_id"].nunique()),
                "win_rate": round((wins / total) * 100, 2) if total > 0 else 0,
                "wins": wins,
                "losses": total - wins,
            }

        # 🔥 Convert → DataFrame → Save CSV
        result_df = pd.DataFrame([result])
        self._save_df(result_df, "series_overview.csv")

        # ✅ Return dict for LLM usage
        return result


    # 3️⃣ Per-game per-player stats (Added KDA & Filtering)
    def _analyze_game_player_stats(self, path: Path, team_name: str) -> dict:
        df = pd.read_csv(path)
        
        # Filter for the specific team to avoid counting opponent kills
        team_df = df[df["team"] == team_name]

        if team_df.empty:
            return {}

        # Calculate true KDA: (Kills + Assists) / Deaths
        total_k = team_df["kills"].sum()
        total_d = team_df["deaths"].sum()
        total_a = team_df["assists"].sum()
        kda = (total_k + total_a) / max(1, total_d)

        return {
            "avg_kills_per_game": team_df["kills"].mean(),
            "avg_deaths_per_game": team_df["deaths"].mean(),
            "avg_assists_per_game": team_df["assists"].mean(),
            "team_kda": round(kda, 2),
            "first_kill_rate": team_df["first_kill"].mean() * 100,
            "top_agents": (
                team_df.groupby("agent")["kills"]
                .mean()
                .sort_values(ascending=False)
                .head(3)
                .to_dict()
            ),
        }

    # 4️⃣ Team segment stats (Fixed Weighted Average Error)
    def _analyze_team_segments(self, path: Path) -> dict:
        df = pd.read_csv(path)

        # Weighted Average: deaths_sum / total_rounds
        def weighted_avg_deaths(group):
            return group["deaths_sum"].sum() / group["count"].sum()

        segments = {}
        for seg_type, group in df.groupby("segment_type"):
            segments[seg_type] = {
                "total_rounds": int(group["count"].sum()),
                "true_deaths_avg": round(weighted_avg_deaths(group), 3)
            }
        
        rows = []
        for seg_type, data in segments.items():
            rows.append({
                "segment_type": seg_type,
                **data
            })

        df_out = pd.DataFrame(rows)
        self._save_df(df_out, "team_segments.csv")

        return segments

    # 5️⃣ Player aggregate stats (Filtered Coaches/Inactive)
    def _analyze_player_stats(self, path: Path) -> dict:
        df = pd.read_csv(path)

        # Remove coaches/inactive players (those with 0 games played)
        active_players = df[df["games_played"] > 0].copy()

        top_players = (
            active_players.sort_values("kills_avg", ascending=False)
            .head(5)[
                ["nickname", "kills_avg", "win_percentage", "series_count", "games_played"]
            ]
        )

        self._save_df(top_players, "player_stats.csv")

        return top_players.to_dict(orient="records")

    # 6️⃣ Player segment stats (Fixed Weighted Average)
    def _analyze_player_segments(self, path: Path) -> dict:
        df = pd.read_csv(path)
        
        # Filter out 0-count entries to avoid division by zero
        df = df[df["count"] > 0]

        results = {}
        for (name, seg), group in df.groupby(["nickname", "segment_type"]):
            if name not in results:
                results[name] = {}
            
            # Accurate weighted average calculation
            results[name][seg] = {
                "deaths_avg": round(group["deaths_sum"].sum() / group["count"].sum(), 3),
                "sample_size": int(group["count"].sum())
            }
            
        rows = []

        for player, segs in results.items():
            for seg_type, data in segs.items():
                rows.append({
                    "player": player,
                    "segment_type": seg_type,
                    **data
        })

        df_out = pd.DataFrame(rows)
        self._save_df(df_out, "player_segments.csv")

        return results

    
    # 7️⃣ EXPLOITABLE WEAKNESS DETECTION
    def _detect_exploitable_weaknesses(self, derived: dict) -> dict:
        """
        Cross-reference metrics to find concrete weaknesses
        """
        weaknesses = []
        
        # Weakness 1: Post-pistol collapse
        team_stats = derived.get("team_stats", {})
        team_segments = derived.get("team_segments", {})
        
        if "pistol" in team_segments and "bonus" in team_segments:
            pistol_deaths = team_segments["pistol"].get("true_deaths_avg", 0)
            bonus_deaths = team_segments["bonus"].get("true_deaths_avg", 0)
            
            if bonus_deaths > pistol_deaths * 1.3:  # 30% worse after pistol loss
                weaknesses.append({
                    "type": "post_pistol_collapse",
                    "severity": "high",
                    "metric": f"Deaths increase {((bonus_deaths/pistol_deaths - 1) * 100):.1f}% in bonus rounds",
                    "exploit": "Force bonus rounds after winning pistol - they struggle to stabilize"
                })
        
        # Weakness 2: Player dependency
        player_stats = derived.get("player_stats", [])
        if len(player_stats) >= 2:
            top_player = player_stats[0]
            second_player = player_stats[1]
            
            kda_gap = top_player.get("kills_avg", 0) - second_player.get("kills_avg", 0)
            if kda_gap > 5:  # Heavy carry dependency
                weaknesses.append({
                    "type": "carry_dependency",
                    "severity": "medium",
                    "metric": f"Top fragger ({top_player['nickname']}) averages {kda_gap:.1f} more kills than #2",
                    "exploit": f"Shut down {top_player['nickname']} early - team lacks secondary firepower"
                })
        
        # Weakness 3: Side imbalance
        game_stats = derived.get("game_player_stats", {})
        if "first_kill_rate" in game_stats:
            first_kill = game_stats["first_kill_rate"]
            if first_kill < 40:  # Weak opening duels
                weaknesses.append({
                    "type": "weak_opening_duels",
                    "severity": "high",
                    "metric": f"Only {first_kill:.1f}% first-kill rate",
                    "exploit": "Play aggressive early - they lose opening duels consistently"
                })
        
        df_out = pd.DataFrame(
            weaknesses,
            columns=["type", "severity", "metric", "exploit"]
        )

        self._save_df(df_out, "exploitable_weaknesses.csv")

        return {
            "weaknesses": weaknesses,
            "total_exploits": len(weaknesses),
        }
    
    # 8️⃣ THREAT LEVEL CALCULATION
    def _calculate_threat_level(self, derived: dict) -> dict:
        """
        Quantify how dangerous this opponent is
        """
        team_stats = derived.get("team_stats", {})
        series_overview = derived.get("series_overview", {})
        
        # Scoring system (0-100)
        threat_score = 0
        
        # Win rate component (0-40 points)
        win_pct = team_stats.get("wins_pct", 0)
        threat_score += (win_pct / 100) * 40
        
        # Form component (0-30 points)
        form = team_stats.get("form", "stable")
        form_scores = {
            "on_fire": 30,
            "dominant": 25,
            "stable": 15,
            "inconsistent": 10,
            "slumping": 5
        }
        threat_score += form_scores.get(form, 15)
        
        # Sample size reliability (0-15 points)
        games = team_stats.get("games_played", 0)
        if games >= 15:
            threat_score += 15
        elif games >= 10:
            threat_score += 10
        else:
            threat_score += 5
        
        # Recent momentum (0-15 points)
        win_streak = team_stats.get("wins_streak", 0)
        loss_streak = team_stats.get("losses_streak", 0)
        
        if win_streak >= 3:
            threat_score += 15
        elif loss_streak >= 3:
            threat_score -= 10  # Lower threat if slumping
        else:
            threat_score += 7
        
        # Categorize
        if threat_score >= 80:
            level = "CRITICAL"
        elif threat_score >= 60:
            level = "HIGH"
        elif threat_score >= 40:
            level = "MEDIUM"
        else:
            level = "LOW"
        
        result = {
            "threat_level": level,
            "threat_score": round(threat_score, 1),
            "reasoning": f"Win%: {win_pct:.1f}%, Form: {form}, Streak: {win_streak}W/{loss_streak}L",
        }

        df_out = pd.DataFrame([result])
        self._save_df(df_out, "threat_assessment.csv")

        return result
    
    # 9️⃣ AGENT POOL ANALYSIS (VALORANT-specific)
    def _analyze_agent_diversity(self, derived: dict) -> dict:
        """
        Detect if opponent has limited agent pool (predictable)
        """
        game_stats = derived.get("game_player_stats", {})
        top_agents = game_stats.get("top_agents", {})
        
        if not top_agents:
            return {"diversity": "unknown", "predictability": "unknown"}
        
        # Calculate concentration (Herfindahl index)
        total_kills = sum(top_agents.values())
        if total_kills == 0:
            return {"diversity": "unknown", "predictability": "unknown"}
        
        concentration = sum((kills/total_kills)**2 for kills in top_agents.values())
        
        # Interpret
        if concentration > 0.5:  # Heavy reliance on 1-2 agents
            diversity = "low"
            predictability = "high"
            exploit = f"Agent pool concentrated: {list(top_agents.keys())[:2]} - ban/counter these"
        elif concentration > 0.33:
            diversity = "medium"
            predictability = "medium"
            exploit = "Moderate agent flexibility - prepare for top 3 agents"
        else:
            diversity = "high"
            predictability = "low"
            exploit = "Diverse agent pool - harder to predict compositions"
        
        result = {
            "diversity": diversity,
            "predictability": predictability,
            "concentration_index": round(concentration, 2),
            "exploitation_advice": exploit,
        }

        df_out = pd.DataFrame([result])
        self._save_df(df_out, "agent_pool_analysis.csv")

        # Top agents CSV
        top_agents_df = pd.DataFrame({
            "agent": top_agents.keys(),
            "kills": top_agents.values(),
        })
        self._save_df(top_agents_df, "agent_pool_top_agents.csv")

        return {
            **result,
            "top_3_agents": list(top_agents.keys())[:3]
        }
    
    # 🔟 PLAYER VOLATILITY ANALYSIS
    def _analyze_player_volatility(self, derived: dict) -> dict:
        """
        Identify inconsistent players (tilt-prone or high-variance)
        """
        player_segments = derived.get("player_segments", {})
        volatile_players = []
        
        for player_name, segments in player_segments.items():
            if len(segments) < 2:  # Need multiple segments to measure variance
                continue
            
            death_avgs = [seg["deaths_avg"] for seg in segments.values() if "deaths_avg" in seg]
            
            if len(death_avgs) >= 2:
                import statistics
                std_dev = statistics.stdev(death_avgs)
                mean_deaths = statistics.mean(death_avgs)
                
                # Coefficient of variation
                cv = (std_dev / mean_deaths) if mean_deaths > 0 else 0
                
                if cv > 0.4:  # High variance = inconsistent
                    volatile_players.append({
                        "player": player_name,
                        "volatility_index": round(cv, 2),
                        "avg_deaths": round(mean_deaths, 2),
                        "std_dev": round(std_dev, 2),
                        "interpretation": "High-variance player - may tilt or pop off unpredictably"
                    })
        
        df_out = pd.DataFrame(volatile_players)
        self._save_df(df_out, "player_volatility.csv")
        
        return {
            "volatile_players": sorted(volatile_players, key=lambda x: x["volatility_index"], reverse=True),
            "count": len(volatile_players)
        }

    def _build_opponent_map_df(self, path: Path) -> pd.DataFrame:
        df = pd.read_csv(path)

        base = df[["series_id", "game_id", "team"]].drop_duplicates()

        base["opponent"] = (
            base.groupby(["series_id", "game_id"])["team"]
            .transform(lambda x: x.iloc[::-1].values)
        )

        return base
    
    def _build_player_vs_opponent_df(self, path: Path) -> pd.DataFrame:
        df = pd.read_csv(path)

        opp = self._build_opponent_map_df(path)

        merged = df.merge(
            opp,
            on=["series_id", "game_id", "team"],
            how="left"
        )

        return (
            merged.groupby(["player_name", "opponent", "map_name"])
            .agg(
                games=("game_id", "nunique"),
                avg_kills=("kills", "mean"),
                avg_deaths=("deaths", "mean"),
                first_kill_rate=("first_kill", "mean")
            )
            .reset_index()
        )

    def _build_team_map_loss_df(self, path: Path, team_name: str) -> pd.DataFrame:
        df = pd.read_csv(path)

        team_df = df[df["team"] == team_name]

        return (
            team_df.groupby("map_name")
            .agg(
                games=("game_id", "nunique"),
                deaths=("deaths", "sum"),
                kills=("kills", "sum")
            )
            .reset_index()
        )
    
    def _build_player_entry_df(self, path: Path) -> pd.DataFrame:
        df = pd.read_csv(path)

        return (
            df.groupby(["player_name", "map_name"])
            .agg(
                entry_attempts=("first_kill", "count"),
                entry_success_rate=("first_kill", "mean")
            )
            .reset_index()
        )
    
    def _build_player_death_heatmap_df(self, path: Path) -> pd.DataFrame:
        df = pd.read_csv(path)

        return df[df["position_x"].notnull()][
            ["player_name", "map_name", "position_x", "position_y"]
        ]


    def _debug_print_state(self, state: dict, df_rows: int = 5):
        print("\n" + "=" * 80)

        # ─────────────────────────────
        # HIGH-LEVEL ANALYTICS
        # ─────────────────────────────
        print("📊 TEAM STATS")
        print(state.get("team_stats"))

        print("\n📈 SERIES OVERVIEW")
        print(state.get("series_overview"))

        print("\n🎯 GAME PLAYER STATS")
        print(state.get("game_player_stats"))

        print("\n🧩 TEAM SEGMENTS")
        print(state.get("team_segments"))

        print("\n👥 PLAYER STATS (Top Players)")
        for p in state.get("player_stats", []):
            print(p)

        print("\n📊 PLAYER SEGMENTS (sample)")
        player_segments = state.get("player_segments", {})
        if player_segments:
            first_player = next(iter(player_segments))
            print({first_player: player_segments[first_player]})

        print("\n🚨 EXPLOITABLE WEAKNESSES")
        print(state.get("exploitable_weaknesses"))

        print("\n⚠️ THREAT ASSESSMENT")
        print(state.get("threat_assessment"))

        print("\n🎭 AGENT POOL ANALYSIS")
        print(state.get("agent_pool_analysis"))

        print("\n📉 PLAYER VOLATILITY")
        print(state.get("player_volatility"))

        # ─────────────────────────────
        # DATAFRAMES (EXPLICIT, NO .items())
        # ─────────────────────────────
        print("\n" + "-" * 80)
        print("📂 GENERATED DATAFRAMES")
        print("-" * 80)

        df_keys = [
            "df_raw_game_level",
            "df_match_results",
            "df_map_team_performance",
            "df_player_vs_team",
            "df_first_duels",
            "df_player_time_series",
            "df_opponents",
            "df_player_vs_opponent",
            "df_team_map_losses",
            "df_player_entries",
            "df_player_death_heatmap",
        ]

        for key in df_keys:
            df = state.get(key)
            if df is None:
                continue

            print(f"\n🧾 {key}")
            print(f"Shape   : {df.shape}")
            print(f"Columns : {list(df.columns)}")
            print(f"Head ({df_rows} rows):")
            print(df.head(df_rows))

        print("\n" + "=" * 80 + "\n")



    # ─────────────────────────────────────────────
    # Main execution
    # ─────────────────────────────────────────────
    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:

        scouting_csvs = ctx.session.state.get("scouting_csvs")
        if not scouting_csvs:
            yield Event(
                author=self.name,
                content=types.Content(
                    role="assistant",
                    parts=[types.Part(text="Scouting CSVs not found in session state.")]
                )
            )
            return

        logger.info(f"[{self.name}] Running full CSV analysis")

        state = ctx.session.state

        state["team_stats"] = self._analyze_team_stats(
            Path(scouting_csvs["team_stats"])
        )

        state["series_overview"] = self._analyze_series_overview(
            Path(scouting_csvs["series_overview"]),
            state.get("team_name")
        )

        state["game_player_stats"] = self._analyze_game_player_stats(
            Path(scouting_csvs["series_game_player_stats"]),
            state.get("team_name")
        )

        state["team_segments"] = self._analyze_team_segments(
            Path(scouting_csvs["team_segment_stats"])
        )

        state["player_stats"] = self._analyze_player_stats(
            Path(scouting_csvs["player_stats"])
        )

        state["player_segments"] = self._analyze_player_segments(
            Path(scouting_csvs["player_segment_stats"])
        )
        state["exploitable_weaknesses"] = self._detect_exploitable_weaknesses({
            "team_stats": state["team_stats"],
            "team_segments": state["team_segments"],
            "player_stats": state["player_stats"],
            "game_player_stats": state["game_player_stats"],
        })

        state["threat_assessment"] = self._calculate_threat_level({
            "team_stats": state["team_stats"],
            "series_overview": state["series_overview"],
        })

        state["agent_pool_analysis"] = self._analyze_agent_diversity({
            "game_player_stats": state["game_player_stats"]
        })

        state["player_volatility"] = self._analyze_player_volatility({
            "player_segments": state["player_segments"]
        })

        # ─────────────────────────────────────────
        # 🧠 Advanced Opponent & Player Intelligence
        # ─────────────────────────────────────────

        state["df_opponents"] = self._build_opponent_map_df(
            Path(scouting_csvs["series_game_player_stats"])
        )

        state["df_player_vs_opponent"] = self._build_player_vs_opponent_df(
            Path(scouting_csvs["series_game_player_stats"])
        )

        state["df_team_map_losses"] = self._build_team_map_loss_df(
            Path(scouting_csvs["series_game_player_stats"]),
            state.get("team_name")
        )

        state["df_player_entries"] = self._build_player_entry_df(
            Path(scouting_csvs["series_game_player_stats"])
        )

        state["df_player_death_heatmap"] = self._build_player_death_heatmap_df(
            Path(scouting_csvs["series_game_player_stats"])
        )

        self._save_df(
                self._build_opponent_map_df(
                    Path(scouting_csvs["series_game_player_stats"])
                ),
                "df_opponents.csv"
            )

        self._save_df(
                self._build_player_vs_opponent_df(
                    Path(scouting_csvs["series_game_player_stats"])
                ),
                "df_player_vs_opponent.csv"
            )

        self._save_df(
                self._build_team_map_loss_df(
                    Path(scouting_csvs["series_game_player_stats"]),
                    state.get("team_name")
                ),
                "df_team_map_losses.csv"
            )

        self._save_df(
                self._build_player_entry_df(
                    Path(scouting_csvs["series_game_player_stats"])
                ),
                "df_player_entries.csv"
            )

        self._save_df(
                self._build_player_death_heatmap_df(
                    Path(scouting_csvs["series_game_player_stats"])
                ),
                "df_player_death_heatmap.csv"
            )

        

        # Flatten key team stats for LLM templates (optional convenience)
        state.update(state["team_stats"])

        REQUIRED_KEYS = [
            "team_stats",
            "series_overview",
            "game_player_stats",
            "team_segments",
            "player_stats",
            "player_segments",
            "exploitable_weaknesses",
            "threat_assessment",
            "agent_pool_analysis",
            "player_volatility",
        ]

        missing = [k for k in REQUIRED_KEYS if k not in state]

        if missing:
            logger.error(f"[{self.name}] Missing required state keys: {missing}")
            return

        self._debug_print_state(state)

        logger.info(f"[{self.name}] Running parallel stakeholder analyses")

        async for event in self.stakeholder_parallel.run_async(ctx):
            yield event

        logger.info(f"[{self.name}] All stakeholder analyses completed")

        print("TYPE:", type(ctx.session.state.get("player_visual_blocks")))
        print("VALUE:", ctx.session.state.get("player_visual_blocks"))


        yield Event(
            author=self.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text="All stakeholder analyses completed.")]
            )
        )

AnalyzerAgent = TeamStatsAnalyzerAgent(
    name="TeamStatsAnalyzerAgent",
    coach_visual_llm=coach_visual_llm,
    analyst_visual_llm=analyst_visual_llm,
    manager_visual_llm=manager_visual_llm,
    opponent_visual_llm=opponent_visual_llm,
)
