import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_manager import *
import os
from datetime import datetime, timedelta
import requests
import numpy as np

st.set_page_config(
    page_title="Eagle Pro - AI Futbol Analiz",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

bg_image_url = "https://www.istanbul.com.tr/images/places/vodafone-park-2.jpg"

st.markdown(f"""
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
    h1, h2, h3, h4, p, div, span, label {{
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
    }}
    .stButton > button:hover {{
        transform: scale(1.05) !important;
        background-color: #ffb347 !important;
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
    }}
    .feature-card {{
        background: rgba(255, 255, 255, 0.05) !important;
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
        border-radius: 12px !important;
        padding: 12px 20px !important;
        border-left: 4px solid #f5a623 !important;
        margin-bottom: 10px !important;
    }}
    .league-card {{
        background: rgba(0, 0, 0, 0.3) !important;
        border-radius: 12px !important;
        padding: 15px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }}
</style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state['page'] = 'home'

if st.session_state['page'] == 'home':

    st.markdown("""
        <div style='text-align: center; padding: 20px 0 10px 0;'>
            <h1 style='font-size: 60px; font-weight: 900; color: #f5a623; text-shadow: 0 4px 20px rgba(245, 166, 35, 0.3);'>
                EAGLE PRO
            </h1>
            <p style='font-size: 22px; color: #e0e0e0; margin-top: -10px;'>
                AI Futbol Analiz ve Tahmin
            </p>
            <p style='font-size: 16px; color: #b0b0b0;'>
                Veriyle Konusan Analiz | 40+ Lig | Yapay Zeka Tahmin
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Hizli Erisim")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("Premier Lig", key="quick_pl"):
            st.session_state['quick_league'] = "Premier League"
            st.session_state['page'] = 'analysis'
            st.rerun()
    with col2:
        if st.button("La Liga", key="quick_ll"):
            st.session_state['quick_league'] = "La Liga"
            st.session_state['page'] = 'analysis'
            st.rerun()
    with col3:
        if st.button("Bundesliga", key="quick_bund"):
            st.session_state['quick_league'] = "Bundesliga"
            st.session_state['page'] = 'analysis'
            st.rerun()
    with col4:
        if st.button("Sampiyonlar Ligi", key="quick_ucl"):
            st.session_state['quick_league'] = "Sampiyonlar Ligi"
            st.session_state['page'] = 'analysis'
            st.rerun()

    st.divider()

    st.markdown("### Bugunun Maclari")
    sample_matches = [
        {"home": "Arsenal", "away": "Chelsea", "time": "19:30"},
        {"home": "Real Madrid", "away": "Barcelona", "time": "22:00"},
        {"home": "Bayern Munih", "away": "Dortmund", "time": "20:30"},
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

    st.divider()

    st.markdown("### Lig Ozetleri")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
            <div class="league-card">
                <h4 style='color: #f5a623;'>Premier League</h4>
                <p>1. Liverpool (78p)<br>2. Arsenal (74p)<br>3. Manchester City (71p)</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="league-card">
                <h4 style='color: #f5a623;'>La Liga</h4>
                <p>1. Real Madrid (76p)<br>2. Barcelona (72p)<br>3. Atletico Madrid (68p)</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### Eagle Pro ile Neler Yapabilirsin?")
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
                <p style='font-size: 13px; color: #ccc;'>Beklenen gol, pas agi, sut haritasi</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="feature-card">
                <h3 style='font-size: 36px;'>📈</h3>
                <h4>Takim Stili</h4>
                <p style='font-size: 13px; color: #ccc;'>Pres, top kapma, pas stili analizi</p>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="feature-card">
                <h3 style='font-size: 36px;'>🤖</h3>
                <h4>AI Tahmin</h4>
                <p style='font-size: 13px; color: #ccc;'>XGBoost ile mac sonucu tahmini</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Kesfetmeye Basla", use_container_width=True):
            st.session_state['page'] = 'analysis'
            st.rerun()

else:

    if 'quick_league' in st.session_state:
        default_league = st.session_state['quick_league']
        del st.session_state['quick_league']
    else:
        default_league = "Premier League"

    LEAGUE_CODES = {
        "Premier League": "PL", "La Liga": "PD", "Bundesliga": "BL1",
        "Serie A": "SA", "Ligue 1": "FL1", "Championship": "ELC",
        "La Liga2": "SD", "Bundesliga 2": "BL2", "Serie B": "SB",
        "Ligue 2": "FL2", "Eredivisie": "ED", "Primeira Liga": "PPL",
        "Super Lig": "SL", "Belcika Pro League": "BLG", "Iskocya Premier": "SCO",
        "Avusturya Bundesliga": "AUT", "Isvicre Super League": "SUI",
        "Yunanistan Super League": "GRE", "Rusya Premier": "RUS",
        "Ukrayna Premier": "UKR", "Danimarka Superliga": "DEN",
        "Norvec Eliteserien": "NOR", "Isvec Allsvenskan": "SWE",
        "Polonya Ekstraklasa": "POL", "Hirvatistan HNL": "CRO",
        "Sirbistan SuperLiga": "SRB", "Cek Cumhuriyeti 1. Liga": "CZE",
        "Romanya Liga 1": "ROU", "Macaristan NB I": "HUN",
        "Bulgaristan 1. Liga": "BUL", "Slovakya Super Liga": "SVK",
        "Slovenya PrvaLiga": "SVN", "Irlanda Premier Division": "IRL",
        "Sampiyonlar Ligi": "CL", "Avrupa Ligi": "EL", "Konferans Ligi": "ECL",
        "Dunya Kupasi": "WC", "Avrupa Sampiyonasi": "EC",
        "Copa America": "CAM", "Afrika Kupasi": "AFC", "Asya Kupasi": "ASC",
        "FA Cup": "FAC", "EFL Cup": "FLC", "DFB-Pokal": "DFB",
        "Coppa Italia": "CIT", "Coupe de France": "CDF",
        "Copa del Rey": "CDR", "Turkiye Kupasi": "TKC",
    }

    SS_LEAGUES = {
        "Premier League": "premier-league", "La Liga": "la-liga",
        "Bundesliga": "bundesliga", "Serie A": "serie-a",
        "Ligue 1": "ligue-1", "Championship": "championship",
        "La Liga2": "la-liga-2", "Bundesliga 2": "bundesliga-2",
        "Serie B": "serie-b", "Ligue 2": "ligue-2",
        "Eredivisie": "eredivisie", "Primeira Liga": "portugal-primeira-liga",
        "Super Lig": "super-lig", "Belcika Pro League": "belgian-pro-league",
        "Iskocya Premier": "scottish-premiership", "Avusturya Bundesliga": "austrian-bundesliga",
        "Isvicre Super League": "swiss-super-league", "Yunanistan Super League": "greek-super-league",
        "Rusya Premier": "russian-premier-league", "Ukrayna Premier": "ukrainian-premier-league",
        "Danimarka Superliga": "danish-superliga", "Norvec Eliteserien": "norwegian-eliteserien",
        "Isvec Allsvenskan": "swedish-allsvenskan", "Polonya Ekstraklasa": "polish-ekstraklasa",
        "Hirvatistan HNL": "croatian-hnl", "Sirbistan SuperLiga": "serbian-superliga",
        "Cek Cumhuriyeti 1. Liga": "czech-1-liga", "Romanya Liga 1": "romanian-liga-1",
        "Macaristan NB I": "hungarian-nb-i", "Bulgaristan 1. Liga": "bulgarian-1-liga",
        "Slovakya Super Liga": "slovak-super-liga", "Slovenya PrvaLiga": "slovenian-prvaliga",
        "Irlanda Premier Division": "irish-premier-division",
    }

    ALL_LEAGUES = sorted(set(list(LEAGUE_CODES.keys()) + [k for k in SS_LEAGUES.keys() if k not in LEAGUE_CODES]))

    st.title("Eagle Pro - AI Futbol Analiz ve Tahmin")
    st.markdown("### Top 30+ Lig, 2. Ligler, Kupalar, UEFA & FIFA - Veriyle Konusan Analiz")

    if st.button("Ana Sayfaya Don"):
        st.session_state['page'] = 'home'
        st.rerun()

    if default_league in ALL_LEAGUES:
        league_name = st.selectbox("Lig/Turnuva Sec", ALL_LEAGUES, index=ALL_LEAGUES.index(default_league))
    else:
        league_name = st.selectbox("Lig/Turnuva Sec", ALL_LEAGUES)

    if st.button("Puan Durumunu Goster"):
        with st.spinner("Veri cekiliyor..."):
            if league_name in LEAGUE_CODES:
                league_code = LEAGUE_CODES[league_name]
                table = get_league_table(league_code)
                if "error" not in table and "standings" in table:
                    standings = table["standings"]
                    if standings:
                        rows = standings[0].get("table", [])
                        if rows:
                            df = pd.DataFrame([{
                                "Sira": r["position"],
                                "Takim": r["team"]["name"],
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
                            st.warning("Bu lig icin tablo verisi bulunamadi.")
                    else:
                        st.warning("Standings verisi bos.")
                else:
                    st.error("Football-Data.org'dan puan durumu alinamadi. Sports-skills deneniyor...")
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
                                        "Sira": item.get("rank") or item.get("position", ""),
                                        "Takim": item.get("team", {}).get("name", "") if isinstance(item.get("team"), dict) else str(item.get("team", "")),
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
                                    st.warning("Sports-skills'ten tablo verisi alinamadi.")
                            else:
                                st.warning("Sports-skills'ten standings verisi bos.")
                        else:
                            st.error("Her iki kaynaktan da veri alinamadi.")
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
                                    "Sira": item.get("rank") or item.get("position", ""),
                                    "Takim": item.get("team", {}).get("name", "") if isinstance(item.get("team"), dict) else str(item.get("team", "")),
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
                                st.warning("Sports-skills'ten tablo verisi alinamadi.")
                        else:
                            st.warning("Sports-skills'ten standings verisi bos.")
                    else:
                        st.error("Sports-skills'ten veri alinamadi.")
                else:
                    st.error(f"'{league_name}' icin veri kaynagi bulunamadi.")

    if league_name in ["Premier League", "La Liga", "Bundesliga", "Serie A", "Ligue 1"]:
        understat_mapping = {
            "Premier League": "EPL", "La Liga": "La_liga",
            "Bundesliga": "Bundesliga", "Serie A": "Serie_A",
            "Ligue 1": "Ligue_1"
        }
        if st.button("xG/xA Verileri (Understat)"):
            with st.spinner("Understat'ten xG verileri cekiliyor..."):
                xg_df = get_xg_from_understat(understat_mapping[league_name], "2024")
                if not xg_df.empty:
                    st.dataframe(xg_df.head(20))
                else:
                    st.warning("xG verisi alinamadi.")

    if st.button("Takim Istatistikleri (FBref)"):
        with st.spinner("Veri cekiliyor (sports-skills uzerinden)..."):
            for season in ["2024", "2023"]:
                df = get_fbref_team_stats(league_name, season)
                if not df.empty and "Hata" not in df.columns:
                    st.success(f"{season} sezonu verisi basariyla cekildi!")
                    if "team" in df.columns:
                        df["team_name"] = df["team"].apply(
                            lambda x: x.get("name", str(x)) if isinstance(x, dict) else str(x)
                        )
                        cols = ["position", "team_name", "played", "won", "drawn", "lost", 
                                "goals_for", "goals_against", "goal_difference", "points"]
                        df = df[[c for c in cols if c in df.columns]]
                        df.columns = ["Sira", "Takim", "O", "G", "B", "M", "A", "Y", "Avans", "Puan"]
                    else:
                        df.columns = [col.replace("_", " ").title() for col in df.columns]
                    st.dataframe(df, use_container_width=True)
                    break
                else:
                    if not df.empty and "Hata" in df.columns:
                        st.warning(f"{season}: {df['Hata'].iloc[0]}")
                    else:
                        st.warning(f"{season} sezonu icin veri alinamadi.")
            else:
                st.error("Hicbir sezon icin veri alinamadi.")

    st.markdown("---")
    st.subheader("sports-skills Test Alani")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Premier League Puan Durumu (sports-skills)"):
            with st.spinner("sports-skills'ten veri cekiliyor..."):
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
                                        "Sira": item.get("rank") or item.get("position", ""),
                                        "Takim": team_name,
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
                                st.warning("Tablo verisi bulunamadi.")
                                st.json(first)
                        else:
                            st.warning("Standings listesi bos.")
                    else:
                        st.warning("'standings' anahtari bulunamadi.")
                        st.json(data)
                else:
                    st.error("Veri alinamadi.")
    with col2:
        if st.button("Takim Ara (Arsenal)"):
            with st.spinner("Takim profili araniyor..."):
                team = get_ss_team_profile("arsenal")
                if team:
                    st.json(team)
                else:
                    st.error("Takim bulunamadi.")

    st.markdown("---")
    st.subheader("StatsBomb Olay Bazli Veri (Acik Veri)")
    TOURNAMENTS = {
        "FIFA Dunya Kupasi 2022": {"competition_id": 43, "season_id": 106},
        "UEFA Sampiyonlar Ligi 2021-22": {"competition_id": 16, "season_id": 4},
        "UEFA Sampiyonlar Ligi 2022-23": {"competition_id": 16, "season_id": 14},
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
    selected_tournament = st.selectbox("Turnuva Sec", list(TOURNAMENTS.keys()))
    tournament_info = TOURNAMENTS[selected_tournament]
    competition_id = tournament_info["competition_id"]
    season_id = tournament_info["season_id"]

    if st.button("Maclari Listele"):
        with st.spinner("StatsBomb'dan maclar cekiliyor..."):
            matches = get_statsbomb_matches(competition_id, season_id)
            if not matches.empty:
                st.success(f"{len(matches)} mac bulundu!")
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
                        "away": away,
                        "home_id": home_team.get('id') if isinstance(home_team, dict) else None,
                        "away_id": away_team.get('id') if isinstance(away_team, dict) else None
                    })
                st.session_state['match_options'] = match_options
            else:
                st.error("Mac listesi alinamadi.")

    if 'match_options' in st.session_state and st.session_state['match_options']:
        match_options = st.session_state['match_options']
        selected_match_label = st.selectbox(
            "Mac Sec",
            options=[m["display"] for m in match_options],
            key="sb_match_select"
        )
        selected_match = next(m for m in match_options if m["display"] == selected_match_label)

        st.markdown("---")
        st.subheader("Eagle Pro - AI Tahmin Merkezi")

        col1, col2 = st.columns(2)
        with col1:
            predict_1x2 = st.button("1X2 Tahmini", key="predict_1x2")
            predict_ht = st.button("Ilk Yari Tahmini", key="predict_ht")
            predict_btts = st.button("KG Var/Yok Tahmini", key="predict_btts")
        with col2:
            predict_over15 = st.button("Alt/Ust 1.5", key="predict_over15")
            predict_over25 = st.button("Alt/Ust 2.5", key="predict_over25")
            predict_over35 = st.button("Alt/Ust 3.5", key="predict_over35")
            predict_ai = st.button("AI Yorumcu", key="predict_ai")

        if any([predict_1x2, predict_ht, predict_btts, predict_over15, predict_over25, predict_over35, predict_ai]):
            st.info("Su an ornek verilerle tahmin yapilmaktadir. Gercek model entegrasyonu icin veri seti olusturuluyor.")

            st.subheader("Tahmin Sonuclari")

            if predict_1x2:
                st.markdown("#### 1X2 Mac Sonucu")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Ev Kazanir", "%68")
                with col2:
                    st.metric("Beraberlik", "%22")
                with col3:
                    st.metric("Deplasman Kazanir", "%10")

            if predict_ht:
                st.markdown("#### Ilk Yari Sonucu")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Ev Kazanir", "%45")
                with col2:
                    st.metric("Beraberlik", "%40")
                with col3:
                    st.metric("Deplasman Kazanir", "%15")

            if predict_btts:
                st.markdown("#### Karsilikli Gol (BTTS)")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Evet (KG Var)", "%62")
                with col2:
                    st.metric("Hayir (KG Yok)", "%38")

            if predict_over15:
                st.markdown("#### Alt/Ust 1.5")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Ust 1.5", "%78")
                with col2:
                    st.metric("Alt 1.5", "%22")

            if predict_over25:
                st.markdown("#### Alt/Ust 2.5")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Ust 2.5", "%55")
                with col2:
                    st.metric("Alt 2.5", "%45")

            if predict_over35:
                st.markdown("#### Alt/Ust 3.5")
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Ust 3.5", "%30")
                with col2:
                    st.metric("Alt 3.5", "%70")

            if predict_ai:
                st.markdown("#### AI Yorumcu")
                commentary = generate_ai_commentary(
                    selected_match['home'],
                    selected_match['away'],
                    {
                        '1X2': {'tahmin': 'Ev Sahibi Kazanir', 'ev_sahibi_kazanma': 68, 'beraberlik': 22, 'deplasman_kazanma': 10},
                        'HT': {'tahmin': 'Beraberlik', 'ev_sahibi_kazanma': 45, 'beraberlik': 40, 'deplasman_kazanma': 15},
                        'btts': {'tahmin': 'Evet', 'evet': 62, 'hayir': 38},
                        'over_under': {
                            '1.5': {'tahmin': 'Ust', 'over': 78, 'under': 22},
                            '2.5': {'tahmin': 'Ust', 'over': 55, 'under': 45},
                            '3.5': {'tahmin': 'Alt', 'over': 30, 'under': 70}
                        }
                    },
                    {
                        'home_form_5': '4G-1B-0M (13 puan)',
                        'away_form_5': '2G-1B-2M (7 puan)',
                        'home_xg_5': '2.4',
                        'away_xg_5': '1.2'
                    }
                )
                st.markdown(commentary)

        if st.button(f"{selected_match['home']} vs {selected_match['away']} Olaylarini Goster", key="show_events"):
            with st.spinner("Olaylar cekiliyor..."):
                events = get_statsbomb_events(selected_match["match_id"])
                if not events.empty:
                    st.success(f"{len(events)} olay bulundu!")
                    st.session_state['events'] = events
                    st.session_state['selected_match'] = selected_match
                    st.session_state['match_id'] = selected_match["match_id"]
                    event_types = events['type'].unique().tolist()
                    selected_types = st.multiselect(
                        "Olay Turlerini Filtrele",
                        options=event_types,
                        default=event_types[:5] if len(event_types) >= 5 else event_types,
                        key="event_types_filter"
                    )
                    if selected_types:
                        filtered_events = events[events['type'].isin(selected_types)]
                        st.dataframe(filtered_events, use_container_width=True)
                    else:
                        st.dataframe(events, use_container_width=True)
                    st.subheader("Olay Ozeti")
                    summary = events['type'].value_counts().reset_index()
                    summary.columns = ['Olay Turu', 'Sayi']
                    st.dataframe(summary, use_container_width=True)
                else:
                    st.warning("Bu mac icin olay verisi bulunamadi.")
    else:
        if 'match_options' not in st.session_state or not st.session_state['match_options']:
            st.info("Lutfen yukaridan bir turnuva secip 'Maclari Listele' butonuna tiklayin.")

    st.markdown("---")
    st.subheader("Pas Agi Analizi (StatsBomb)")
    if 'selected_match' in st.session_state and st.session_state['selected_match']:
        selected_match = st.session_state['selected_match']
        match_id = st.session_state.get('match_id', None)
        if st.button(f"{selected_match['home']} - {selected_match['away']} Pas Agini Goster", key="show_pass_network"):
            if not match_id:
                st.warning("Once yukaridan bir mac secip 'Olaylari Goster' butonuna tiklayin.")
            else:
                with st.spinner("Pas verileri isleniyor..."):
                    try:
                        events = st.session_state.get('events', None)
                        if events is None or events.empty:
                            events = get_statsbomb_events(match_id)
                        if events.empty:
                            st.warning("Bu mac icin olay verisi bulunamadi.")
                            st.stop()
                        passes = events[events['type'] == 'Pass'].copy()
                        if passes.empty:
                            st.warning("Bu macta pas verisi bulunamadi.")
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
                            st.warning("Pozisyon hesaplanamadi.")
                            st.stop()
                        connections = {}
                        for (p1, p2), count in pass_counts.items():
                            if p1 in positions and p2 in positions and count >= 2:
                                connections[(p1, p2)] = count
                        if not connections:
                            st.warning("Yeterli pas baglantisi yok (en az 2 pas).")
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
                        ax.set_title(f"Pas Agi - {selected_match['home']} vs {selected_match['away']}", color='white', fontsize=14)
                        st.pyplot(fig)
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Toplam Pas", len(passes))
                        with col2:
                            st.metric("Aktif Oyuncu", len(active))
                        with col3:
                            if positions:
                                most = max(positions.items(), key=lambda x: x[1]['total'])
                                st.metric("En Cok Pas", most[0])
                    except Exception as e:
                        st.error(f"Pas agi olusturulurken hata: {str(e)}")
                        with st.expander("Hata Ayiklama: Ham Olay Verisi (Ilk 5)"):
                            if 'events' in st.session_state:
                                st.dataframe(st.session_state['events'].head(5))
    else:
        st.info("Lutfen yukaridan bir turnuva secin, 'Maclari Listele' butonuna tiklayin ve bir mac secin, ardindan 'Olaylari Goster' butonuna tiklayin.")

    st.markdown("---")
    st.subheader("Mac Ozet Raporu (StatsBomb)")
    if 'selected_match' in st.session_state and st.session_state['selected_match']:
        selected_match = st.session_state['selected_match']
        match_id = st.session_state.get('match_id', None)
        if st.button(f"{selected_match['home']} - {selected_match['away']} Mac Ozet Raporu Olustur", key="generate_match_report"):
            if not match_id:
                st.warning("Once yukaridan bir mac secip 'Olaylari Goster' butonuna tiklayin.")
            else:
                with st.spinner("Mac ozet raporu olusturuluyor..."):
                    try:
                        events = st.session_state.get('events', None)
                        if events is None or events.empty:
                            events = get_statsbomb_events(match_id)
                        if events.empty:
                            st.warning("Bu mac icin olay verisi bulunamadi.")
                            st.stop()
                        st.subheader("Mac Bilgileri")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Ev Sahibi", selected_match['home'])
                        with col2:
                            st.metric("Deplasman", selected_match['away'])
                        with col3:
                            match_date = events['event_date'].iloc[0] if 'event_date' in events.columns else 'Tarih yok'
                            st.metric("Tarih", match_date[:10] if len(str(match_date)) > 10 else str(match_date))
                        st.divider()
                        st.subheader("Temel Istatistikler")
                        passes = events[events['type'] == 'Pass'].copy() if 'type' in events.columns else pd.DataFrame()
                        shots = events[events['type'] == 'Shot'].copy() if 'type' in events.columns else pd.DataFrame()
                        carries = events[events['type'] == 'Carry'].copy() if 'type' in events.columns else pd.DataFrame()
                        pressures = events[events['type'] == 'Pressure'].copy() if 'type' in events.columns else pd.DataFrame()
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Toplam Pas", len(passes))
                        with col2:
                            st.metric("Toplam Sut", len(shots))
                        with col3:
                            st.metric("Pres Sayisi", len(pressures))
                        with col4:
                            st.metric("Top Tasima", len(carries))
                        st.divider()
                        st.subheader("xG ve Sut Haritasi")
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
                                    st.metric("Toplam xG", round(total_xg, 2))
                                with col2:
                                    st.metric("Ortalama xG/Sut", round(total_xg / len(shot_xg), 2) if shot_xg else 0)
                            from mplsoccer import Pitch
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
                            ax.set_title(f"Sut Haritasi - {selected_match['home']} vs {selected_match['away']}", color='white', fontsize=14)
                            st.pyplot(fig)
                        else:
                            st.info("Bu macta sut verisi bulunamadi.")
                        st.divider()
                        st.subheader("Pas Agi")
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
                                    ax.set_title(f"Pas Agi - {selected_match['home']} vs {selected_match['away']}", color='white', fontsize=14)
                                    st.pyplot(fig)
                                else:
                                    st.info("Pas baglantilari yeterli degil.")
                            else:
                                st.info("Yeterli pas verisi yok.")
                        else:
                            st.info("Bu macta pas verisi bulunamadi.")
                        st.divider()
                        st.subheader("One Cikan Oyuncular")
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
                                st.write("**En Cok Pas Yapan Oyuncular**")
                                df_passes = pd.DataFrame(top_passers, columns=["Oyuncu", "Pas Sayisi"])
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
                                st.write("**En Cok Sut Ceken Oyuncular**")
                                df_shots = pd.DataFrame(top_shooters, columns=["Oyuncu", "Sut Sayisi"])
                                st.dataframe(df_shots, use_container_width=True, hide_index=True)
                        st.success("Mac ozet raporu basariyla olusturuldu!")
                    except Exception as e:
                        st.error(f"Rapor olusturulurken hata: {str(e)}")
                        with st.expander("Hata Ayiklama: Ham Olay Verisi (Ilk 5)"):
                            if 'events' in st.session_state:
                                st.dataframe(st.session_state['events'].head(5))
    else:
        st.info("Lutfen yukaridan bir turnuva secin, 'Maclari Listele' butonuna tiklayin ve bir mac secin, ardindan 'Olaylari Goster' butonuna tiklayin.")

    st.markdown("---")
    st.subheader("Takim Stili Analizi (StatsBomb)")
    if 'selected_match' in st.session_state and st.session_state['selected_match']:
        selected_match = st.session_state['selected_match']
        match_id = st.session_state.get('match_id', None)
        if st.button(f"{selected_match['home']} - {selected_match['away']} Takim Stili Analizi", key="team_style_analysis"):
            if not match_id:
                st.warning("Once yukaridan bir mac secip 'Olaylari Goster' butonuna tiklayin.")
            else:
                with st.spinner("Takim stili analizi yapiliyor..."):
                    try:
                        events = st.session_state.get('events', None)
                        if events is None or events.empty:
                            events = get_statsbomb_events(match_id)
                        if events.empty:
                            st.warning("Bu mac icin olay verisi bulunamadi.")
                            st.stop()
                        teams = []
                        if 'team' in events.columns:
                            teams = events['team'].unique().tolist()
                        elif 'team_name' in events.columns:
                            teams = events['team_name'].unique().tolist()
                        if len(teams) < 2:
                            st.warning("Takim bilgileri bulunamadi.")
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
                                metrics['Pas Basari Orani'] = round((successful_passes / total_passes) * 100, 1)
                            else:
                                metrics['Pas Basari Orani'] = 0
                            pressures = team_events[team_events['type'] == 'Pressure'].copy() if 'type' in team_events.columns else pd.DataFrame()
                            metrics['Toplam Pres'] = len(pressures)
                            shots = team_events[team_events['type'] == 'Shot'].copy() if 'type' in team_events.columns else pd.DataFrame()
                            metrics['Toplam Sut'] = len(shots)
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
                            metrics['Top Tasima'] = len(carries)
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
                            metrics['Rakip Yari Sahada Pres'] = high_pressures
                            metrics['Rakip Yari Sahada Pres Orani'] = round((high_pressures / metrics['Toplam Pres'] * 100), 1) if metrics['Toplam Pres'] > 0 else 0
                            ball_recoveries = team_events[team_events['type'] == 'Ball Recovery'].copy() if 'type' in team_events.columns else pd.DataFrame()
                            recovery_zones = {'kendi_yari': 0, 'orta_saha': 0, 'rakip_yari': 0}
                            for idx, row in ball_recoveries.iterrows():
                                loc = row.get('location', [])
                                if len(loc) >= 2:
                                    try:
                                        x = float(loc[0])
                                        if x < 40:
                                            recovery_zones['kendi_yari'] += 1
                                        elif x < 80:
                                            recovery_zones['orta_saha'] += 1
                                        else:
                                            recovery_zones['rakip_yari'] += 1
                                    except:
                                        pass
                            metrics['Top Kapma - Kendi Yari'] = recovery_zones['kendi_yari']
                            metrics['Top Kapma - Orta Saha'] = recovery_zones['orta_saha']
                            metrics['Top Kapma - Rakip Yari'] = recovery_zones['rakip_yari']
                            metrics['Aksiyon Hizi (Skor)'] = "Orta"
                            return metrics
                        home_metrics = calculate_style_metrics(home_events, home_team)
                        away_metrics = calculate_style_metrics(away_events, away_team)
                        st.subheader(f"{home_team} vs {away_team} - Stil Karsilastirmasi")
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
                            st.subheader(f"{home_team} - Top Kapma Bolgeleri")
                            recovery_data = {
                                'Bolge': ['Kendi Yari', 'Orta Saha', 'Rakip Yari'],
                                'Sayi': [
                                    home_metrics['Top Kapma - Kendi Yari'],
                                    home_metrics['Top Kapma - Orta Saha'],
                                    home_metrics['Top Kapma - Rakip Yari']
                                ]
                            }
                            if sum(recovery_data['Sayi']) > 0:
                                fig, ax = plt.subplots()
                                ax.pie(recovery_data['Sayi'], labels=recovery_data['Bolge'], autopct='%1.1f%%', 
                                       colors=['#ff6b6b', '#feca57', '#48dbfb'], startangle=90)
                                ax.axis('equal')
                                st.pyplot(fig)
                            else:
                                st.info("Top kapma verisi yok.")
                        with col2:
                            st.subheader(f"{away_team} - Top Kapma Bolgeleri")
                            recovery_data = {
                                'Bolge': ['Kendi Yari', 'Orta Saha', 'Rakip Yari'],
                                'Sayi': [
                                    away_metrics['Top Kapma - Kendi Yari'],
                                    away_metrics['Top Kapma - Orta Saha'],
                                    away_metrics['Top Kapma - Rakip Yari']
                                ]
                            }
                            if sum(recovery_data['Sayi']) > 0:
                                fig, ax = plt.subplots()
                                ax.pie(recovery_data['Sayi'], labels=recovery_data['Bolge'], autopct='%1.1f%%', 
                                       colors=['#ff6b6b', '#feca57', '#48dbfb'], startangle=90)
                                ax.axis('equal')
                                st.pyplot(fig)
                            else:
                                st.info("Top kapma verisi yok.")
                        st.divider()
                        st.subheader("Pres Yuksekligi Karsilastirmasi")
                        pres_data = {
                            'Takim': [home_team, away_team],
                            'Rakip Yari Sahada Pres Orani (%)': [
                                home_metrics['Rakip Yari Sahada Pres Orani'],
                                away_metrics['Rakip Yari Sahada Pres Orani']
                            ]
                        }
                        df_pres = pd.DataFrame(pres_data)
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.bar(df_pres['Takim'], df_pres['Rakip Yari Sahada Pres Orani (%)'], color=['#00ffcc', '#ff6b6b'])
                        ax.set_ylabel('Rakip Yari Sahada Pres Orani (%)')
                        ax.set_title('Pres Yuksekligi Karsilastirmasi')
                        ax.set_ylim(0, 100)
                        for i, v in enumerate(df_pres['Rakip Yari Sahada Pres Orani (%)']):
                            ax.text(i, v + 2, f"{v}%", ha='center', color='white')
                        st.pyplot(fig)
                        st.subheader("Pas Basari Orani Karsilastirmasi")
                        pass_data = {
                            'Takim': [home_team, away_team],
                            'Pas Basari Orani (%)': [
                                home_metrics['Pas Basari Orani'],
                                away_metrics['Pas Basari Orani']
                            ]
                        }
                        df_pass = pd.DataFrame(pass_data)
                        fig, ax = plt.subplots(figsize=(8, 5))
                        ax.bar(df_pass['Takim'], df_pass['Pas Basari Orani (%)'], color=['#00ffcc', '#ff6b6b'])
                        ax.set_ylabel('Pas Basari Orani (%)')
                        ax.set_title('Pas Basari Orani Karsilastirmasi')
                        ax.set_ylim(0, 100)
                        for i, v in enumerate(df_pass['Pas Basari Orani (%)']):
                            ax.text(i, v + 2, f"{v}%", ha='center', color='white')
                        st.pyplot(fig)
                        st.success("Takim stili analizi basariyla tamamlandi!")
                    except Exception as e:
                        st.error(f"Takim stili analizi sirasinda hata: {str(e)}")
                        with st.expander("Hata Ayiklama: Ham Olay Verisi (Ilk 5)"):
                            if 'events' in st.session_state:
                                st.dataframe(st.session_state['events'].head(5))
    else:
        st.info("Lutfen yukaridan bir turnuva secin, 'Maclari Listele' butonuna tiklayin ve bir mac secin, ardindan 'Olaylari Goster' butonuna tiklayin.")            
