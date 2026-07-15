import pandas as pd
import requests
import soccerdata as sd
from statsbombpy import sb
import json
import os
from datetime import datetime, timedelta

# Football-Data.org anahtarını Streamlit secrets'tan al
API_KEY_FOOTBALL_DATA = os.environ.get("FOOTBALL_DATA_API_KEY", "683de67308df4cfcb2ef3051100bdc66")
FOOTBALL_DATA_BASE = "https://api.football-data.org/v4"

# Önbellek klasörü (verileri tekrar tekrar çekmemek için)
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def football_data_request(endpoint):
    """Football-Data.org'a istek atar ve JSON döndürür."""
    url = f"{FOOTBALL_DATA_BASE}/{endpoint}"
    headers = {"X-Auth-Token": API_KEY_FOOTBALL_DATA}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def get_league_table(league_code):
    """
    Football-Data.org'dan puan durumunu çeker.
    league_code örnekleri: PL (Premier), PD (La Liga), BL1 (Bundesliga), SA (Serie A), FL1 (Ligue 1), CL (UCL), WC (World Cup)
    """
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
    """Football-Data.org'dan takımın son maçlarını çeker."""
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
    """Football-Data.org'dan takım detaylarını çeker."""
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
    """
    Understat'ten xG/xA verilerini çeker.
    league: 'EPL', 'La_liga', 'Bundesliga', 'Serie_A', 'Ligue_1'
    """
    try:
        # soccerdata ile Understat
        understat = sd.Understat()
        df = understat.read_league_season(league=league, season=season)
        return df
    except Exception as e:
        return pd.DataFrame()  # Boş DataFrame döndür

def get_fbref_team_stats(league, season):
    """FBref'ten takım istatistiklerini çeker."""
    try:
        fbref = sd.FBref(league, season)
        df = fbref.read_team_season_stats(stat_type="standard")
        return df
    except Exception as e:
        return pd.DataFrame()

def get_statsbomb_matches(competition_id, season_id):
    """StatsBomb açık veriden maç listesi çeker."""
    try:
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        return matches
    except Exception as e:
        return pd.DataFrame()

def get_statsbomb_events(match_id):
    """StatsBomb açık veriden olay bazlı veri çeker."""
    try:
        events = sb.events(match_id=match_id)
        return events
    except Exception as e:
        return pd.DataFrame()
# ==================== sports-skills ENTEGRASYONU ====================
from sports_skills import football

def get_ss_standings(season_id: str):
    """
    sports-skills ile puan durumu çeker ve düzgün bir liste döndürür.
    """
    try:
        result = football.get_season_standings(season_id=season_id)
        if not result or "data" not in result:
            return None
        
        standings_data = result["data"].get("standings", [])
        if not standings_data:
            return None
        
        # standings_data genellikle bir liste içinde sözlükler barındırır.
        # Örnek: [{"rank":1, "team":"Arsenal", "played":10, ...}, ...]
        # Eğer iç içe geçmişse, doğru katmana inmek gerekir.
        # Çoğu durumda standings_data[0] ana tabloyu içerir.
        if isinstance(standings_data, list) and len(standings_data) > 0:
            # Eğer ilk eleman 'table' veya 'standings' anahtarına sahipse içine gir.
            if isinstance(standings_data[0], dict) and "table" in standings_data[0]:
                return standings_data[0]["table"]
            elif isinstance(standings_data[0], dict) and "standings" in standings_data[0]:
                return standings_data[0]["standings"]
            else:
                # Doğrudan liste halindeyse
                return standings_data
        else:
            return None
    except Exception as e:
        print(f"sports-skills puan durumu hatası: {e}")
        return None
