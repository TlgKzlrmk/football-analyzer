import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_manager import *
import os
from datetime import datetime, timedelta
import requests

# ==================== SAYFA YAPILANDIRMASI ====================
st.set_page_config(
    page_title="Eagle Pro - AI Futbol Analiz",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== ARKA PLAN GÖRSELİ (BEŞİKTAŞ STADI + DENİZ) ====================
# Değiştirmek istersen bg_image_url değişkenine kendi görsel URL'ni yaz.
bg_image_url = "https://www.istanbul.com.tr/images/places/vodafone-park-2.jpg"

page_bg_img = f"""
<style>
.stApp {{
    background-image: url("{bg_image_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.stApp::before {{
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.75);
    z-index: 0;
}}

.stApp > div {{
    position: relative;
    z-index: 1;
}}

h1, h2, h3, h4, p, div, span {{
    color: white !important;
}}

.stButton > button {{
    background-color: #f5a623 !important;
    color: #1a1a1a !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 12px 30px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(245, 166, 35, 0.4) !important;
}}

.stButton > button:hover {{
    transform: scale(1.05) !important;
    background-color: #ffb347 !important;
    box-shadow: 0 6px 20px rgba(245, 166, 35, 0.6) !important;
}}

.quick-btn > button {{
    background-color: rgba(255, 255, 255, 0.15) !important;
    color: white !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 20px !important;
    padding: 8px 20px !important;
    font-size: 14px !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: none !important;
}}

.quick-btn > button:hover {{
    background-color: rgba(245, 166, 35, 0.3) !important;
    border-color: #f5a623 !important;
    transform: scale(1.02) !important;
}}

.feature-card {{
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border-radius: 16px !important;
    padding: 20px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    text-align: center !important;
    transition: all 0.3s ease !important;
}}

.feature-card:hover {{
    transform: translateY(-5px) !important;
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: #f5a623 !important;
}}

.match-card {{
    background: rgba(0, 0, 0, 0.4) !important;
    backdrop-filter: blur(5px) !important;
    border-radius: 12px !important;
    padding: 12px 20px !important;
    border-left: 4px solid #f5a623 !important;
    margin-bottom: 10px !important;
}}

.league-card {{
    background: rgba(0, 0, 0, 0.3) !important;
    backdrop-filter: blur(5px) !important;
    border-radius: 12px !important;
    padding: 15px !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# ==================== SESSION STATE YÖNETİMİ ====================
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

# ==================== KARŞILAMA EKRANI (HOME) ====================
if st.session_state['page'] == 'home':

    # Üst banner
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown("""
            <div style='text-align: center; padding: 20px 0 10px 0;'>
                <h1 style='font-size: 60px; font-weight: 900; color: #f5a623; text-shadow: 0 4px 20px rgba(245, 166, 35, 0.3);'>
                    🦅 EAGLE PRO
                </h1>
                <p style='font-size: 22px; color: #e0e0e0; margin-top: -10px;'>
                    AI Futbol Analiz ve Tahmin
                </p>
                <p style='font-size: 16px; color: #b0b0b0;'>
                    Veriyle Konuşan Analiz | 40+ Lig | Yapay Zeka Tahmin
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Hızlı Erişim Butonları
    st.markdown("### ⚡ Hızlı Erişim")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button("🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier Lig", key="quick_pl"):
            st.session_state['quick_league'] = "Premier League"
            st.session_state['page'] = 'analysis'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button("🇪🇸 La Liga", key="quick_ll"):
            st.session_state['quick_league'] = "La Liga"
            st.session_state['page'] = 'analysis'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button("🇩🇪 Bundesliga", key="quick_bund"):
            st.session_state['quick_league'] = "Bundesliga"
            st.session_state['page'] = 'analysis'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col4:
        st.markdown('<div class="quick-btn">', unsafe_allow_html=True)
        if st.button("🏆 Şampiyonlar Ligi", key="quick_ucl"):
            st.session_state['quick_league'] = "Şampiyonlar Ligi"
            st.session_state['page'] = 'analysis'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Bugünün Maçları
    st.markdown("### 📅 Bugünün Maçları")
    try:
        sample_matches = [
            {"home": "Arsenal", "away": "Chelsea", "time": "19:30"},
            {"home": "Real Madrid", "away": "Barcelona", "time": "22:00"},
            {"home": "Bayern Münih", "away": "Dortmund", "time": "20:30"},
            {"home": "Milan", "away": "Inter", "time": "21:45"},
            {"home": "PSG", "away": "Marseille", "time": "20:00"},
        ]
        for m in sample_matches:
            st.markdown(f"""
                <div class="match-card">
                    <span style='font-size: 18px; font-weight: bold;'>{m['home']} vs {m['away']}</span>
                    <span style='float: right; color: #f5a623; font-weight: bold;'>{m['time']}</span>
                </div>
            """, unsafe_allow_html=True)
    except:
        st.info("Bugünün maç listesi şu anda hazırlanıyor. Lütfen daha sonra tekrar kontrol edin.")

    st.divider()

    # Lig Özetleri
    st.markdown("### 📊 Lig Özetleri")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="league-card">
                <h4 style='color: #f5a623;'>🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League</h4>
                <p>1. Liverpool (78p)<br>2. Arsenal (74p)<br>3. Manchester City (71p)</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="league-card">
                <h4 style='color: #f5a623;'>🇪🇸 La Liga</h4>
                <p>1. Real Madrid (76p)<br>2. Barcelona (72p)<br>3. Atletico Madrid (68p)</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Eagle Pro Özellikleri
    st.markdown("### 🧠 Eagle Pro ile Neler Yapabilirsin?")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="feature-card">
                <h3 style='font-size: 36px;'>📊</h3>
                <h4>40+ Lig</h4>
                <p style='font-size: 13px; color: #ccc;'>Avrupa'dan 40'tan fazla lig ve turnuva</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="feature-card">
                <h3 style='font-size: 36px;'>🎯</h3>
                <h4>xG & Olay Verisi</h4>
                <p style='font-size: 13px; color: #ccc;'>Beklenen gol, pas ağı, şut haritası</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3 style='font-size: 36px;'>📈</h3>
                <h4>Takım Stili</h4>
                <p style='font-size: 13px; color: #ccc;'>Pres, top kapma, pas stili analizi</p>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="feature-card">
                <h3 style='font-size: 36px;'>🤖</h3>
                <h4>AI Tahmin</h4>
                <p style='font-size: 13px; color: #ccc;'>XGBoost ile maç sonucu tahmini</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Keşfet Butonu
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Keşfetmeye Başla", use_container_width=True):
            st.session_state['page'] = 'analysis'
            st.rerun()

# ==================== ANALİZ EKRANI (ANALYSIS) ====================
else:
    # Hızlı erişimden gelen lig seçimini kontrol et
    if 'quick_league' in st.session_state:
        default_league = st.session_state['quick_league']
        # Seçimi temizle
        del st.session_state['quick_league']
    else:
        default_league = "Premier League"

    # ==================== LİG VE TURNUVALAR ====================
    LEAGUE_CODES = {
        "Premier League": "PL",
        "La Liga": "PD",
        "Bundesliga": "BL1",
        "Serie A": "SA",
        "Ligue 1": "FL1",
        "Championship": "ELC",
        "La Liga2": "SD",
        "Bundesliga 2": "BL2",
        "Serie B": "SB",
        "Ligue 2": "FL2",
        "Eredivisie": "ED",
        "Primeira Liga": "PPL",
        "Süper Lig": "SL",
        "Belçika Pro League": "BLG",
        "İskoçya Premier": "SCO",
        "Avusturya Bundesliga": "AUT",
        "İsviçre Super League": "SUI",
        "Yunanistan Super League": "GRE",
        "Rusya Premier": "RUS",
        "Ukrayna Premier": "UKR",
        "Danimarka Superliga": "DEN",
        "Norveç Eliteserien": "NOR",
        "İsveç Allsvenskan": "SWE",
        "Polonya Ekstraklasa": "POL",
        "Hırvatistan HNL": "CRO",
        "Sırbistan SuperLiga": "SRB",
        "Çek Cumhuriyeti 1. Liga": "CZE",
        "Romanya Liga 1": "ROU",
        "Macaristan NB I": "HUN",
        "Bulgaristan 1. Liga": "BUL",
        "Slovakya Super Liga": "SVK",
        "Slovenya PrvaLiga": "SVN",
        "İrlanda Premier Division": "IRL",
        "Şampiyonlar Ligi": "CL",
        "Avrupa Ligi": "EL",
        "Konferans Ligi": "ECL",
        "Dünya Kupası": "WC",
        "Avrupa Şampiyonası": "EC",
        "Copa America": "CAM",
        "Afrika Kupası": "AFC",
        "Asya Kupası": "ASC",
        "FA Cup": "FAC",
        "EFL Cup": "FLC",
        "DFB-Pokal": "DFB",
        "Coppa Italia": "CIT",
        "Coupe de France": "CDF",
        "Copa del Rey": "CDR",
        "Türkiye Kupası": "TKC",
    }

    SS_LEAGUES = {
        "Premier League": "premier-league",
        "La Liga": "la-liga",
        "Bundesliga": "bundesliga",
        "Serie A": "serie-a",
        "Ligue 1": "ligue-1",
        "Championship": "championship",
        "La Liga2": "la-liga-2",
        "Bundesliga 2": "bundesliga-2",
        "Serie B": "serie-b",
        "Ligue 2": "ligue-2",
        "Eredivisie": "eredivisie",
        "Primeira Liga": "portugal-primeira-liga",
        "Süper Lig": "süper-lig",
        "Belçika Pro League": "belgian-pro-league",
        "İskoçya Premier": "scottish-premiership",
        "Avusturya Bundesliga": "austrian-bundesliga",
        "İsviçre Super League": "swiss-super-league",
        "Yunanistan Super League": "greek-super-league",
        "Rusya Premier": "russian-premier-league",
        "Ukrayna Premier": "ukrainian-premier-league",
        "Danimarka Superliga": "danish-superliga",
        "Norveç Eliteserien": "norwegian-eliteserien",
        "İsveç Allsvenskan": "swedish-allsvenskan",
        "Polonya Ekstraklasa": "polish-ekstraklasa",
        "Hırvatistan HNL": "croatian-hnl",
        "Sırbistan SuperLiga": "serbian-superliga",
        "Çek Cumhuriyeti 1. Liga": "czech-1-liga",
        "Romanya Liga 1": "romanian-liga-1",
        "Macaristan NB I": "hungarian-nb-i",
        "Bulgaristan 1. Liga": "bulgarian-1-liga",
        "Slovakya Super Liga": "slovak-super-liga",
        "Slovenya PrvaLiga": "slovenian-prvaliga",
        "İrlanda Premier Division": "irish-premier-division",
    }

    ALL_LEAGUES = list(LEAGUE_CODES.keys()) + [k for k in SS_LEAGUES.keys() if k not in LEAGUE_CODES]
    ALL_LEAGUES = sorted(set(ALL_LEAGUES))

    # Başlık
    st.title("🦅 Eagle Pro - AI Futbol Analiz ve Tahmin")
    st.markdown("### Top 30+ Lig, 2. Ligler, Kupalar, UEFA & FIFA - Veriyle Konuşan Analiz")

    # Geri dönüş butonu
    if st.button("🏠 Ana Sayfaya Dön"):
        st.session_state['page'] = 'home'
        st.rerun()

    # Lig seçimi
    if default_league in ALL_LEAGUES:
        league_name = st.selectbox("🏆 Lig/Turnuva Seç", ALL_LEAGUES, index=ALL_LEAGUES.index(default_league))
    else:
        league_name = st.selectbox("🏆 Lig/Turnuva Seç", ALL_LEAGUES)

    # ==================== PUAN DURUMU ====================
    if st.button("📊 Puan Durumunu Göster"):
        with st.spinner("Veri çekiliyor..."):
            if league_name in LEAGUE_CODES:
                league_code = LEAGUE_CODES[league_name]
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
                    st.error("Football-Data.org'dan puan durumu alınamadı. Sports-skills deneniyor...")
                    ss_id = SS_LEAGUES.get(league_name)
                    if ss_id:
                        ss_data = get_ss_standings(ss_id)
                        if ss_data and "standings" in ss_data:
                            standings = ss_data["standings"]
                            if isinstance(standings, list) and len(standings) > 0:
                                first = standings[0]
                                entries = first.get("entries", first.get("table", []))
                                if entries:
                                    df = pd.DataFrame([{
                                        "Sıra": item.get("rank") or item.get("position", ""),
                                        "Takım": item.get("team", {}).get("name", "") if isinstance(item.get("team"), dict) else str(item.get("team", "")),
                                        "O": item.get("played") or item.get("playedGames", ""),
                                        "G": item.get("win") or item.get("won", ""),
                                        "B": item.get("draw", ""),
                                        "M": item.get("lose") or item.get("lost", ""),
                                        "A": item.get("goalsFor") or item.get("gf", ""),
                                        "Y": item.get("goalsAgainst") or item.get("ga", ""),
                                        "Puan": item.get("points", ""),
                                        "Avans": item.get("goalDifference") or item.get("goalDiff", "")
                                    } for item in entries])
                                    st.dataframe(df, use_container_width=True)
                                else:
                                    st.warning("Sports-skills'ten tablo verisi alınamadı.")
                            else:
                                st.warning("Sports-skills'ten standings verisi boş.")
                        else:
                            st.error("Her iki kaynaktan da veri alınamadı.")
            else:
                ss_id = SS_LEAGUES.get(league_name)
                if ss_id:
                    ss_data = get_ss_standings(ss_id)
                    if ss_data and "standings" in ss_data:
                        standings = ss_data["standings"]
                        if isinstance(standings, list) and len(standings) > 0:
                            first = standings[0]
                            entries = first.get("entries", first.get("table", []))
                            if entries:
                                df = pd.DataFrame([{
                                    "Sıra": item.get("rank") or item.get("position", ""),
                                    "Takım": item.get("team", {}).get("name", "") if isinstance(item.get("team"), dict) else str(item.get("team", "")),
                                    "O": item.get("played") or item.get("playedGames", ""),
                                    "G": item.get("win") or item.get("won", ""),
                                    "B": item.get("draw", ""),
                                    "M": item.get("lose") or item.get("lost", ""),
                                    "A": item.get("goalsFor") or item.get("gf", ""),
                                    "Y": item.get("goalsAgainst") or item.get("ga", ""),
                                    "Puan": item.get("points", ""),
                                    "Avans": item.get("goalDifference") or item.get("goalDiff", "")
                                } for item in entries])
                                st.dataframe(df, use_container_width=True)
                            else:
                                st.warning("Sports-skills'ten tablo verisi alınamadı.")
                        else:
                            st.warning("Sports-skills'ten standings verisi boş.")
                    else:
                        st.error("Sports-skills'ten veri alınamadı.")
                else:
                    st.error(f"'{league_name}' için veri kaynağı bulunamadı.")

    # ==================== UNDERSTAT xG ====================
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
                    st.warning("xG verisi alınamadı.")

    # ==================== FBREF ====================
    if st.button("📈 Takım İstatistikleri (FBref)"):
        with st.spinner("Veri çekiliyor (sports-skills üzerinden)..."):
            for season in ["2024", "2023"]:
                df = get_fbref_team_stats(league_name, season)
                if not df.empty and "Hata" not in df.columns:
                    st.success(f"{season} sezonu verisi başarıyla çekildi!")
                    if "team" in df.columns:
                        df["team_name"] = df["team"].apply(
                            lambda x: x.get("name", str(x)) if isinstance(x, dict) else str(x)
                        )
                        cols = ["position", "team_name", "played", "won", "drawn", "lost", 
                                "goals_for", "goals_against", "goal_difference", "points"]
                        df = df[[c for c in cols if c in df.columns]]
                        df.columns = ["Sıra", "Takım", "O", "G", "B", "M", "A", "Y", "Avans", "Puan"]
                    else:
                        df.columns = [col.replace("_", " ").title() for col in df.columns]
                    st.dataframe(df, use_container_width=True)
                    break
                else:
                    if not df.empty and "Hata" in df.columns:
                        st.warning(f"{season}: {df['Hata'].iloc[0]}")
                    else:
                        st.warning(f"{season} sezonu için veri alınamadı.")
            else:
                st.error("Hiçbir sezon için veri alınamadı.")

    # ==================== SPORTS-SKILLS TEST ====================
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

    # ==================== STATSBOMB ====================
    st.markdown("---")
    st.subheader("⚽ StatsBomb Olay Bazlı Veri (Açık Veri)")
    TOURNAMENTS = {
        "FIFA Dünya Kupası 2022": {"competition_id": 43, "season_id": 106},
        "UEFA Şampiyonlar Ligi 2021-22": {"competition_id": 16, "season_id": 4},
        "UEFA Şampiyonlar Ligi 2022-23": {"competition_id": 16, "season_id": 14},
        "Premier League 2021-22": {"competition_id": 2, "season_id": 4},
        "Premier League 2022-23": {"competition_id": 2, "season_id": 14},
        "La Liga 2021-22": {"competition_id": 11, "season_id": 4},
        "La Liga 2022-23": {"competition_id": 11, "season_id": 14},
        "Bundesliga 2021-22": {"competition_id": 9, "season_id": 4},
        "Bundesliga 2022-23": {"competition_id": 9, "season_id": 14},
        "Serie A 2021-22": {"competition_id": 23, "season_id": 4},
        "Serie A 2022-23": {"competition_id": 23, "season_id": 14},
        "Ligue 1 2021-22": {"competition_id": 7, "season_id": 4},
        "Ligue 1 2022-23": {"competition_id": 7, "season_id": 14},
    }
    selected_tournament = st.selectbox("🏆 Turnuva Seç", list(TOURNAMENTS.keys()))
    tournament_info = TOURNAMENTS[selected_tournament]
    competition_id = tournament_info["competition_id"]
    season_id = tournament_info["season_id"]

    if st.button("📋 Maçları Listele"):
        with st.spinner("StatsBomb'dan maçlar çekiliyor..."):
            matches = get_statsbomb_matches(competition_id, season_id)
            if not matches.empty:
                st.success(f"{len(matches)} maç bulundu!")
                match_options = []
                for idx, row in matches.iterrows():
                    home_team = row.get('home_team', {})
                    if isinstance(home_team, dict):
                        home = home_team.get('name', home_team.get('team_name', str(home_team)))
                    else:
                        home = str(home_team) if home_team else '?'
                    away_team = row.get('away_team', {})
                    if isinstance(away_team, dict):
                        away = away_team.get('name', away_team.get('team_name', str(away_team)))
                    else:
                        away = str(away_team) if away_team else '?'
                    match_date = row.get('match_date', 'Tarih yok')
                    match_id = row.get('match_id', row.get('id', ''))
                    match_options.append({
                        "display": f"{home} vs {away} ({match_date})",
                        "match_id": match_id,
                        "home": home,
                        "away": away
                    })
                st.session_state['match_options'] = match_options
            else:
                st.error("Maç listesi alınamadı.")

    if 'match_options' in st.session_state and st.session_state['match_options']:
        match_options = st.session_state['match_options']
        selected_match_label = st.selectbox(
            "📅 Maç Seç",
            options=[m["display"] for m in match_options],
            key="sb_match_select"
        )
        selected_match = next(m for m in match_options if m["display"] == selected_match_label)
        if st.button(f"🚀 {selected_match['home']} vs {selected_match['away']} Olaylarını Göster", key="show_events"):
            with st.spinner("Olaylar çekiliyor..."):
                events = get_statsbomb_events(selected_match["match_id"])
                if not events.empty:
                    st.success(f"{len(events)} olay bulundu!")
                    st.session_state['events'] = events
                    st.session_state['selected_match'] = selected_match
                    st.session_state['match_id'] = selected_match["match_id"]
                    event_types = events['type'].unique().tolist()
                    selected_types = st.multiselect(
                        "🔍 Olay Türlerini Filtrele",
                        options=event_types,
                        default=event_types[:5] if len(event_types) >= 5 else event_types,
                        key="event_types_filter"
                    )
                    if selected_types:
                        filtered_events = events[events['type'].isin(selected_types)]
                        st.dataframe(filtered_events, use_container_width=True)
                    else:
                        st.dataframe(events, use_container_width=True)
                    st.subheader("📊 Olay Özeti")
                    summary = events['type'].value_counts().reset_index()
                    summary.columns = ['Olay Türü', 'Sayı']
                    st.dataframe(summary, use_container_width=True)
                else:
                    st.warning("Bu maç için olay verisi bulunamadı.")
    else:
        if 'match_options' not in st.session_state or not st.session_state['match_options']:
            st.info("Lütfen yukarıdan bir turnuva seçip 'Maçları Listele' butonuna tıklayın.")

    # ==================== PAS AĞI ====================
    st.markdown("---")
    st.subheader("🔗 Pas Ağı Analizi (StatsBomb)")
    if 'selected_match' in st.session_state and st.session_state['selected_match']:
        selected_match = st.session_state['selected_match']
        match_id = st.session_state.get('match_id', None)
        if st.button(f"📊 {selected_match['home']} - {selected_match['away']} Pas Ağını Göster", key="show_pass_network"):
            if not match_id:
                st.warning("Önce yukarıdan bir maç seçip 'Olayları Göster' butonuna tıklayın.")
            else:
                with st.spinner("Pas verileri işleniyor..."):
                    try:
                        events = st.session_state.get('events', None)
                        if events is None or events.empty:
                            events = get_statsbomb_events(match_id)
                        if events.empty:
                            st.warning("Bu maç için olay verisi bulunamadı.")
                            st.stop()
                        passes = events[events['type'] == 'Pass'].copy()
                        if passes.empty:
                            st.warning("Bu maçta pas verisi bulunamadı.")
                            st.stop()
                        import numpy as np
                        player_positions = {}
                        pass_counts = {}
                        for idx, row in passes.iterrows():
                            try:
                                player = None
                                if 'player' in row and isinstance(row['player'], dict):
                                    player = str(row['player'].get('name', ''))
                                elif 'player_name' in row:
                                    player = str(row['player_name'])
                                elif 'player' in row and isinstance(row['player'], str):
                                    player = str(row['player'])
                                elif 'player_id' in row:
                                    player = f"P{row['player_id']}"
                                if not player or player == '' or player == 'nan':
                                    continue
                                if 'location' not in row:
                                    continue
                                loc = row['location']
                                if not isinstance(loc, (list, tuple)) or len(loc) < 2:
                                    continue
                                try:
                                    x = float(loc[0])
                                    y = float(loc[1])
                                except (ValueError, TypeError):
                                    continue
                                if player not in player_positions:
                                    player_positions[player] = {'x': [], 'y': [], 'total': 0}
                                player_positions[player]['x'].append(x)
                                player_positions[player]['y'].append(y)
                                player_positions[player]['total'] += 1
                                recipient = None
                                if 'pass' in row and isinstance(row['pass'], dict):
                                    pdata = row['pass']
                                    if 'recipient' in pdata and isinstance(pdata['recipient'], dict):
                                        recipient = str(pdata['recipient'].get('name', ''))
                                    elif 'recipient_name' in pdata:
                                        recipient = str(pdata['recipient_name'])
                                    elif 'recipient' in pdata and isinstance(pdata['recipient'], str):
                                        recipient = str(pdata['recipient'])
                                elif 'pass_recipient' in row:
                                    recipient = str(row['pass_recipient'])
                                elif 'recipient' in row:
                                    recipient = str(row['recipient'])
                                if recipient and recipient != '' and recipient != 'nan' and recipient != player:
                                    key = tuple(sorted([player, recipient]))
                                    if key not in pass_counts:
                                        pass_counts[key] = 0
                                    pass_counts[key] += 1
                            except:
                                continue
                        active = [p for p, data in player_positions.items() if data['total'] >= 3]
                        if len(active) < 2:
                            st.warning(f"Yeterli pas verisi yok (en az 3 pas yapan {len(active)} oyuncu, 2 gerekli).")
                            st.stop()
                        positions = {}
                        for p in active:
                            data = player_positions[p]
                            try:
                                mean_x = float(np.mean(data['x']))
                                mean_y = float(np.mean(data['y']))
                            except:
                                continue
                            positions[p] = {'x': mean_x, 'y': mean_y, 'total': data['total']}
                        if not positions:
                            st.warning("Pozisyon hesaplanamadı.")
                            st.stop()
                        connections = {}
                        for (p1, p2), count in pass_counts.items():
                            if p1 in positions and p2 in positions and count >= 2:
                                connections[(p1, p2)] = count
                        if not connections:
                            st.warning("Yeterli pas bağlantısı yok (en az 2 pas).")
                            st.stop()
                        fig, ax = plt.subplots(figsize=(12, 8))
                        ax.set_facecolor('#22312b')
                        ax.plot([0, 120, 120, 0, 0], [0, 0, 80, 80, 0], color='#c7d5cc', linewidth=2)
                        ax.plot([60, 60], [0, 80], color='#c7d5cc', linewidth=2)
                        circle = plt.Circle((60, 40), 9.15, color='#c7d5cc', fill=False, linewidth=2)
                        ax.add_patch(circle)
                        ax.plot([0, 16.5, 16.5, 0], [30.34, 30.34, 49.66, 49.66], color='#c7d5cc', linewidth=2)
                        ax.plot([120, 103.5, 103.5, 120], [30.34, 30.34, 49.66, 49.66], color='#c7d5cc', linewidth=2)
                        ax.plot([0, 5.5, 5.5, 0], [34.34, 34.34, 45.66, 45.66], color='#c7d5cc', linewidth=2)
                        ax.plot([120, 114.5, 114.5, 120], [34.34, 34.34, 45.66, 45.66], color='#c7d5cc', linewidth=2)
                        ax.scatter(11, 40, color='#c7d5cc', s=50, zorder=1)
                        ax.scatter(109, 40, color='#c7d5cc', s=50, zorder=1)
                        for player, pos in positions.items():
                            x = pos['x']
                            y = pos['y']
                            size = 150 + (pos['total'] * 3)
                            ax.scatter(x, y, s=size, color='#00ffcc', edgecolors='white', zorder=5, alpha=0.8)
                            ax.text(x, y-3, player, color='white', ha='center', fontsize=8, fontweight='bold')
                        for (p1, p2), count in connections.items():
                            if p1 in positions and p2 in positions:
                                x1 = positions[p1]['x']
                                y1 = positions[p1]['y']
                                x2 = positions[p2]['x']
                                y2 = positions[p2]['y']
                                linewidth = 1 + (count / 3)
                                alpha = min(0.8, 0.2 + (count / 10))
                                ax.plot([x1, x2], [y1, y2], color='cyan', linewidth=linewidth, alpha=alpha, zorder=2)
                        ax.set_xlim(0, 120)
                        ax.set_ylim(0, 80)
                        ax.set_aspect('equal')
                        ax.axis('off')
                        ax.set_title(f"Pas Ağı - {selected_match['home']} vs {selected_match['away']}", color='white', fontsize=14)
                        st.pyplot(fig)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Toplam Pas", len(passes))
                        with col2:
                            st.metric("Aktif Oyuncu", len(active))
                        with col3:
                            if positions:
                                most = max(positions.items(), key=lambda x: x[1]['total'])
                                st.metric("En Çok Pas", most[0])
                    except Exception as e:
                        st.error(f"Pas ağı oluşturulurken hata: {str(e)}")
                        with st.expander("🔍 Hata Ayıklama: Ham Olay Verisi (İlk 5)"):
                            if 'events' in st.session_state:
                                st.dataframe(st.session_state['events'].head(5))
    else:
        st.info("Lütfen yukarıdan bir turnuva seçin, 'Maçları Listele' butonuna tıklayın ve bir maç seçin, ardından 'Olayları Göster' butonuna tıklayın.")

    # ==================== MAÇ ÖZET RAPORU ====================
    st.markdown("---")
    st.subheader("📋 Maç Özet Raporu (StatsBomb)")
    if 'selected_match' in st.session_state and st.session_state['selected_match']:
        selected_match = st.session_state['selected_match']
        match_id = st.session_state.get('match_id', None)
        if st.button(f"📄 {selected_match['home']} - {selected_match['away']} Maç Özet Raporu Oluştur", key="generate_match_report"):
            if not match_id:
                st.warning("Önce yukarıdan bir maç seçip 'Olayları Göster' butonuna tıklayın.")
            else:
                with st.spinner("Maç özet raporu oluşturuluyor..."):
                    try:
                        events = st.session_state.get('events', None)
                        if events is None or events.empty:
                            events = get_statsbomb_events(match_id)
                        if events.empty:
                            st.warning("Bu maç için olay verisi bulunamadı.")
                            st.stop()
                        st.subheader("📌 Maç Bilgileri")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("🏠 Ev Sahibi", selected_match['home'])
                        with col2:
                            st.metric("✈️ Deplasman", selected_match['away'])
                        with col3:
                            match_date = events['event_date'].iloc[0] if 'event_date' in events.columns else 'Tarih yok'
                            st.metric("📅 Tarih", match_date[:10] if len(str(match_date)) > 10 else str(match_date))
                        st.divider()
                        st.subheader("📊 Temel İstatistikler")
                        passes = events[events['type'] == 'Pass'].copy() if 'type' in events.columns else pd.DataFrame()
                        shots = events[events['type'] == 'Shot'].copy() if 'type' in events.columns else pd.DataFrame()
                        carries = events[events['type'] == 'Carry'].copy() if 'type' in events.columns else pd.DataFrame()
                        pressures = events[events['type'] == 'Pressure'].copy() if 'type' in events.columns else pd.DataFrame()
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("🔄 Toplam Pas", len(passes))
                        with col2:
                            st.metric("🎯 Toplam Şut", len(shots))
                        with col3:
                            st.metric("🔥 Pres Sayısı", len(pressures))
                        with col4:
                            st.metric("🏃 Top Taşıma", len(carries))
                        st.divider()
                        st.subheader("🎯 xG ve Şut Haritası")
                        if not shots.empty:
                            shot_xg = []
                            for idx, row in shots.iterrows():
                                shot_data = row.get('shot', {})
                                if isinstance(shot_data, dict):
                                    xg = shot_data.get('statsbomb_xg', None)
                                    if xg is not None:
                                        try:
                                            shot_xg.append(float(xg))
                                        except:
                                            pass
                            if shot_xg:
                                total_xg = sum(shot_xg)
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("⚡ Toplam xG", round(total_xg, 2))
                                with col2:
                                    st.metric("📊 Ortalama xG/Şut", round(total_xg / len(shot_xg), 2) if shot_xg else 0)
                            pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
                            fig, ax = pitch.draw(figsize=(10, 7))
                            for idx, row in shots.iterrows():
                                location = row.get('location', [])
                                if len(location) >= 2:
                                    x = float(location[0]) if location[0] is not None else None
                                    y = float(location[1]) if location[1] is not None else None
                                    if x is not None and y is not None:
                                        shot_data = row.get('shot', {})
                                        outcome = shot_data.get('outcome', {}).get('name', '') if isinstance(shot_data, dict) else ''
                                        is_goal = outcome == 'Goal'
                                        color = 'red' if is_goal else 'blue'
                                        ax.scatter(x, y, s=150, color=color, alpha=0.7, edgecolors='white')
                                        if isinstance(shot_data, dict):
                                            xg_val = shot_data.get('statsbomb_xg', None)
                                            if xg_val is not None:
                                                ax.text(x+2, y+2, f"{float(xg_val):.2f}", color='white', fontsize=7)
                            ax.set_title(f"Şut Haritası - {selected_match['home']} vs {selected_match['away']}", color='white', fontsize=14)
                            st.pyplot(fig)
                        else:
                            st.info("Bu maçta şut verisi bulunamadı.")
                        st.divider()
                        st.subheader("🔗 Pas Ağı")
                        if not passes.empty:
                            import numpy as np
                            player_positions = {}
                            pass_counts = {}
                            for idx, row in passes.iterrows():
                                player = None
                                if 'player' in row and isinstance(row['player'], dict):
                                    player = row['player'].get('name', None)
                                elif 'player_name' in row:
                                    player = row['player_name']
                                elif 'player' in row and isinstance(row['player'], str):
                                    player = row['player']
                                if not player:
                                    continue
                                loc = row.get('location', [])
                                if len(loc) >= 2:
                                    try:
                                        x = float(loc[0])
                                        y = float(loc[1])
                                    except:
                                        continue
                                else:
                                    continue
                                if player not in player_positions:
                                    player_positions[player] = {'x': [], 'y': [], 'total': 0}
                                player_positions[player]['x'].append(x)
                                player_positions[player]['y'].append(y)
                                player_positions[player]['total'] += 1
                                recipient = None
                                if 'pass' in row and isinstance(row['pass'], dict):
                                    pdata = row['pass']
                                    if 'recipient' in pdata and isinstance(pdata['recipient'], dict):
                                        recipient = pdata['recipient'].get('name', None)
                                if recipient and recipient != player:
                                    key = tuple(sorted([player, recipient]))
                                    if key not in pass_counts:
                                        pass_counts[key] = 0
                                    pass_counts[key] += 1
                            active_players = [p for p, data in player_positions.items() if data['total'] >= 3]
                            if len(active_players) >= 2:
                                positions = {}
                                for p in active_players:
                                    data = player_positions[p]
                                    positions[p] = {
                                        'x': np.mean(data['x']),
                                        'y': np.mean(data['y']),
                                        'total': data['total']
                                    }
                                connections = {k: v for k, v in pass_counts.items() 
                                               if k[0] in active_players and k[1] in active_players and v >= 2}
                                if connections:
                                    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
                                    fig, ax = pitch.draw(figsize=(12, 8))
                                    for player, pos in positions.items():
                                        x = pos['x']
                                        y = pos['y']
                                        size = 150 + (pos['total'] * 3)
                                        ax.scatter(x, y, s=size, color='#00ffcc', edgecolors='white', zorder=5, alpha=0.8)
                                        ax.text(x, y-3, player, color='white', ha='center', fontsize=8, fontweight='bold')
                                    for (p1, p2), count in connections.items():
                                        if p1 in positions and p2 in positions:
                                            x1 = positions[p1]['x']
                                            y1 = positions[p1]['y']
                                            x2 = positions[p2]['x']
                                            y2 = positions[p2]['y']
                                            linewidth = 1 + (count / 3)
                                            alpha = min(0.8, 0.2 + (count / 10))
                                            ax.plot([x1, x2], [y1, y2], color='cyan', linewidth=linewidth, alpha=alpha, zorder=2)
                                    ax.set_title(f"Pas Ağı - {selected_match['home']} vs {selected_match['away']}", color='white', fontsize=14)
                                    st.pyplot(fig)
                                else:
                                    st.info("Pas bağlantıları yeterli değil.")
                            else:
                                st.info("Yeterli pas verisi yok.")
                        else:
                            st.info("Bu maçta pas verisi bulunamadı.")
                        st.divider()
                        st.subheader("🏅 Öne Çıkan Oyuncular")
                        if not passes.empty:
                            pass_counts_by_player = {}
                            for idx, row in passes.iterrows():
                                player = None
                                if 'player' in row and isinstance(row['player'], dict):
                                    player = row['player'].get('name', None)
                                elif 'player_name' in row:
                                    player = row['player_name']
                                elif 'player' in row and isinstance(row['player'], str):
                                    player = row['player']
                                if player:
                                    pass_counts_by_player[player] = pass_counts_by_player.get(player, 0) + 1
                            if pass_counts_by_player:
                                top_passers = sorted(pass_counts_by_player.items(), key=lambda x: x[1], reverse=True)[:5]
                                st.write("**En Çok Pas Yapan Oyuncular**")
                                df_passes = pd.DataFrame(top_passers, columns=["Oyuncu", "Pas Sayısı"])
                                st.dataframe(df_passes, use_container_width=True, hide_index=True)
                        if not shots.empty:
                            shot_counts_by_player = {}
                            for idx, row in shots.iterrows():
                                player = None
                                if 'player' in row and isinstance(row['player'], dict):
                                    player = row['player'].get('name', None)
                                elif 'player_name' in row:
                                    player = row['player_name']
                                elif 'player' in row and isinstance(row['player'], str):
                                    player = row['player']
                                if player:
                                    shot_counts_by_player[player] = shot_counts_by_player.get(player, 0) + 1
                            if shot_counts_by_player:
                                top_shooters = sorted(shot_counts_by_player.items(), key=lambda x: x[1], reverse=True)[:5]
                                st.write("**En Çok Şut Çeken Oyuncular**")
                                df_shots = pd.DataFrame(top_shooters, columns=["Oyuncu", "Şut Sayısı"])
                                st.dataframe(df_shots, use_container_width=True, hide_index=True)
                        st.success("✅ Maç özet raporu başarıyla oluşturuldu!")
                    except Exception as e:
                        st.error(f"Rapor oluşturulurken hata: {str(e)}")
                        with st.expander("🔍 Hata Ayıklama: Ham Olay Verisi (İlk 5)"):
                            if 'events' in st.session_state:
                                st.dataframe(st.session_state['events'].head(5))
    else:
        st.info("Lütfen yukarıdan bir turnuva seçin, 'Maçları Listele' butonuna tıklayın ve bir maç seçin, ardından 'Olayları Göster' butonuna tıklayın.")

    # ==================== TAKIM STİLİ ANALİZİ ====================
    st.markdown("---")
    st.subheader("📊 Takım Stili Analizi (StatsBomb)")
    if 'selected_match' in st.session_state and st.session_state['selected_match']:
        selected_match = st.session_state['selected_match']
        match_id = st.session_state.get('match_id', None)
        if st.button(f"📊 {selected_match['home']} - {selected_match['away']} Takım Stili Analizi", key="team_style_analysis"):
            if not match_id:
                st.warning("Önce yukarıdan bir maç seçip 'Olayları Göster' butonuna tıklayın.")
            else:
                with st.spinner("Takım stili analizi yapılıyor..."):
                    try:
                        events = st.session_state.get('events', None)
                        if events is None or events.empty:
                            events = get_statsbomb_events(match_id)
                        if events.empty:
                            st.warning("Bu maç için olay verisi bulunamadı.")
                            st.stop()
                        teams = []
                        if 'team' in events.columns:
                            teams = events['team'].unique().tolist()
                        elif 'team_name' in events.columns:
                            teams = events['team_name'].unique().tolist()
                        if len(teams) < 2:
                            st.warning("Takım bilgileri bulunamadı.")
                            st.stop()
                        home_team = teams[0] if teams else selected_match['home']
                        away_team = teams[1] if len(teams) > 1 else selected_match['away']
                        home_events = events[events['team'] == home_team].copy() if 'team' in events.columns else events[events['team_name'] == home_team].copy()
                        away_events = events[events['team'] == away_team].copy() if 'team' in events.columns else events[events['team_name'] == away_team].copy()
                        def calculate_style_metrics(team_events, team_name):
                            metrics = {}
                            passes = team_events[team_events['type'] == 'Pass'].copy() if 'type' in team_events.columns else pd.DataFrame()
                            total_passes = len(passes)
                            metrics['Toplam Pas'] = total_passes
                            if total_passes > 0:
                                successful_passes = 0
                                for idx, row in passes.iterrows():
                                    pass_data = row.get('pass', {})
                                    if isinstance(pass_data, dict):
                                        if pass_data.get('outcome', {}).get('name') != 'Incomplete':
                                            successful_passes += 1
                                metrics['Pas Başarı Oranı'] = round((successful_passes / total_passes) * 100, 1)
                            else:
                                metrics['Pas Başarı Oranı'] = 0
                            pressures = team_events[team_events['type'] == 'Pressure'].copy() if 'type' in team_events.columns else pd.DataFrame()
                            metrics['Toplam Pres'] = len(pressures)
                            shots = team_events[team_events['type'] == 'Shot'].copy() if 'type' in team_events.columns else pd.DataFrame()
                            metrics['Toplam Şut'] = len(shots)
                            shot_xg = []
                            for idx, row in shots.iterrows():
                                shot_data = row.get('shot', {})
                                if isinstance(shot_data, dict):
                                    xg = shot_data.get('statsbomb_xg', None)
                                    if xg is not None:
                                        try:
                                            shot_xg.append(float(xg))
                                        except:
                                            pass
                            metrics['Toplam xG'] = round(sum(shot_xg), 2) if shot_xg else 0
                            carries = team_events[team_events['type'] == 'Carry'].copy() if 'type' in team_events.columns else pd.DataFrame()
                            metrics['Top Taşıma'] = len(carries)
                            high_pressures = 0
                            for idx, row in pressures.iterrows():
                                loc = row.get('location', [])
                                if len(loc) >= 2:
                                    try:
                                        x = float(loc[0])
                                        if x > 60:
                                            high_pressures += 1
                                    except:
                                        pass
                            metrics['Rakip Yarı Sahada Pres'] = high_pressures
                            metrics['Rakip Yarı Sahada Pres Oranı'] = round((high_pressures / metrics['Toplam Pres'] * 100), 1) if metrics['Toplam Pres'] > 0 else 0
                            ball_recoveries = team_events[team_events['type'] == 'Ball Recovery'].copy() if 'type' in team_events.columns else pd.DataFrame()
                            recovery_zones = {'kendi_yarı': 0, 'orta_saha': 0, 'rakip_yarı': 0}
                            for idx, row in ball_recoveries.iterrows():
                                loc = row.get('location', [])
                                if len(loc) >= 2:
                                    try:
                                        x = float(loc[0])
                                        if x < 40:
                                            recovery_zones['kendi_yarı'] += 1
                                        elif x < 80:
                                            recovery_zones['orta_saha'] += 1
                                        else:
                                            recovery_zones['rakip_yarı'] += 1
                                    except:
                                        pass
                            metrics['Top Kapma - Kendi Yarı'] = recovery_zones['kendi_yarı']
                            metrics['Top Kapma - Orta Saha'] = recovery_zones['orta_saha']
                            metrics['Top Kapma - Rakip Yarı'] = recovery_zones['rakip_yarı']
                            metrics['Aksiyon Hızı (Skor)'] = "Orta"
                            return metrics
                        home_metrics = calculate_style_metrics(home_events, home_team)
                        away_metrics = calculate_style_metrics(away_events, away_team)
                        st.subheader(f"⚽ {home_team} vs {away_team} - Stil Karşılaştırması")
                        comparison_data = {
                            "Metrik": list(home_metrics.keys()),
                            home_team: list(home_metrics.values()),
                            away_team: list(away_metrics.values())
                        }
                        df_comparison = pd.DataFrame(comparison_data)
                        st.dataframe(df_comparison, use_container_width=True, hide_index=True)
                        st.divider()
                        col1, col2 = st.columns(2)
                        with col1:
                            st.subheader(f"📍 {home_team} - Top Kapma Bölgeleri")
                            recovery_data = {
                                'Bölge': ['Kendi Yarı', 'Orta Saha', 'Rakip Yarı'],
                                'Sayı': [
                                    home_metrics['Top Kapma - Kendi Yarı'],
                                    home_metrics['Top Kapma - Orta Saha'],
                                    home_metrics['Top Kapma - Rakip Yarı']
                                ]
                            }
                            if sum(recovery_data['Sayı']) > 0:
                                fig, ax = plt.subplots()
                                ax.pie(recovery_data['Sayı'], labels=recovery_data['Bölge'], autopct='%1.1f%%', 
                                       colors=['#ff6b6b', '#feca57', '#48dbfb'], startangle=90)
                                ax.axis('equal')
                                st.pyplot(fig)
                            else:
                                st.info("Top kapma verisi yok.")
                        with col2:
                            st.subheader(f"📍 {away_team} - Top Kapma Bölgeleri")
                            recovery_data = {
                                'Bölge': ['Kendi Yarı', 'Orta Saha', 'Rakip Yarı'],
                                'Sayı': [
                                    away_metrics['Top Kapma - Kendi Yarı'],
                                    away_metrics['Top Kapma - Orta Saha'],
                                    away_metrics['Top Kapma - Rakip Yarı']
                                ]
                            }
                            if sum(recovery_data['Sayı']) > 0:
                                fig, ax = plt.subplots()
                                ax.pie(recovery_data['Sayı'], labels=recovery_data['Bölge'], autopct='%1.1f%%', 
                                       colors=['#ff6b6b', '#feca57', '#48dbfb'], startangle=90)
                                ax.axis('equal')
                                st.pyplot(fig)
                            else:
                                st.info("Top kapma verisi yok.")
                        st.divider()
                        st.subheader("🔥 Pres Yüksekliği Karşılaştırması")
                        pres_data = {
                            'Takım': [home_team, away_team],
                            'Rakip Yarı Sahada Pres Oranı (%)': [
                                home_metrics['Rakip Yarı Sahada Pres Oranı'],
                                away_metrics['Rakip Yarı Sahada Pres Oranı']
                            ]
                        }
                        df_pres = pd.DataFrame(pres_data)
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.bar(df_pres['Takım'], df_pres['Rakip Yarı Sahada Pres Oranı (%)'], color=['#00ffcc', '#ff6b6b'])
                        ax.set_ylabel('Rakip Yarı Sahada Pres Oranı (%)')
                        ax.set_title('Pres Yüksekliği Karşılaştırması')
                        ax.set_ylim(0, 100)
                        for i, v in enumerate(df_pres['Rakip Yarı Sahada Pres Oranı (%)']):
                            ax.text(i, v + 2, f"{v}%", ha='center', color='white')
                        st.pyplot(fig)
                        st.subheader("🎯 Pas Başarı Oranı Karşılaştırması")
                        pass_data = {
                            'Takım': [home_team, away_team],
                            'Pas Başarı Oranı (%)': [
                                home_metrics['Pas Başarı Oranı'],
                                away_metrics['Pas Başarı Oranı']
                            ]
                        }
                        df_pass = pd.DataFrame(pass_data)
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.bar(df_pass['Takım'], df_pass['Pas Başarı Oranı (%)'], color=['#00ffcc', '#ff6b6b'])
                        ax.set_ylabel('Pas Başarı Oranı (%)')
                        ax.set_title('Pas Başarı Oranı Karşılaştırması')
                        ax.set_ylim(0, 100)
                        for i, v in enumerate(df_pass['Pas Başarı Oranı (%)']):
                            ax.text(i, v + 2, f"{v}%", ha='center', color='white')
                        st.pyplot(fig)
                        st.success("✅ Takım stili analizi başarıyla tamamlandı!")
                    except Exception as e:
                        st.error(f"Takım stili analizi sırasında hata: {str(e)}")
                        with st.expander("🔍 Hata Ayıklama: Ham Olay Verisi (İlk 5)"):
                            if 'events' in st.session_state:
                                st.dataframe(st.session_state['events'].head(5))
    else:
        st.info("Lütfen yukarıdan bir turnuva seçin, 'Maçları Listele' butonuna tıklayın ve bir maç seçin, ardından 'Olayları Göster' butonuna tıklayın.")
