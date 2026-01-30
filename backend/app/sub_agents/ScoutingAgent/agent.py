
import csv
import requests
from dotenv import load_dotenv; 
load_dotenv()
import asyncio
import aiohttp
from datetime import datetime
import json
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from typing import AsyncGenerator
from typing_extensions import override
from google.genai import types
import logging
import os

logger = logging.getLogger(__name__)


GRID_CENTRAL_DATA_URL = "https://api-op.grid.gg/central-data/graphql"
GRID_LIVE_DATA_FEED_URL = "https://api-op.grid.gg/live-data-feed/series-state/graphql"
GRID_STATISTICS_FEED_URL = "https://api-op.grid.gg/statistics-feed/graphql"
API_KEY = os.getenv("GRID_API_KEY")

# Process 1 : 
# Fetch GRID teamId by team name using paginated team list.

def get_team_id_by_name(target_team_name: str) -> str:
    """
    Fetch GRID teamId by team name using paginated team list.

    :param target_team_name: Team name to search for (e.g. "NRG")
    :return: teamId as string
    :raises RuntimeError: if team is not found
    """

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    after_cursor = None
    target_lower = target_team_name.lower()

    while True:
        query = f"""
        query GetTeams {{
          teams(first: 50{f', after: "{after_cursor}"' if after_cursor else ''}) {{
            pageInfo {{
              hasNextPage
              endCursor
            }}
            edges {{
              node {{
                id
                name
              }}
            }}
          }}
        }}
        """

        response = requests.post(
            GRID_CENTRAL_DATA_URL,
            headers=headers,
            json={"query": query},
            timeout=30
        )

        response.raise_for_status()
        payload = response.json()

        if "errors" in payload:
            raise RuntimeError(f"GraphQL error: {payload['errors']}")

        teams_data = payload["data"]["teams"]

        for edge in teams_data["edges"]:
            team = edge["node"]
            if team["name"].lower() == target_lower:
                return team["id"]

        # pagination
        if not teams_data["pageInfo"]["hasNextPage"]:
            break

        after_cursor = teams_data["pageInfo"]["endCursor"]

    raise RuntimeError(f"Team '{target_team_name}' not found in GRID database")


# Process 2 : 
# Fetch recent VALORANT esports series and filter by team name.

def get_recent_valorant_series_for_team(team_name: str, limit: int = 20) -> dict:
    """
    Fetch recent VALORANT esports series and filter by team name.

    :param team_name: Team name to filter for (e.g. "NRG")
    :param limit: Number of recent series to fetch from GRID
    :return: Filtered response matching GRID allSeries structure
    """

    if not API_KEY:
        raise RuntimeError("GRID_API_KEY not found in environment")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    query = f"""
    query GetRecentValorantSeries {{
      allSeries(
        first: {limit}
        filter: {{
          titleId: 6
          types: ESPORTS
        }}
        orderBy: StartTimeScheduled
        orderDirection: DESC
      ) {{
        edges {{
          node {{
            id
            startTimeScheduled
            tournament {{
              name
            }}
            teams {{
              baseInfo {{
                name
              }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        GRID_CENTRAL_DATA_URL,
        headers=headers,
        json={"query": query},
        timeout=30
    )

    response.raise_for_status()
    payload = response.json()

    if "errors" in payload:
        raise RuntimeError(f"GraphQL error: {payload['errors']}")

    target = team_name.lower()
    filtered_edges = []

    for edge in payload["data"]["allSeries"]["edges"]:
        teams = [
            t["baseInfo"]["name"].lower()
            for t in edge["node"]["teams"]
        ]
        if target in teams:
            filtered_edges.append(edge)

    # Return in the SAME structure you showed
    return {
        "data": {
            "allSeries": {
                "edges": filtered_edges
            }
        }
    }

#Process 3 : 
#Fetch series state data for a given series ID.

async def get_series_state_async(session, series_id: str) -> dict:
    """
    Fetch enriched VALORANT series state (agent, assists, economy, map).
    Backward-compatible with existing CSV writers.
    """

    query = f"""
    query GetSeriesState {{
      seriesState(id: "{series_id}") {{
        valid
        updatedAt
        started
        finished

        teams {{
          name
          won
        }}

        games {{
          id
          sequenceNumber
          duration

          map {{
            id
            name
          }}

          teams {{
            name
            won
            players {{
              id
              name

              character {{
                name
              }}

              kills
              deaths
              killAssistsGiven
              firstKill

              money
              loadoutValue
              netWorth

              position {{
                x
                y
              }}
            }}
          }}
        }}
      }}
    }}
    """

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    async with session.post(
        GRID_LIVE_DATA_FEED_URL,
        headers=headers,
        json={"query": query}
    ) as resp:
        payload = await resp.json()

    if "errors" in payload:
        raise RuntimeError(payload["errors"])

    return payload["data"]["seriesState"]



#Process 4 : 
#Fetch Team Stats based on last 6 months followed by all its series.

def get_team_stats_last_6_months(team_id: str) -> dict:
    """
    Fetch aggregated team statistics for the last 6 months.

    :param team_id: GRID team ID
    :return: teamStatistics response
    """

    if not API_KEY:
        raise RuntimeError("GRID_API_KEY not found in environment")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    query = f"""
    query TeamStatisticsForLastSixMonths {{
      teamStatistics(
        teamId: "{team_id}"
        filter: {{ timeWindow: LAST_6_MONTHS }}
      ) {{
        id
        aggregationSeriesIds
        series {{
          count
          kills {{
            sum
            min
            max
            avg
          }}
        }}
        game {{
          count
          won {{
            value
            count
            percentage
            streak {{
              min
              max
              current
            }}
          }}
        }}
        segment {{
          type
          count
          deaths {{
            sum
            min
            max
            avg
          }}
        }}
      }}
    }}
    """

    response = requests.post(
        GRID_STATISTICS_FEED_URL,
        headers=headers,
        json={"query": query},
        timeout=60
    )

    response.raise_for_status()
    payload = response.json()

    if "errors" in payload:
        raise RuntimeError(f"GraphQL error: {payload['errors']}")

    return payload["data"]["teamStatistics"]


#Process 5: 
#Fetch full roster (players) for a given team.

def get_team_roster(team_id: str) -> list[dict]:
    """
    Fetch full roster (players) for a given team.

    :param team_id: GRID team ID
    :return: List of player dicts [{id, nickname, title}]
    """

    
    if not API_KEY:
        raise RuntimeError("GRID_API_KEY not found in environment")

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    after_cursor = None
    players = []

    while True:
        query = f"""
        query GetTeamRoster {{
          players(
            filter: {{ teamIdFilter: {{ id: "{team_id}" }} }}
            first: 50
            {f'after: "{after_cursor}"' if after_cursor else ""}
          ) {{
            edges {{
              node {{
                id
                nickname
                title {{
                  name
                }}
              }}
            }}
            pageInfo {{
              hasNextPage
              endCursor
            }}
          }}
        }}
        """

        response = requests.post(
            GRID_CENTRAL_DATA_URL,
            headers=headers,
            json={"query": query},
            timeout=60
        )

        response.raise_for_status()
        payload = response.json()

        if "errors" in payload:
            raise RuntimeError(f"GraphQL error: {payload['errors']}")

        data = payload["data"]["players"]

        for edge in data["edges"]:
            players.append(edge["node"])

        if not data["pageInfo"]["hasNextPage"]:
            break

        after_cursor = data["pageInfo"]["endCursor"]

    return players

#Process 6: 
#Fetch Each Player Stats

async def get_player_stats_last_6_months_async(session, player_id: str) -> dict:
    query = f"""
    query PlayerStatisticsForLastSixMonths {{
      playerStatistics(
        playerId: "{player_id}"
        filter: {{ timeWindow: LAST_6_MONTHS }}
      ) {{
        id
        aggregationSeriesIds
        series {{
          count
          kills {{
            sum
            min
            max
            avg
          }}
        }}
        game {{
          count
          won {{
            value
            count
            percentage
            streak {{
              min
              max
              current
            }}
          }}
        }}
        segment {{
          type
          count
          deaths {{
            sum
            min
            max
            avg
          }}
        }}
      }}
    }}
    """

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    async with session.post(
        GRID_STATISTICS_FEED_URL,
        headers=headers,
        json={"query": query},
        timeout=60
    ) as resp:
        payload = await resp.json()

    if "errors" in payload:
        raise RuntimeError(payload["errors"])

    return payload["data"]["playerStatistics"]

#Process 7: 
#to save the data in csv format

from pathlib import Path
import csv


def save_scouting_report_csv(
    team_name: str,
    series_ids: list,
    series_states: dict,
    team_stats_last_6_months: dict,
    team_roster: list,
    player_stats_last_6_months: dict,
):
    """
    Save scouting data into multiple structured CSV files
    under project_root/scouting_outputs/ and return their paths.
    """

    # project_root/scouting_outputs
    output_dir = Path(__file__).resolve().parents[2] / "scouting_outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    csv_paths = {}

    # ───────────────────────────────────────────────────────
    # 1️⃣ Series overview
    # ───────────────────────────────────────────────────────
    path = output_dir / "series_overview.csv"
    csv_paths["series_overview"] = str(path)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["series_id", "valid", "started", "finished", "updated_at", "team", "won"])

        for sid in series_ids:
            state = series_states.get(sid)
            if not state:
                continue

            for t in state["teams"]:
                writer.writerow([
                    sid,
                    state["valid"],
                    state["started"],
                    state["finished"],
                    state["updatedAt"],
                    t["name"],
                    t["won"]
                ])

    # ───────────────────────────────────────────────────────
    # 2️⃣ Per-game, per-player stats
    # ───────────────────────────────────────────────────────
    path = output_dir / "series_game_player_stats.csv"
    csv_paths["series_game_player_stats"] = str(path)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "series_id", "game_id", "sequence_number", "map_name",
            "team", "player_id", "player_name", "agent",
            "kills", "deaths", "assists", "first_kill",
            "money", "loadout_value", "net_worth",
            "position_x", "position_y"
        ])

        for sid, state in series_states.items():
            for game in state["games"]:
                for team in game["teams"]:
                    for p in team["players"]:
                        pos = p.get("position") or {}
                        writer.writerow([
                            sid,
                            game["id"],
                            game["sequenceNumber"],
                            game["map"]["name"],
                            team["name"],
                            p["id"],
                            p["name"],
                            p["character"]["name"] if p.get("character") else None,
                            p["kills"],
                            p["deaths"],
                            p["killAssistsGiven"],
                            p["firstKill"],
                            p["money"],
                            p["loadoutValue"],
                            p["netWorth"],
                            pos.get("x"),
                            pos.get("y")
                        ])

    # ───────────────────────────────────────────────────────
    # 3️⃣ Team aggregate stats (6 months)
    # ───────────────────────────────────────────────────────
    path = output_dir / "team_stats.csv"
    csv_paths["team_stats"] = str(path)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])

        s = team_stats_last_6_months["series"]
        k = s["kills"]

        writer.writerow(["series_count", s["count"]])
        writer.writerow(["kills_sum", k["sum"]])
        writer.writerow(["kills_min", k["min"]])
        writer.writerow(["kills_max", k["max"]])
        writer.writerow(["kills_avg", k["avg"]])
        writer.writerow(["games_played", team_stats_last_6_months["game"]["count"]])

        for w in team_stats_last_6_months["game"]["won"]:
            label = "wins" if w["value"] else "losses"
            writer.writerow([f"{label}_count", w["count"]])
            writer.writerow([f"{label}_percentage", w["percentage"]])
            writer.writerow([f"{label}_streak_current", w["streak"]["current"]])
            writer.writerow([f"{label}_streak_max", w["streak"]["max"]])

    # ───────────────────────────────────────────────────────
    # 4️⃣ Team segment stats
    # ───────────────────────────────────────────────────────
    path = output_dir / "team_segment_stats.csv"
    csv_paths["team_segment_stats"] = str(path)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["segment_type", "count", "deaths_sum", "deaths_min", "deaths_max", "deaths_avg"])

        for seg in team_stats_last_6_months["segment"]:
            d = seg["deaths"]
            writer.writerow([
                seg["type"],
                seg["count"],
                d["sum"],
                d["min"],
                d["max"],
                d["avg"]
            ])

    # ───────────────────────────────────────────────────────
    # 5️⃣ Player aggregate stats (6 months)
    # ───────────────────────────────────────────────────────
    path = output_dir / "player_stats.csv"
    csv_paths["player_stats"] = str(path)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "player_id", "nickname", "series_count",
            "kills_sum", "kills_min", "kills_max", "kills_avg",
            "games_played", "wins", "losses", "win_percentage"
        ])

        for pid, pdata in player_stats_last_6_months.items():
            stats = pdata["stats"]
            wins = next(w for w in stats["game"]["won"] if w["value"] is True)
            losses = next(w for w in stats["game"]["won"] if w["value"] is False)

            writer.writerow([
                pid,
                pdata["nickname"],
                stats["series"]["count"],
                stats["series"]["kills"]["sum"],
                stats["series"]["kills"]["min"],
                stats["series"]["kills"]["max"],
                stats["series"]["kills"]["avg"],
                stats["game"]["count"],
                wins["count"],
                losses["count"],
                wins["percentage"]
            ])

    # ───────────────────────────────────────────────────────
    # 6️⃣ Player segment stats
    # ───────────────────────────────────────────────────────
    path = output_dir / "player_segment_stats.csv"
    csv_paths["player_segment_stats"] = str(path)

    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "player_id", "nickname", "segment_type",
            "count", "deaths_sum", "deaths_min", "deaths_max", "deaths_avg"
        ])

        for pid, pdata in player_stats_last_6_months.items():
            for seg in pdata["stats"]["segment"]:
                d = seg["deaths"]
                writer.writerow([
                    pid,
                    pdata["nickname"],
                    seg["type"],
                    seg["count"],
                    d["sum"],
                    d["min"],
                    d["max"],
                    d["avg"]
                ])

    print(f"CSV scouting reports saved in: {output_dir}")
    return csv_paths

#main function to run the pipeline

async def run_scouting_pipeline(team_name: str):
    yield f"Resolving team: {team_name}"
    team_id = get_team_id_by_name(team_name)

    yield f"Fetching recent series for {team_name}"
    series_info = get_recent_valorant_series_for_team(team_name, limit=20)

    series_ids = [
        edge["node"]["id"]
        for edge in series_info["data"]["allSeries"]["edges"]
    ]

    yield f"Found {len(series_ids)} series"

    async with aiohttp.ClientSession() as session:
        series_states = {}

        for series_id in series_ids:
            yield f"Fetching series state: {series_id}"
            series_states[series_id] = await get_series_state_async(
                session, series_id
            )
            await asyncio.sleep(7)

        yield "Fetching team stats (last 6 months)"
        team_stats_last_6_months = get_team_stats_last_6_months(team_id)

        yield "Fetching team roster"
        raw_roster = get_team_roster(team_id)

        unique_roster = {p["id"]: p for p in raw_roster}
        team_roster = list(unique_roster.values())

        yield f"Found {len(team_roster)} players"

        player_stats_last_6_months = {}

        for player in team_roster:
            nickname = player["nickname"]
            yield f"Fetching stats for player: {nickname}"

            stats = await get_player_stats_last_6_months_async(
                session, player["id"]
            )

            player_stats_last_6_months[player["id"]] = {
                "nickname": nickname,
                "stats": stats
            }

            await asyncio.sleep(7)

    yield "Saving scouting CSV reports"
    csv_paths = save_scouting_report_csv(
        team_name=team_name,
        series_ids=series_ids,
        series_states=series_states,
        team_stats_last_6_months=team_stats_last_6_months,
        team_roster=team_roster,
        player_stats_last_6_months=player_stats_last_6_months
    )

    # ✅ FINAL structured yield
    yield {
        "type": "DONE",
        "csv_paths": csv_paths
    }



class ScoutingPipelineAgent(BaseAgent):
    """
    Runs the async scouting pipeline and stores results in session state.
    """

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, name: str):
        super().__init__(
            name=name,
            sub_agents=[],  # pure Python logic
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:

        team_name = ctx.session.state.get("team_name")

        logger.info(f"[{self.name}] Starting scouting for {team_name}")

        async for update in run_scouting_pipeline(team_name):

            # ✅ Final result
            if isinstance(update, dict) and update.get("type") == "DONE":
                ctx.session.state["scouting_csvs"] = update["csv_paths"]

                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="assistant",
                        parts=[types.Part(text="Scouting pipeline completed")]
                    )
                )
            else:
                # ✅ Progress update
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="assistant",
                        parts=[types.Part(text=str(update))]
                    )
                )

        logger.info(f"[{self.name}] Scouting completed for {team_name}")


ScoutingAgent=ScoutingPipelineAgent(name="ScoutingAgent")
