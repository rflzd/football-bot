import requests
from difflib import get_close_matches

def search_team_id(query):
    url = "https://api.sofascore.com/api/v1/search/multi"
    params = {"q": query}
    res = requests.get(url, params=params)
    data = res.json()

    teams = []
    for section in data.get("sections", []):
        if section["name"] == "teams":
            for team in section.get("events", []):
                name = team.get("name", "")
                team_id = team.get("id", "")
                teams.append((name, team_id))

    if not teams:
        return None

    names = [name for name, _ in teams]
    best_match = get_close_matches(query, names, n=1, cutoff=0.5)
    if best_match:
        for name, tid in teams:
            if name == best_match[0]:
                return tid
    return None

def fetch_team_data(team_id):
    url = f"https://api.sofascore.com/api/v1/team/{team_id}/last/0"
    response = requests.get(url)
    matches = response.json().get("events", [])[:5]

    total_goals = 0
    wins = 0
    for match in matches:
        home = match["homeTeam"]["name"]
        away = match["awayTeam"]["name"]
        home_score = match["homeScore"]["current"]
        away_score = match["awayScore"]["current"]
        total_goals += home_score + away_score

        is_win = (
            (match["homeTeam"]["id"] == team_id and home_score > away_score) or
            (match["awayTeam"]["id"] == team_id and away_score > home_score)
        )
        if is_win:
            wins += 1

    stats = {
        "form": wins,
        "avg_goals": round(total_goals / 5, 2),
        "win_ratio": round((wins / 5) * 100, 2)
    }
    return stats