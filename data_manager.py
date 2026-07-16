import pandas as pd
import requests
import soccerdata as sd
from statsbombpy import sb
import json
import os
from datetime import datetime, timedelta

# Football-Data.org anahtarını Streamlit secrets'tan al
API_KEY_FOOTBALL_DATA = os.environ.get("FOOTBALL_DATA_API_KEY", "your_key_here")
FOOTBALL_DATA_BASE = "https://api.football-data.org/v4"

# BSD API anahtarını Streamlit secrets'tan al
BZZOIRO_API_KEY = os.environ.get("BZZOIRO_API_KEY", "your_bsd_key_here")
BZZOIRO_BASE_URL = "https://sports.bzzoiro.com"

# Önbellek klasörü
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
    from sports_skills import football
    import pandas as pd
    
    league_map = {
        "Premier League": "premier-league",
        "La Liga": "la-liga",
        "Bundesliga": "bundesliga",
        "Serie A": "serie-a",
        "Ligue 1": "ligue-1"
    }
    league_slug = league_map.get(league, league.lower().replace(" ", "-"))
    season_id = f"{league_slug}-{season}"
    
    try:
        result = football.get_season_standings(season_id=season_id)
        if not result or "data" not in result:
            return pd.DataFrame({"Hata": ["Veri alınamadı"]})
        
        standings = result["data"].get("standings", [])
        if not standings:
            return pd.DataFrame({"Hata": ["Standings boş"]})
        
        first = standings[0]
        entries = first.get("entries", first.get("table", []))
        if not entries:
            return pd.DataFrame({"Hata": ["Tablo bulunamadı"]})
        
        df = pd.DataFrame(entries)
        return df
    except Exception as e:
        return pd.DataFrame({"Hata": [f"sports-skills hatası: {str(e)}"]})

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

# ==================== sports-skills ENTEGRASYONU ====================
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

# ==================== BSD (Bzziro Sports Data) ENTEGRASYONU ====================
def get_bsd_events(date_from=None, date_to=None, league_id=None, limit=50):
    """
    BSD'den maç listesini çeker.
    date_from: "2026-07-16" veya "2026-07-16T00:00:00Z" formatında
    date_to: aynı formatta
    league_id: lig ID'si (isteğe bağlı)
    limit: max 200
    """
    url = f"{BZZOIRO_BASE_URL}/api/v2/events/"
    headers = {"X-API-Key": BZZOIRO_API_KEY}
    params = {"limit": min(limit, 200)}
    
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to
    if league_id:
        params["league_id"] = league_id
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"BSD Events hatası: {e}")
        return None

def get_bsd_odds(event_id=None, league_id=None, season_id=None, team_id=None, updated_after=None):
    """
    BSD'den bahis oranlarını çeker.
    event_id: maç ID'si (isteğe bağlı)
    league_id: lig ID'si (isteğe bağlı)
    season_id: sezon ID'si (isteğe bağlı)
    team_id: takım ID'si (isteğe bağlı)
    updated_after: ISO format tarih (isteğe bağlı)
    """
    url = f"{BZZOIRO_BASE_URL}/api/v2/odds/"
    headers = {"X-API-Key": BZZOIRO_API_KEY}
    params = {}
    
    if event_id:
        params["event_id"] = event_id
    if league_id:
        params["league_id"] = league_id
    if season_id:
        params["season_id"] = season_id
    if team_id:
        params["team_id"] = team_id
    if updated_after:
        params["updated_after"] = updated_after
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"BSD Odds hatası: {e}")
        return None

def get_bsd_predictions(event_id):
    """
    BSD'den maç tahminlerini çeker.
    event_id: maç ID'si
    """
    url = f"{BZZOIRO_BASE_URL}/api/v2/predictions/"
    headers = {"X-API-Key": BZZOIRO_API_KEY}
    params = {"event_id": event_id}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"BSD Predictions hatası: {e}")
        return None
