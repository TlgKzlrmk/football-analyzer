import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from data_manager import *
import os

st.set_page_config(page_title="Pro Football AI", layout="wide")
st.title("⚽ Pro Seviye AI Futbol Analiz")
st.markdown("### Top 30 Lig, 2. Ligler, Kupalar, UEFA & FIFA")

# Football-Data.org lig kodları
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

# Understat xG (sadece 5 büyük lig)
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

# FBref takım istatistikleri (opsiyonel)
if st.button("📈 Takım İstatistikleri (FBref)"):
    with st.spinner("FBref'ten veri çekiliyor..."):
        fbref_league_map = {
            "Premier League": "ENG-Premier League",
            "La Liga": "ESP-La Liga",
            "Bundesliga": "GER-Bundesliga",
            "Serie A": "ITA-Serie A",
            "Ligue 1": "FRA-Ligue 1"
        }
        if league_name in fbref_league_map:
            df = get_fbref_team_stats(fbref_league_map[league_name], "2024")
            if not df.empty:
                st.dataframe(df.head(20))
            else:
                st.warning("FBref verisi alınamadı.")
        else:
            st.info("FBref şu anda sadece 5 büyük lig için etkindir.")

# ============ sports-skills TEST ALANI ============
st.markdown("---")
st.subheader("🧪 sports-skills Test Alanı")

col1, col2 = st.columns(2)

with col1:
    if st.button("🏆 Premier League Puan Durumu (sports-skills)"):
        with st.spinner("sports-skills'ten veri çekiliyor..."):
            data = get_ss_standings("premier-league-2024")
            if data:
                # 'standings' anahtarını kontrol et
                if "standings" in data:
                    standings = data["standings"]
                    if isinstance(standings, list) and len(standings) > 0:
                        first = standings[0]
                        
                        # Hangi anahtarın içinde tablo var?
                        entries = None
                        if "entries" in first:
                            entries = first["entries"]
                        elif "table" in first:
                            entries = first["table"]
                        else:
                            # Belki doğrudan listedir
                            entries = standings
                        
                        if entries and isinstance(entries, list) and len(entries) > 0:
                            # Tabloyu oluştur
                            rows = []
                            for item in entries:
                                # Takım bilgisi iç içe olabilir
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
                                    "A": item.get("goalsFor") or item.get("goalsFor", ""),
                                    "Y": item.get("goalsAgainst") or item.get("goalsAgainst", ""),
                                    "Puan": item.get("points", ""),
                                    "Avans": item.get("goalDifference") or item.get("goalDiff", "")
                                }
                                rows.append(row)
                            
                            df = pd.DataFrame(rows)
                            st.dataframe(df, use_container_width=True)
                        else:
                            st.warning("Tablo verisi bulunamadı. Lütfen yapıyı kontrol edin.")
                            st.json(first)  # Hata ayıklama için
                    else:
                        st.warning("Standings listesi boş veya beklenen formatta değil.")
                else:
                    st.warning("'standings' anahtarı bulunamadı. Tüm veri:")
                    st.json(data)
            else:
                st.error("Veri alınamadı. Lütfen sezon ID'sini kontrol edin (premier-league-2024).")

with col2:
    if st.button("🔎 Takım Ara (Arsenal)"):
        with st.spinner("Takım profili aranıyor..."):
            team = get_ss_team_profile("arsenal")
            if team:
                st.json(team)
            else:
                st.error("Takım bulunamadı.")
