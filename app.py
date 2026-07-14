import streamlit as st
import requests
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from datetime import datetime, timedelta
import os

API_KEY = st.secrets.get("API_KEY", "deneme123")
HEADERS = {"x-apisports-key": API_KEY}
BASE_URL = "https://v3.football.api-sports.io"

LEAGUES = {
    "İngiltere Premier": 39, "İngiltere Championship": 40,
    "İspanya La Liga": 140, "İspanya La Liga2": 141,
    "Almanya Bundesliga": 78, "Almanya 2. Bundesliga": 79,
    "İtalya Serie A": 135, "İtalya Serie B": 136,
    "Fransa Ligue 1": 61, "Fransa Ligue 2": 62,
    "Hollanda Eredivisie": 88, "Portekiz Primeira": 94,
    "Belçika Pro": 144, "Türkiye Süper Lig": 203, "Türkiye 1. Lig": 204,
    "Şampiyonlar Ligi": 2, "Avrupa Ligi": 3,
    "İngiltere FA Cup": 45, "İspanya Kral Kupası": 143, "Almanya DFB": 81
}

def get_matches(league_id, season="2025"):
    today = datetime.now().strftime("%Y-%m-%d")
    url = f"{BASE_URL}/fixtures"
    params = {"league": league_id, "season": season, "date": today}
    try:
        resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = resp.json()
        if not data["response"]:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            params["date"] = tomorrow
            resp = requests.get(url, headers=HEADERS, params=params, timeout=10)
            data = resp.json()
        matches = []
        for m in data["response"]:
            matches.append({
                "id": m["fixture"]["id"],
                "home": m["teams"]["home"]["name"],
                "away": m["teams"]["away"]["name"],
                "date": m["fixture"]["date"][:10]
            })
        return matches
    except:
        return []

def analyze_match(league_name, match_id):
    if not match_id:
        return None, "Lütfen maç seçin!", None
    league_id = LEAGUES.get(league_name)
    if not league_id:
        return None, "Lig bulunamadı!", None
    matches = get_matches(league_id)
    match = next((m for m in matches if str(m["id"]) == match_id), None)
    if not match:
        return None, "Maç bulunamadı!", None
    home, away = match["home"], match["away"]
    
    url = f"{BASE_URL}/fixtures/statistics"
    resp = requests.get(url, headers=HEADERS, params={"fixture": match_id}, timeout=10)
    stats = resp.json()
    home_stats = {}
    away_stats = {}
    if stats.get("response"):
        for team_data in stats["response"]:
            if team_data["team"]["name"] == home:
                for s in team_data["statistics"]:
                    home_stats[s["type"]] = s["value"]
            else:
                for s in team_data["statistics"]:
                    away_stats[s["type"]] = s["value"]
    
    def calc_xg(st):
        try:
            shots = float(st.get("Total Shots", 0))
            on_target = float(st.get("Shots on Goal", 0))
            return round((on_target / (shots + 1)) * 1.2 + (shots / 15), 2) if shots > 0 else 0.0
        except:
            return 0.0
    
    home_xg = calc_xg(home_stats)
    away_xg = calc_xg(away_stats)
    
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(10, 7))
    np.random.seed(int(match_id) % 100)
    for _ in range(np.random.randint(5, 12)):
        x = np.random.uniform(50, 105)
        y = np.random.uniform(20, 80)
        color = 'red' if np.random.rand() > 0.85 else 'blue'
        ax.scatter(x, y, s=150, color=color, alpha=0.7, edgecolors='white')
    ax.set_title(f"🎯 {home} {home_xg} - {away_xg} {away}", color='white', fontsize=14)
    
    report = f"""
**📊 MAÇ RAPORU - {home} vs {away}**
- ⚽ xG: {home} {home_xg} - {away_xg} {away}
- 🏃 Topa Sahip Olma: {home_stats.get('Ball Possession', '?')} - {away_stats.get('Ball Possession', '?')}
- 🎯 İsabetli Şut: {home_stats.get('Shots on Goal', '?')} - {away_stats.get('Shots on Goal', '?')}
    """
    return fig, report, None

st.set_page_config(page_title="Pro Football AI", layout="wide")
st.title("⚽ Pro Seviye AI Futbol Analiz")
st.markdown("### Top 20 Lig, 2. Ligler, Kupalar, UEFA & FIFA")

col1, col2 = st.columns(2)
with col1:
    league_name = st.selectbox("🏆 Lig/Turnuva Seç", list(LEAGUES.keys()))
with col2:
    matches = get_matches(LEAGUES[league_name])
    if matches:
        match_options = {f"{m['home']} vs {m['away']} ({m['date']})": str(m['id']) for m in matches}
        selected_match_label = st.selectbox("📅 Maç Seç", list(match_options.keys()))
        match_id = match_options[selected_match_label]
    else:
        st.warning("Bugün/yarın maç yok")
        match_id = None

if st.button("🚀 Analiz Et", type="primary"):
    if match_id:
        fig, report, error = analyze_match(league_name, match_id)
        if error:
            st.error(error)
        else:
            st.markdown(report)
            st.pyplot(fig)
    else:
        st.warning("Lütfen bir maç seçin.")
