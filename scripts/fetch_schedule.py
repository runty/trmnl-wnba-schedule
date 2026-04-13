#!/usr/bin/env python3
"""Fetch WNBA schedule data from ESPN API and generate per-team JSON for TRMNL."""

import calendar
import json
import os
import sys
from datetime import datetime, timezone
from urllib.error import URLError
from urllib.request import Request, urlopen

ESPN_BASE = "https://site.api.espn.com/apis/site/v2/sports/basketball/wnba"
WNBA_LOGO = "https://a.espncdn.com/i/teamlogos/leagues/500/wnba.png"

TEAMS = {
    "atlanta-dream": 20,
    "chicago-sky": 19,
    "connecticut-sun": 18,
    "dallas-wings": 3,
    "golden-state-valkyries": 129689,
    "indiana-fever": 5,
    "las-vegas-aces": 17,
    "los-angeles-sparks": 6,
    "minnesota-lynx": 8,
    "new-york-liberty": 9,
    "phoenix-mercury": 11,
    "portland-fire": 132052,
    "seattle-storm": 14,
    "toronto-tempo": 131935,
    "washington-mystics": 16,
}


def fetch_json(url):
    req = Request(url, headers={"User-Agent": "TRMNL-WNBA-Recipe/1.0"})
    with urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def fetch_all_records():
    """Fetch current W-L records for all WNBA teams."""
    records = {}
    for slug, team_id in TEAMS.items():
        try:
            data = fetch_json(f"{ESPN_BASE}/teams/{team_id}")
            team = data.get("team", {})
            record_items = team.get("record", {}).get("items", [])
            total = next((r for r in record_items if r.get("type") == "total"), {})
            records[str(team_id)] = total.get("summary", "0-0")
        except Exception:
            records[str(team_id)] = "0-0"
    return records


def parse_game(event, team_id, team_records):
    """Parse a single ESPN event into a clean game object."""
    comp = event.get("competitions", [{}])[0]
    competitors = comp.get("competitors", [])
    status = comp.get("status", {}).get("type", {})
    venue = comp.get("venue", {})
    season_type = event.get("seasonType", {})

    home_away = "home"
    opponent = {}
    team_score = ""
    opp_score = ""
    for c in competitors:
        if str(c.get("id")) == str(team_id):
            home_away = c.get("homeAway", "home")
            team_score = c.get("score", "")
        else:
            opponent = c
            opp_score = c.get("score", "")

    opp_team = opponent.get("team", {})
    opp_abbr = opp_team.get("abbreviation", "")
    date_iso = event.get("date", "")

    # Use WNBA logo as fallback for non-WNBA opponents (exhibitions, international teams)
    if opp_abbr and opp_abbr != "???":
        opp_logo = f"https://a.espncdn.com/i/teamlogos/wnba/500/{opp_abbr.lower()}.png"
    else:
        opp_logo = WNBA_LOGO
        opp_abbr = opp_team.get("shortDisplayName", opp_team.get("displayName", "TBD"))

    opp_id = str(opponent.get("id", ""))
    opp_record = team_records.get(opp_id, "")

    try:
        dt = datetime.fromisoformat(date_iso.replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        dt = None

    return {
        "date_iso": date_iso,
        "date": status.get("detail", ""),
        "date_short": status.get("shortDetail", ""),
        "day_of_week": dt.strftime("%a") if dt else "",
        "month": dt.strftime("%B") if dt else "",
        "month_num": dt.month if dt else 0,
        "day_num": dt.day if dt else 0,
        "year": dt.year if dt else 0,
        "opponent": opp_team.get("displayName", "Unknown"),
        "opp_abbr": opp_abbr,
        "opp_logo": opp_logo,
        "opp_record": opp_record,
        "home_away": home_away,
        "is_home": home_away == "home",
        "location": "Home" if home_away == "home" else "Away",
        "venue": venue.get("fullName", ""),
        "city": f"{venue.get('address', {}).get('city', '')}, {venue.get('address', {}).get('state', '')}".strip(", "),
        "status": status.get("description", "Scheduled"),
        "completed": status.get("completed", False),
        "season_type": season_type.get("name", ""),
        "team_score": team_score,
        "opp_score": opp_score,
        "result": "W" if (team_score and opp_score and int(team_score) > int(opp_score)) else
                  "L" if (team_score and opp_score and int(team_score) < int(opp_score)) else "",
        "score_display": f"{team_score}-{opp_score}" if (team_score and opp_score) else "",
    }


def build_calendar(games, year, month):
    """Build a calendar grid for the given month with game data embedded."""
    cal = calendar.Calendar(firstweekday=6)  # Sunday first
    weeks = cal.monthdayscalendar(year, month)

    game_map = {}
    for g in games:
        if g["year"] == year and g["month_num"] == month:
            game_map[g["day_num"]] = g

    result_weeks = []
    for week in weeks:
        week_data = []
        for day in week:
            if day == 0:
                week_data.append({"day": 0, "has_game": False})
            else:
                game = game_map.get(day)
                if game:
                    entry = {
                        "day": day,
                        "has_game": True,
                        "completed": game["completed"],
                        "opp_abbr": game["opp_abbr"],
                        "home_away": game["home_away"],
                        "is_home": game["is_home"],
                        "time": game["date_short"],
                    }
                    if game["completed"]:
                        entry["result"] = game["result"]
                        entry["score_display"] = game["score_display"]
                    week_data.append(entry)
                else:
                    week_data.append({"day": day, "has_game": False})
        result_weeks.append(week_data)

    return {
        "month_name": calendar.month_name[month],
        "month_num": month,
        "year": year,
        "weeks": result_weeks,
    }


def process_team(slug, team_id, team_records):
    """Fetch and transform schedule for a single team."""
    url = f"{ESPN_BASE}/teams/{team_id}/schedule"
    data = fetch_json(url)

    team_info = data.get("team", {})
    events = data.get("events", [])
    now = datetime.now(timezone.utc)

    games = [parse_game(e, team_id, team_records) for e in events]
    upcoming = [g for g in games if not g["completed"]]
    recent = [g for g in games if g["completed"]]

    # Build calendar for current month and next month
    calendars = []
    current_month = now.month
    current_year = now.year
    for offset in range(3):
        m = current_month + offset
        y = current_year
        if m > 12:
            m -= 12
            y += 1
        month_games = [g for g in games if g["month_num"] == m and g["year"] == y]
        if month_games:
            calendars.append(build_calendar(games, y, m))

    next_game = upcoming[0] if upcoming else None

    # Fetch game preview for next game
    preview = ""
    if next_game:
        try:
            game_id = next_game.get("date_iso", "").replace("-", "").replace(":", "").replace("Z", "")
            # Use the event ID from the original events data
            for e in events:
                if e.get("date") == next_game["date_iso"]:
                    game_id = e["id"]
                    break
            summary_data = fetch_json(f"{ESPN_BASE}/summary?event={game_id}")

            parts = []

            # Season series
            series = summary_data.get("seasonseries", [])
            if series:
                s = series[0]
                parts.append(s.get("summary", ""))

            # Last 5 form for both teams
            l5 = summary_data.get("lastFiveGames", [])
            for team_l5 in l5:
                t_name = team_l5.get("team", {}).get("abbreviation", "")
                results = [e.get("gameResult", "") for e in team_l5.get("events", [])]
                if results:
                    form = "".join(r[0] if r else "" for r in results[:5])
                    parts.append(f"{t_name} last 5: {form}")

            preview = ". ".join(p for p in parts if p)
        except Exception:
            preview = ""

    if next_game:
        next_game["preview"] = preview

    return {
        "team": {
            "name": team_info.get("displayName", ""),
            "abbreviation": team_info.get("abbreviation", ""),
            "logo": team_info.get("logo", ""),
            "record": team_info.get("recordSummary", "0-0"),
            "standing": team_info.get("standingSummary", ""),
            "color": team_info.get("color", "000000"),
        },
        "upcoming": upcoming[:20],
        "recent": list(reversed(recent[-5:])),
        "next_game": next_game,
        "calendars": calendars,
        "games_remaining": len(upcoming),
        "total_games": len(games),
        "updated": now.strftime("%Y-%m-%d %H:%M UTC"),
    }


def main():
    out_dir = os.path.join(os.path.dirname(__file__), "..", "api", "teams")
    os.makedirs(out_dir, exist_ok=True)

    print("Fetching team records...")
    team_records = fetch_all_records()
    print(f"Got records for {len(team_records)} teams\n")

    errors = []
    for slug, team_id in TEAMS.items():
        try:
            result = process_team(slug, team_id, team_records)
            path = os.path.join(out_dir, f"{slug}.json")
            with open(path, "w") as f:
                json.dump(result, f, separators=(",", ":"))
            print(f"OK  {slug} ({result['team']['name']}) - {result['games_remaining']} upcoming games")
        except (URLError, KeyError, IndexError) as e:
            errors.append(f"{slug}: {e}")
            print(f"ERR {slug}: {e}", file=sys.stderr)

    if errors:
        print(f"\n{len(errors)} error(s) encountered", file=sys.stderr)
        sys.exit(1)

    print(f"\nDone. Generated {len(TEAMS) - len(errors)} team files in {out_dir}")


if __name__ == "__main__":
    main()
