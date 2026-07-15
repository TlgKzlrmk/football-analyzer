import pandas as pd
import requests
import soccerdata as sd
from statsbombpy import sb
import json
import os
from datetime import datetime, timedelta

API_KEY_FOOTBALL_DATA = os.environ.get("FOOTBALL_DATA_API_KEY", "683de67308df4cfcb2ef3051100bdc66")
FOOTBALL_DATA_BASE = "https://api.football-data.org/v4"

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def football_data_request(endpoint):
    url = f"{FOOTBALL_DATA_BASE}/{endpoint}"
    headers = {"X-Auth-Token": API_KEY_FOOTBALL_DATA}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def get_league_table(league_code):
    cache_file = f"{CACHE_DIR}/table_{league_code}.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    data = football_data_request(f"competitions/{league_code}/standings")
    if "error" not in data:
        with open(cache_file, "w") as f:
            json.dump(data, f)
    return data

def get_team_matches(team_id, limit=10):
    cache_file = f"{CACHE_DIR}/team_matches_{team_id}.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    data = football_data_request(f"teams/{team_id}/matches?limit={limit}")
    if "error" not in data:
        with open(cache_file, "w") as f:
            json.dump(data, f)
    return data

def get_team_info(team_id):
    cache_file = f"{CACHE_DIR}/team_{team_id}.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    data = football_data_request(f"teams/{team_id}")
    if "error" not in data:
        with open(cache_file, "w") as f:
            json.dump(data, f)
    return data

def get_xg_from_understat(league, season):
    try:
        understat = sd.Understat()
        df = understat.read_league_season(league=league, season=season)
        return df
    except Exception as e:
        return pd.DataFrame()

def get_fbref_team_stats(league, season):
    """
    FBref'ten takım istatistiklerini cloudscraper ile çeker (Cloudflare aşar).
    league: "Premier League", "La Liga" gibi (İngilizce isim)
    season: "2024-2025" veya "2023-2024" formatında
    """
    import pandas as pd
    import cloudscraper
    
    # FBref URL formatı
    league_slug = {
        "Premier League": "Premier-League",
        "La Liga": "La-Liga",
        "Bundesliga": "Bundesliga",
        "Serie A": "Serie-A",
        "Ligue 1": "Ligue-1"
    }.get(league, league.replace(" ", "-"))
    
    url = f"https://fbref.com/en/comps/{season}/{league_slug}-Stats"
    
    try:
        scraper = cloudscraper.create_scraper()
        resp = scraper.get(url, timeout=15)
        resp.raise_for_status()
        
        # Tabloları çek
        tables = pd.read_html(resp.text)
        if tables:
            df = tables[0]  # İlk tablo genelde takım istatistikleridir
            return df
        else:
            return pd.DataFrame({"Hata": ["Tablo bulunamadı"]})
    except Exception as e:
        return pd.DataFrame({"Hata": [f"FBref çekme hatası: {str(e)}"]})

def get_statsbomb_matches(competition_id, season_id):
    try:
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        return matches
    except Exception as e:
        return pd.DataFrame()

def get_statsbomb_events(match_id):
    try:
        events = sb.events(match_id=match_id)
        return events
    except Exception as e:
        return pd.DataFrame()

# ==================== sports-skills ====================
from sports_skills import football

def get_ss_standings(season_id: str):
    try:
        result = football.get_season_standings(season_id=season_id)
        if not result or "data" not in result:
            return None
        return result["data"]
    except Exception as e:
        print(f"sports-skills puan durumu hatası: {e}")
        return None

def get_ss_team_profile(team_id: str):
    try:
        result = football.get_team_profile(team_id=team_id)
        if result and "data" in result:
            return result["data"]
        else:
            return None
    except Exception as e:
        print(f"sports-skills takım profili hatası: {e}")
        return None

def get_ss_player_market_value(tm_player_id: str):
    try:
        result = football.get_player_market_value(tm_player_id=tm_player_id)
        if result and "data" in result:
            return result["data"]
        else:
            return None
    except Exception as e:
        print(f"Transfermarkt hatası: {e}")
        return None

def get_ss_player_stats(player_id: str):
    try:
        result = football.get_player_stats(player_id=player_id)
        if result and "data" in result:
            return result["data"]
        else:
            return None
    except Exception as e:
        print(f"sports-skills oyuncu istatistikleri hatası: {e}")
        return None
