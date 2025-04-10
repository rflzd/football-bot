import requests
from rapidfuzz import fuzz, process

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def search_team_raw(name):
    """SofaScore search endpoint ilə komanda nəticələrini al"""
    url = f"https://api.sofascore.com/api/v1/search/{name}"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        data = r.json()
        return [team for cat in data.get("categories", []) for team in cat.get("teams", [])]
    except:
        return []

def find_best_match(query, teams, threshold=60):
    """Fuzzy match ilə ən uyğun komandanı tap"""
    team_names = [team["name"] for team in teams]
    best = process.extractOne(query, team_names, scorer=fuzz.token_sort_ratio, score_cutoff=threshold)
    if best:
        for team in teams:
            if team["name"] == best[0]:
                return {
                    "id": team["id"],
                    "name": team["name"],
                    "slug": team["slug"],
                    "sport": team["sport"]["name"],
                    "country": team["country"]["name"]
                }
    return None

def resolve_team(query: str) -> dict:
    """İstifadəçinin yazdığı adı düzgün komandaya map edən əsas funksiya"""
    cleaned_query = query.strip().lower()
    teams = search_team_raw(cleaned_query)
    if not teams:
        return {"error": "Komanda tapılmadı."}

    match = find_best_match(cleaned_query, teams)
    if not match:
        return {"error": "Ən uyğun komanda tapılmadı."}

    return match