import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from data_manager import *

st.set_page_config(page_title="Pro Football AI", layout="wide")
st.title("⚽ Pro Seviye AI Futbol Analiz")
st.markdown("### Top 30 Lig, 2. Ligler, Kupalar, UEFA & FIFA")

# Football-Data.org lig kodları (kendi API dokümantasyonundan kontrol et)
LEAGUE_CODES = {
    "Premier League": "PL",
    "La Liga": "PD",
    "Bundesliga": "BL1",
    "Serie A": "SA",
    "Ligue 1": "FL1",
    "Şampiyonlar Ligi": "CL",
    "Dünya Kupası": "WC",
    "Avrupa Ligi": "EL",
    # ... daha fazlasını ekleyebilirsin
}

# Kullanıcı lig seçer
league_name = st.selectbox("🏆 Lig/Turnuva Seç", list(LEAGUE_CODES.keys()))
league_code = LEAGUE_CODES[league_name]

# Puan durumunu göster
if st.button("📊 Puan Durumunu Göster"):
    table = get_league_table(league_code)
    if "error" not in table:
        standings = table.get("standings", [])
        if standings:
            rows = standings[0].get("table", [])
            df = pd.DataFrame([{
                "Sıra": r["position"],
                "Takım": r["team"]["name"],
                "O": r["playedGames"],
                "G": r["won"],
                "B": r["draw"],
                "M": r["lost"],
                "A": r["goalsFor"],
                "Y": r["goalsAgainst"],
                "Puan": r["points"]
            } for r in rows])
            st.dataframe(df, use_container_width=True)
    else:
        st.error("Puan durumu alınamadı.")

# xG verileri (Understat) - sadece 5 büyük lig için
if league_name in ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]:
    understat_mapping = {
        "Premier League": "EPL",
        "La Liga": "La_liga",
        "Bundesliga": "Bundesliga",
        "Serie A": "Serie_A",
        "Ligue 1": "Ligue_1"
    }
    if st.button("⚡ xG/xA Verileri (Understat)"):
        xg_df = get_xg_from_understat(understat_mapping[league_name], "2024")
        if not xg_df.empty:
            st.dataframe(xg_df.head(20))
        else:
            st.warning("xG verisi alınamadı.")
