import requests
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_last_matches(team_id, limit=5):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/last/0"
    r = requests.get(url, headers=HEADERS)
    matches = r.json().get("events", [])[:limit]

    result = []
    for match in matches:
        result.append({
            "date": datetime.utcfromtimestamp(match["startTimestamp"]).strftime("%d %b %Y"),
            "home": match["homeTeam"]["name"],
            "away": match["awayTeam"]["name"],
            "score": f"{match['homeScore']['current']} - {match['awayScore']['current']}",
            "tournament": match["tournament"]["name"]
        })
    return result

def get_next_match(team_id):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/events/next/0"
    r = requests.get(url, headers=HEADERS)
    events = r.json().get("events", [])
    if not events:
        return None

    match = events[0]
    return {
        "date": datetime.utcfromtimestamp(match["startTimestamp"]).strftime("%d %b %Y %H:%M"),
        "home": match["homeTeam"]["name"],
        "away": match["awayTeam"]["name"],
        "tournament": match["tournament"]["name"]
    }

def get_statistics(team_id, tournament_id, season_id):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/statistics/unique-tournament/{tournament_id}/season/{season_id}"
    r = requests.get(url, headers=HEADERS)
    stats = r.json().get("statistics", {})
    return {
        "shots": stats.get("averageShots", "?"),
        "shots_on_target": stats.get("averageShotsOnTarget", "?"),
        "yellow_cards": stats.get("averageYellowCards", "?"),
        "red_cards": stats.get("averageRedCards", "?"),
        "possession": stats.get("averagePossession", "?")
    }
    
def get_active_tournament_info(team_id):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/unique-tournaments/standings"
    r = requests.get(url, headers=HEADERS)
    data = r.json()

    # Ən son aktiv turnir (mövcud sezon)
    try:
        item = data["uniqueTournaments"][0]
        return {
            "tournament_id": item["uniqueTournament"]["id"],
            "season_id": item["season"]["id"]
        }
    except:
        return None

def get_team_data(resolved_team: dict):
    team_id = resolved_team["id"]

    tournament_info = get_active_tournament_info(team_id)
    if not tournament_info:
        return {"error": "Turnir və mövsüm məlumatı tapılmadı."}

    return {
        "team": resolved_team,
        "next_match": get_next_match(team_id),
        "last_matches": get_last_matches(team_id),
        "statistics": get_statistics(
            team_id,
            tournament_info["tournament_id"],
            tournament_info["season_id"]
        )
    }