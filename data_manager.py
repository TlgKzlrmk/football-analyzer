import pandas as pd
import requests
import soccerdata as sd
from statsbombpy import sb
import json
import os
from datetime import datetime, timedelta

# ==================== API ANAHTARLARI ====================
API_KEY_FOOTBALL_DATA = os.environ.get("FOOTBALL_DATA_API_KEY", "683de67308df4cfcb2ef3051100bdc66")
FOOTBALL_DATA_BASE = "https://api.football-data.org/v4"

# Önbellek klasörü
CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

# ==================== FOOTBALL-DATA.ORG (BİRİNCİL) ====================
def football_data_request(endpoint):
    url = f"{FOOTBALL_DATA_BASE}/{endpoint}"
    headers = {"X-Auth-Token": API_KEY_FOOTBALL_DATA}
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

# ==================== HİBRİT PUAN DURUMU ====================
def get_league_table(league_code):
    """Önce Football-Data.org, olmazsa sports-skills."""
    cache_file = f"{CACHE_DIR}/table_{league_code}.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    
    # 1. Football-Data.org
    data = football_data_request(f"competitions/{league_code}/standings")
    if "error" not in data and "standings" in data:
        with open(cache_file, "w") as f:
            json.dump(data, f)
        return data
    
    # 2. sports-skills (yedek)
    from sports_skills import football
    try:
        # league_code'u sports-skills formatına çevir
        league_map = {
            "PL": "premier-league",
            "PD": "la-liga",
            "BL1": "bundesliga",
            "SA": "serie-a",
            "FL1": "ligue-1",
            "ELC": "championship",
            "SD": "la-liga-2",
            "BL2": "bundesliga-2",
            "SB": "serie-b",
            "FL2": "ligue-2",
            "ED": "eredivisie",
            "PPL": "portugal-primeira-liga",
            "SL": "süper-lig",
            "BLG": "belgian-pro-league",
            "SCO": "scottish-premiership",
            "AUT": "austrian-bundesliga",
            "SUI": "swiss-super-league",
            "GRE": "greek-super-league",
            "RUS": "russian-premier-league",
            "UKR": "ukrainian-premier-league",
            "DEN": "danish-superliga",
            "NOR": "norwegian-eliteserien",
            "SWE": "swedish-allsvenskan",
            "POL": "polish-ekstraklasa",
            "CRO": "croatian-hnl",
            "SRB": "serbian-superliga",
            "CZE": "czech-1-liga",
            "ROU": "romanian-liga-1",
            "HUN": "hungarian-nb-i",
            "BUL": "bulgarian-1-liga",
            "SVK": "slovak-super-liga",
            "SVN": "slovenian-prvaliga",
            "IRL": "irish-premier-division",
        }
        ss_league = league_map.get(league_code, league_code.lower())
        season_id = f"{ss_league}-2024"
        result = football.get_season_standings(season_id=season_id)
        if result and "data" in result:
            with open(cache_file, "w") as f:
                json.dump(result["data"], f)
            return result["data"]
    except:
        pass
    
    return {"error": "Tüm kaynaklardan veri alınamadı."}

# ==================== HİBRİT xG ====================
def get_xg_from_understat(league, season):
    """Önce Understat, olmazsa FBref (sports-skills)."""
    # 1. Understat
    try:
        understat = sd.Understat()
        df = understat.read_league_season(league=league, season=season)
        if not df.empty:
            return df
    except:
        pass
    
    # 2. FBref üzerinden sports-skills
    try:
        from sports_skills import football
        league_map = {
            "EPL": "premier-league",
            "La_liga": "la-liga",
            "Bundesliga": "bundesliga",
            "Serie_A": "serie-a",
            "Ligue_1": "ligue-1"
        }
        league_slug = league_map.get(league, league.lower().replace("_", "-"))
        season_id = f"{league_slug}-{season}"
        result = football.get_season_standings(season_id=season_id)
        if result and "data" in result:
            standings = result["data"].get("standings", [])
            if standings:
                first = standings[0]
                entries = first.get("entries", first.get("table", []))
                if entries:
                    df = pd.DataFrame(entries)
                    # xG'yi buradan çekmeye çalış
                    xg_cols = [c for c in df.columns if 'xg' in c.lower() or 'xG' in c]
                    if xg_cols:
                        return df[['team', 'played'] + xg_cols]
                    return df
    except:
        pass
    
    return pd.DataFrame()

# ==================== HİBRİT FBref ====================
def get_fbref_team_stats(league, season):
    """Önce FBref (sports-skills), olmazsa doğrudan sports-skills."""
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
    
    # 1. FBref (soccerdata ile)
    try:
        fbref = sd.FBref(league, season)
        df = fbref.read_team_season_stats(stat_type="standard")
        if not df.empty:
            return df
    except:
        pass
    
    # 2. sports-skills doğrudan
    try:
        result = football.get_season_standings(season_id=season_id)
        if result and "data" in result:
            standings = result["data"].get("standings", [])
            if standings:
                first = standings[0]
                entries = first.get("entries", first.get("table", []))
                if entries:
                    df = pd.DataFrame(entries)
                    return df
    except:
        pass
    
    return pd.DataFrame({"Hata": ["Tüm kaynaklardan veri alınamadı."]})

# ==================== HİBRİT TAKIM BİLGİLERİ ====================
def get_team_info(team_id):
    """Önce Football-Data.org, olmazsa sports-skills."""
    cache_file = f"{CACHE_DIR}/team_{team_id}.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    
    # 1. Football-Data.org
    data = football_data_request(f"teams/{team_id}")
    if "error" not in data:
        with open(cache_file, "w") as f:
            json.dump(data, f)
        return data
    
    # 2. sports-skills (takım ara)
    from sports_skills import football
    try:
        # team_id'yi isme çevirmek için basit bir eşleştirme (örnek)
        team_map = {
            "57": "arsenal",
            "58": "aston-villa",
            "61": "chelsea",
            "64": "liverpool",
            "65": "man-city",
            "66": "man-united",
            "67": "newcastle",
            "73": "tottenham",
            "80": "real-madrid",
            "81": "barcelona",
            "82": "atletico-madrid",
            "86": "real-betis",
            "90": "sevilla",
            "98": "valencia",
            "99": "villareal",
            "108": "ac-milan",
            "109": "inter",
            "110": "juventus",
            "112": "napoli",
            "113": "roma",
            "115": "atalanta",
            "157": "bayern-munich",
            "160": "dortmund",
            "161": "rb-leipzig",
            "168": "frankfurt",
            "170": "leverkusen",
            "177": "psg",
            "180": "marseille",
            "181": "lyon",
            "182": "nice",
            "183": "monaco",
            "184": "lille",
        }
        team_name = team_map.get(str(team_id), None)
        if team_name:
            result = football.get_team_profile(team_id=team_name)
            if result and "data" in result:
                with open(cache_file, "w") as f:
                    json.dump(result["data"], f)
                return result["data"]
    except:
        pass
    
    return {"error": "Tüm kaynaklardan veri alınamadı."}

# ==================== HİBRİT MAÇ LİSTESİ ====================
def get_team_matches(team_id, limit=10):
    """Önce Football-Data.org, olmazsa sports-skills."""
    cache_file = f"{CACHE_DIR}/team_matches_{team_id}.json"
    if os.path.exists(cache_file):
        with open(cache_file, "r") as f:
            return json.load(f)
    
    # 1. Football-Data.org
    data = football_data_request(f"teams/{team_id}/matches?limit={limit}")
    if "error" not in data:
        with open(cache_file, "w") as f:
            json.dump(data, f)
        return data
    
    # 2. sports-skills (maç listesi)
    from sports_skills import football
    try:
        # Takım adını almak için önce team_info'yu dene
        team_info = get_team_info(team_id)
        if "error" not in team_info:
            team_name = team_info.get("name", "").lower().replace(" ", "-")
            if team_name:
                # Belirli bir takımın maçlarını çekmek için season_id ile dene
                season_id = "premier-league-2024"
                result = football.get_season_fixtures(season_id=season_id)
                if result and "data" in result:
                    fixtures = result["data"].get("fixtures", [])
                    matches = []
                    for m in fixtures:
                        if team_name in m.get("home_team", "").lower() or team_name in m.get("away_team", "").lower():
                            matches.append(m)
                    if matches:
                        with open(cache_file, "w") as f:
                            json.dump({"matches": matches}, f)
                        return {"matches": matches}
    except:
        pass
    
    return {"error": "Tüm kaynaklardan veri alınamadı."}

# ==================== StatsBomb (OLAY BAZLI VERİ) ====================
def get_statsbomb_matches(competition_id, season_id):
    try:
        matches = sb.matches(competition_id=competition_id, season_id=season_id)
        return matches
    except Exception as e:
        return pd.DataFrame()

# ==================== HİBRİT OLAY BAZLI VERİ ====================
def get_statsbomb_events(match_id):
    """Önce StatsBomb, olmazsa sports-skills."""
    # 1. StatsBomb
    try:
        events = sb.events(match_id=match_id)
        if not events.empty:
            return events
    except:
        pass
    
    # 2. sports-skills (maç detayı)
    from sports_skills import football
    try:
        # Maç ID'sini sports-skills formatına çevir
        result = football.get_match_detail(match_id=match_id)
        if result and "data" in result:
            events_data = result["data"]
            # Olayları DataFrame'e çevir
            events_list = events_data.get("events", [])
            if events_list:
                df = pd.DataFrame(events_list)
                return df
    except:
        pass
    
    return pd.DataFrame()

# ==================== sports-skills DOĞRUDAN ====================
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

# ==================== TAKIM FORMU HESAPLAMA (HİBRİT) ====================
def get_team_recent_matches(team_id, league_code, limit=10):
    """
    Bir takımın son N maçını çeker.
    Önce Football-Data.org, olmazsa sports-skills.
    """
    matches = get_team_matches(team_id, limit=limit)
    if "error" not in matches:
        return matches.get("matches", [])
    
    # sports-skills yedek
    from sports_skills import football
    try:
        # Takım adını al
        team_info = get_team_info(team_id)
        if "error" not in team_info:
            team_name = team_info.get("name", "").lower().replace(" ", "-")
            if team_name:
                # Lig ID'sini bul
                league_map = {
                    "PL": "premier-league",
                    "PD": "la-liga",
                    "BL1": "bundesliga",
                    "SA": "serie-a",
                    "FL1": "ligue-1",
                }
                ss_league = league_map.get(league_code, "premier-league")
                season_id = f"{ss_league}-2024"
                result = football.get_season_fixtures(season_id=season_id)
                if result and "data" in result:
                    fixtures = result["data"].get("fixtures", [])
                    team_matches = []
                    for m in fixtures:
                        if team_name in m.get("home_team", "").lower() or team_name in m.get("away_team", "").lower():
                            team_matches.append(m)
                    return team_matches[:limit]
    except:
        pass
    
    return []

def calculate_team_form(team_id, league_code, match_limit=10):
    """
    Takımın son N maçlık form metriklerini hesaplar.
    Dönen değer: {'puan_avg', 'xg_avg', 'gol_avg', 'yediği_gol_avg', 'maç_sayısı', 'galibiyet', 'beraberlik', 'mağlubiyet'}
    """
    matches = get_team_recent_matches(team_id, league_code, limit=match_limit)
    
    if not matches:
        return {
            'puan_avg': 0,
            'xg_avg': 0,
            'gol_avg': 0,
            'yediği_gol_avg': 0,
            'maç_sayısı': 0,
            'galibiyet': 0,
            'beraberlik': 0,
            'mağlubiyet': 0,
            'form_str': 'Veri yok'
        }
    
    total_points = 0
    total_xg = 0
    total_goals_for = 0
    total_goals_against = 0
    wins = 0
    draws = 0
    losses = 0
    
    # Takım adını bul
    team_info = get_team_info(team_id)
    team_name = team_info.get("name", "") if "error" not in team_info else ""
    
    for m in matches:
        # Maç sonucunu bul
        home_team = m.get("home_team", {}).get("name", "") if isinstance(m.get("home_team"), dict) else m.get("home_team", "")
        away_team = m.get("away_team", {}).get("name", "") if isinstance(m.get("away_team"), dict) else m.get("away_team", "")
        
        # Skorları bul
        score = m.get("score", {})
        home_score = score.get("home", 0) if isinstance(score, dict) else 0
        away_score = score.get("away", 0) if isinstance(score, dict) else 0
        
        # Takımın hangi tarafta olduğunu bul
        if team_name and team_name in home_team:
            is_home = True
            goals_for = home_score
            goals_against = away_score
        elif team_name and team_name in away_team:
            is_home = False
            goals_for = away_score
            goals_against = home_score
        else:
            # Takım adı eşleşmezse geç
            continue
        
        total_goals_for += goals_for
        total_goals_against += goals_against
        
        # Puan ve galibiyet/beraberlik/mağlubiyet
        if goals_for > goals_against:
            total_points += 3
            wins += 1
        elif goals_for == goals_against:
            total_points += 1
            draws += 1
        else:
            losses += 1
        
        # xG (varsa)
        stats = m.get("statistics", {})
        if stats:
            if is_home:
                total_xg += float(stats.get("home_xg", 0))
            else:
                total_xg += float(stats.get("away_xg", 0))
    
    match_count = wins + draws + losses
    if match_count == 0:
        return {
            'puan_avg': 0,
            'xg_avg': 0,
            'gol_avg': 0,
            'yediği_gol_avg': 0,
            'maç_sayısı': 0,
            'galibiyet': 0,
            'beraberlik': 0,
            'mağlubiyet': 0,
            'form_str': 'Veri yok'
        }
    
    return {
        'puan_avg': round(total_points / match_count, 2),
        'xg_avg': round(total_xg / match_count, 2) if total_xg > 0 else 0,
        'gol_avg': round(total_goals_for / match_count, 2),
        'yediği_gol_avg': round(total_goals_against / match_count, 2),
        'maç_sayısı': match_count,
        'galibiyet': wins,
        'beraberlik': draws,
        'mağlubiyet': losses,
        'form_str': f"{wins}G-{draws}B-{losses}M"
    }

def get_team_hybrid_form(team_id, league_code):
    """
    Hem 5 maçlık hem 10 maçlık form verilerini döndürür.
    """
    form_5 = calculate_team_form(team_id, league_code, match_limit=5)
    form_10 = calculate_team_form(team_id, league_code, match_limit=10)
    
    return {
        'form_5': form_5,
        'form_10': form_10,
        'form_5_str': form_5.get('form_str', 'Veri yok'),
        'form_10_str': form_10.get('form_str', 'Veri yok'),
        'puan_avg_5': form_5.get('puan_avg', 0),
        'puan_avg_10': form_10.get('puan_avg', 0),
        'xg_avg_5': form_5.get('xg_avg', 0),
        'xg_avg_10': form_10.get('xg_avg', 0),
        'gol_avg_5': form_5.get('gol_avg', 0),
        'gol_avg_10': form_10.get('gol_avg', 0),
        'yediği_gol_avg_5': form_5.get('yediği_gol_avg', 0),
        'yediği_gol_avg_10': form_10.get('yediği_gol_avg', 0),
    }
