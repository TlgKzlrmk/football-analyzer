import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from data_manager import *
import os

st.set_page_config(page_title="Pro Football AI", layout="wide")
st.title("⚽ Pro Seviye AI Futbol Analiz")
st.markdown("### Top 30 Lig, 2. Ligler, Kupalar, UEFA & FIFA")

LEAGUE_CODES = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1",
    "Şampiyonlar Ligi": "CL",
    "Avrupa Ligi": "EL",
    "Dünya Kupası": "WC",
    "La Liga2": "SD",
    "Bundesliga 2": "BL2",
    "Serie B": "SB",
    "Ligue 2": "FL2",
    "Eredivisie": "ED",
    "Primeira Liga": "PPL",
    "Süper Lig": "SL"
}

league_name = st.selectbox("🏆 Lig/Turnuva Seç", list(LEAGUE_CODES.keys()))
league_code = LEAGUE_CODES[league_name]

if st.button("📊 Puan Durumunu Göster"):
    with st.spinner("Football-Data.org'dan veri çekiliyor..."):
        table = get_league_table(league_code)
        if "error" not in table and "standings" in table:
            standings = table["standings"]
            if standings:
                rows = standings[0].get("table", [])
                if rows:
                    df = pd.DataFrame([{
                        "Sıra": r["position"],
                        "Takım": r["team"]["name"],
                        "O": r["playedGames"],
                        "G": r["won"],
                        "B": r["draw"],
                        "M": r["lost"],
                        "A": r["goalsFor"],
                        "Y": r["goalsAgainst"],
                        "Puan": r["points"],
                        "Avans": r["goalDifference"]
                    } for r in rows])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("Bu lig için tablo verisi bulunamadı.")
            else:
                st.warning("Standings verisi boş.")
        else:
            st.error("Puan durumu alınamadı. API anahtarını veya lig kodunu kontrol edin.")
            st.json(table)

# Understat xG
if league_name in ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]:
    understat_mapping = {
        "Premier League": "EPL",
        "La Liga": "La_liga",
        "Bundesliga": "Bundesliga",
        "Serie A": "Serie_A",
        "Ligue 1": "Ligue_1"
    }
    if st.button("⚡ xG/xA Verileri (Understat)"):
        with st.spinner("Understat'ten xG verileri çekiliyor..."):
            xg_df = get_xg_from_understat(understat_mapping[league_name], "2024")
            if not xg_df.empty:
                st.dataframe(xg_df.head(20))
            else:
                st.warning("xG verisi alınamadı. Understat'te bu sezon verisi olmayabilir.")

# ============ FBref TAKIM İSTATİSTİKLERİ (sports-skills ile) ============
if st.button("📈 Takım İstatistikleri (FBref)"):
    with st.spinner("Veri çekiliyor (sports-skills üzerinden)..."):
        # Önce 2024 dene, olmazsa 2023
        for season in ["2024", "2023"]:
            df = get_fbref_team_stats(league_name, season)
            if not df.empty and "Hata" not in df.columns:
                st.success(f"{season} sezonu verisi başarıyla çekildi!")
                st.dataframe(df, use_container_width=True)
                break
            else:
                if not df.empty and "Hata" in df.columns:
                    st.warning(f"{season}: {df['Hata'].iloc[0]}")
                else:
                    st.warning(f"{season} sezonu için veri alınamadı.")
        else:
            st.error("Hiçbir sezon için veri alınamadı.")

# ============ sports-skills Test Alanı ============
st.markdown("---")
st.subheader("🧪 sports-skills Test Alanı")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏆 Premier League Puan Durumu (sports-skills)"):
        with st.spinner("sports-skills'ten veri çekiliyor..."):
            data = get_ss_standings("premier-league-2024")
            if data:
                if "standings" in data:
                    standings = data["standings"]
                    if isinstance(standings, list) and len(standings) > 0:
                        first = standings[0]
                        entries = None
                        if "entries" in first:
                            entries = first["entries"]
                        elif "table" in first:
                            entries = first["table"]
                        else:
                            entries = standings
                        
                        if entries and isinstance(entries, list) and len(entries) > 0:
                            rows = []
                            for item in entries:
                                team = item.get("team", {})
                                if isinstance(team, dict):
                                    team_name = team.get("name", "")
                                else:
                                    team_name = str(team)
                                
                                row = {
                                    "Sıra": item.get("rank") or item.get("position", ""),
                                    "Takım": team_name,
                                    "O": item.get("played") or item.get("playedGames", ""),
                                    "G": item.get("win") or item.get("won", ""),
                                    "B": item.get("draw", ""),
                                    "M": item.get("lose") or item.get("lost", ""),
                                    "A": item.get("goalsFor") or item.get("gf", ""),
                                    "Y": item.get("goalsAgainst") or item.get("ga", ""),
                                    "Puan": item.get("points", ""),
                                    "Avans": item.get("goalDifference") or item.get("goalDiff", "")
                                }
                                rows.append(row)
                            
                            df = pd.DataFrame(rows)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.warning("Tablo verisi bulunamadı.")
                            st.json(first)
                    else:
                        st.warning("Standings listesi boş.")
                else:
                    st.warning("'standings' anahtarı bulunamadı.")
                    st.json(data)
            else:
                st.error("Veri alınamadı.")

with col2:
    if st.button("🔎 Takım Ara (Arsenal)"):
        with st.spinner("Takım profili aranıyor..."):
            team = get_ss_team_profile("arsenal")
            if team:
                st.json(team)
            else:
                st.error("Takım bulunamadı.")
