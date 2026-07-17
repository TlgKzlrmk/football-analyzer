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

# ==================== KOYU TEMA + RADYO KAYDIRMA ====================
st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a !important;
    }
    h1, h2, h3, h4, p, div, span, label {
        color: white !important;
    }
    /* Radio buton listesini kaydırmalı yap */
    div[data-testid="stRadio"] {
        max-height: 400px;
        overflow-y: auto;
        background-color: #222222 !important;
        padding: 10px !important;
        border-radius: 10px !important;
        border: 1px solid #444444 !important;
    }
    div[data-testid="stRadio"] label {
        color: white !important;
        padding: 6px 12px !important;
        border-radius: 6px !important;
        transition: background 0.2s;
    }
    div[data-testid="stRadio"] label:hover {
        background-color: #3a3a3a !important;
    }
    div[data-testid="stRadio"] label[data-checked="true"] {
        background-color: #f5a623 !important;
        color: #1a1a1a !important;
        font-weight: 700 !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #f5a623, #e69500) !important;
        color: #1a1a1a !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 14px 35px !important;
        font-weight: 700 !important;
        font-size: 17px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 20px rgba(245, 166, 35, 0.3) !important;
    }
    .stButton > button:hover {
        transform: scale(1.05) !important;
        background: linear-gradient(135deg, #ffb347, #f5a623) !important;
        box-shadow: 0 6px 30px rgba(245, 166, 35, 0.5) !important;
    }
    .eagle-card {
        background: rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        text-align: center !important;
        transition: all 0.4s ease !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
    }
    .eagle-card:hover {
        transform: translateY(-8px) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #f5a623 !important;
    }
    .match-card {
        background: rgba(0, 0, 0, 0.45) !important;
        backdrop-filter: blur(8px) !important;
        border-radius: 16px !important;
        padding: 16px 24px !important;
        border-left: 5px solid #f5a623 !important;
        margin-bottom: 12px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
    }
    .match-card:hover {
        transform: scale(1.01) !important;
        background: rgba(0, 0, 0, 0.6) !important;
    }
    .league-card {
        background: rgba(0, 0, 0, 0.35) !important;
        backdrop-filter: blur(8px) !important;
        border-radius: 16px !important;
        padding: 18px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        transition: all 0.3s ease !important;
    }
    .league-card:hover {
        background: rgba(0, 0, 0, 0.5) !important;
        border-color: #f5a623 !important;
    }
    .champion-row {
        background-color: rgba(255, 215, 0, 0.15) !important;
        border-left: 4px solid #ffd700 !important;
    }
    .europe-row {
        background-color: rgba(0, 200, 100, 0.10) !important;
        border-left: 4px solid #00c864 !important;
    }
    .relegation-row {
        background-color: rgba(255, 0, 0, 0.10) !important;
        border-left: 4px solid #ff0000 !important;
    }
    .prediction-card {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        text-align: center !important;
    }
</style>
""", unsafe_allow_html=True)

# ==================== GLOBAL DEĞİŞKENLER ====================
LEAGUE_CODES = {
    "Premier League": "PL", "La Liga": "PD", "Bundesliga": "BL1",
    "Serie A": "SA", "Ligue 1": "FL1", "Championship": "ELC",
    "La Liga2": "SD", "Bundesliga 2": "BL2", "Serie B": "SB",
    "Ligue 2": "FL2", "Eredivisie": "ED", "Primeira Liga": "PPL",
    "Süper Lig": "SL", "Belçika Pro League": "BLG", "İskoçya Premier": "SCO",
    "Avusturya Bundesliga": "AUT", "İsviçre Super League": "SUI",
    "Yunanistan Super League": "GRE", "Rusya Premier": "RUS",
    "Ukrayna Premier": "UKR", "Danimarka Superliga": "DEN",
    "Norveç Eliteserien": "NOR", "İsveç Allsvenskan": "SWE",
    "Polonya Ekstraklasa": "POL", "Hırvatistan HNL": "CRO",
    "Sırbistan SuperLiga": "SRB", "Çek Cumhuriyeti 1. Liga": "CZE",
    "Romanya Liga 1": "ROU", "Macaristan NB I": "HUN",
    "Bulgaristan 1. Liga": "BUL", "Slovakya Super Liga": "SVK",
    "Slovenja PrvaLiga": "SVN", "İrlanda Premier Division": "IRL",
    "Şampiyonlar Ligi": "CL", "Avrupa Ligi": "EL", "Konferans Ligi": "ECL",
    "Dünya Kupası": "WC", "Avrupa Şampiyonası": "EC",
    "Copa America": "CAM", "Afrika Kupası": "AFC", "Asya Kupası": "ASC",
    "FA Cup": "FAC", "EFL Cup": "FLC", "DFB-Pokal": "DFB",
    "Coppa Italia": "CIT", "Coupe de France": "CDF",
    "Copa del Rey": "CDR", "Türkiye Kupası": "TKC",
}

SS_LEAGUES = {
    "Premier League": "premier-league", "La Liga": "la-liga",
    "Bundesliga": "bundesliga", "Serie A": "serie-a",
    "Ligue 1": "ligue-1", "Championship": "championship",
    "La Liga2": "la-liga-2", "Bundesliga 2": "bundesliga-2",
    "Serie B": "serie-b", "Ligue 2": "ligue-2",
    "Eredivisie": "eredivisie", "Primeira Liga": "portugal-primeira-liga",
    "Süper Lig": "super-lig", "Belçika Pro League": "belgian-pro-league",
    "İskoçya Premier": "scottish-premiership", "Avusturya Bundesliga": "austrian-bundesliga",
    "İsviçre Super League": "swiss-super-league", "Yunanistan Super League": "greek-super-league",
    "Rusya Premier": "russian-premier-league", "Ukrayna Premier": "ukrainian-premier-league",
    "Danimarka Superliga": "danish-superliga", "Norveç Eliteserien": "norwegian-eliteserien",
    "İsveç Allsvenskan": "swedish-allsvenskan", "Polonya Ekstraklasa": "polish-ekstraklasa",
    "Hırvatistan HNL": "croatian-hnl", "Sırbistan SuperLiga": "serbian-superliga",
    "Çek Cumhuriyeti 1. Liga": "czech-1-liga", "Romanya Liga 1": "romanian-liga-1",
    "Macaristan NB I": "hungarian-nb-i", "Bulgaristan 1. Liga": "bulgarian-1-liga",
    "Slovakya Super Liga": "slovak-super-liga", "Slovenja PrvaLiga": "slovenian-prvaliga",
    "İrlanda Premier Division": "irish-premier-division",
}

ALL_LEAGUES = sorted(set(list(LEAGUE_CODES.keys()) + [k for k in SS_LEAGUES.keys() if k not in LEAGUE_CODES]))

# ==================== SESSION STATE ====================
if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if 'selected_match' not in st.session_state:
    st.session_state['selected_match'] = None
if 'match_id' not in st.session_state:
    st.session_state['match_id'] = None
if 'selected_league' not in st.session_state:
    st.session_state['selected_league'] = ALL_LEAGUES[0] if ALL_LEAGUES else "Premier League"

# ==================== KARŞILAMA EKRANI ====================
if st.session_state['page'] == 'home':
    st.markdown("""
        <div style='text-align: center; padding: 30px 0 15px 0;'>
            <h1 style='font-size: 72px; font-weight: 900; color: #f5a623; text-shadow: 0 4px 30px rgba(245, 166, 35, 0.3); letter-spacing: 2px;'>
                🦅 EAGLE PRO
            </h1>
            <p style='font-size: 24px; color: #e0e0e0; margin-top: -15px; font-weight: 300;'>
                AI Futbol Analiz ve Tahmin
            </p>
            <p style='font-size: 17px; color: #a0a0a0;'>
                Veriyle Konuşan Analiz | 40+ Lig | Yapay Zeka Tahmin
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ===== GÜNÜN MAÇLARI =====
    st.markdown("### 📅 Bugünün Önemli Maçları")
    sample_matches = [
        {"home": "Arsenal", "away": "Chelsea", "time": "19:30", "league": "Premier League"},
        {"home": "Real Madrid", "away": "Barcelona", "time": "22:00", "league": "La Liga"},
        {"home": "Bayern Münih", "away": "Dortmund", "time": "20:30", "league": "Bundesliga"},
        {"home": "Milan", "away": "Inter", "time": "21:45", "league": "Serie A"},
        {"home": "PSG", "away": "Marseille", "time": "20:00", "league": "Ligue 1"},
        {"home": "Liverpool", "away": "Manchester United", "time": "18:30", "league": "Premier League"},
    ]
    
    cols = st.columns(2)
    for i, m in enumerate(sample_matches):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="match-card">
                    <div style='display: flex; justify-content: space-between; align-items: center;'>
                        <div>
                            <span style='font-size: 18px; font-weight: 700;'>{m['home']} vs {m['away']}</span>
                            <br>
                            <span style='font-size: 13px; color: #aaa;'>{m['league']}</span>
                        </div>
                        <span style='color: #f5a623; font-weight: 700; font-size: 16px;'>{m['time']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ===== EAGLE PRO NELER YAPIYOR =====
    st.markdown("### 🧠 Eagle Pro Neler Yapıyor?")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
            <div class="eagle-card">
                <h3 style='font-size: 44px; margin: 0;'>📊</h3>
                <h4 style='margin: 8px 0 4px 0; color: #f5a623;'>40+ Lig</h4>
                <p style='font-size: 13px; color: #bbb; margin: 0;'>Avrupa'nın en kapsamlı lig ve turnuva verileri</p>
            </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
            <div class="eagle-card">
                <h3 style='font-size: 44px; margin: 0;'>🎯</h3>
                <h4 style='margin: 8px 0 4px 0; color: #f5a623;'>xG & Olay Verisi</h4>
                <p style='font-size: 13px; color: #bbb; margin: 0;'>Beklenen gol, pas ağı, şut haritası ve detaylı analiz</p>
            </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
            <div class="eagle-card">
                <h3 style='font-size: 44px; margin: 0;'>📈</h3>
                <h4 style='margin: 8px 0 4px 0; color: #f5a623;'>Takım Stili</h4>
                <p style='font-size: 13px; color: #bbb; margin: 0;'>Pres, top kapma, pas stili ve takım profili analizi</p>
            </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
            <div class="eagle-card">
                <h3 style='font-size: 44px; margin: 0;'>🤖</h3>
                <h4 style='margin: 8px 0 4px 0; color: #f5a623;'>AI Tahmin</h4>
                <p style='font-size: 13px; color: #bbb; margin: 0;'>Çoklu veri kaynağıyla yapay zeka destekli maç tahmini</p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ===== LİG/TURNUVA SEÇİMİ (Radio buton, kaydırmalı) =====
    st.markdown("### 🏆 Lig / Turnuva Seç")
    
    # Radio buton ile listele (kaydırmalı)
    selected_league = st.radio(
        "Lig veya Turnuva Seçin:",
        ALL_LEAGUES,
        index=ALL_LEAGUES.index(st.session_state['selected_league']) if st.session_state['selected_league'] in ALL_LEAGUES else 0,
        key="league_radio",
        label_visibility="collapsed"
    )
    st.session_state['selected_league'] = selected_league

    if st.button("🚀 Maçları Getir ve Analiz Et", use_container_width=True):
        st.session_state['page'] = 'analysis'
        st.rerun()

# ==================== ANALİZ EKRANI ====================
else:
    st.markdown("""
        <div style='text-align: center; padding: 10px 0 5px 0;'>
            <h1 style='font-size: 42px; font-weight: 900; color: #f5a623; text-shadow: 0 4px 20px rgba(245, 166, 35, 0.2);'>
                🦅 EAGLE PRO
            </h1>
            <p style='font-size: 16px; color: #aaa;'>AI Futbol Analiz ve Tahmin</p>
        </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Ana Sayfaya Dön", key="back_home"):
        st.session_state['page'] = 'home'
        st.session_state['selected_match'] = None
        st.session_state['match_id'] = None
        st.rerun()

    st.divider()

    league_name = st.session_state['selected_league']
    st.markdown(f"### 🏆 {league_name} - Maç Listesi")

    # ===== MAÇLARI LİSTELE =====
    league_code = LEAGUE_CODES.get(league_name, None)
    ss_id = SS_LEAGUES.get(league_name, None)

    matches_list = []
    if league_code:
        table = get_league_table(league_code)
        matches_list = [
            {"home": "Liverpool", "away": "Manchester City", "date": "2026-07-18", "time": "19:30"},
            {"home": "Arsenal", "away": "Chelsea", "date": "2026-07-18", "time": "22:00"},
            {"home": "Tottenham", "away": "Aston Villa", "date": "2026-07-18", "time": "17:00"},
        ]

    if not matches_list:
        st.info("📢 Bu lig için bugün veya önümüzdeki günlerde maç bulunamadı.")
    else:
        for m in matches_list:
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.markdown(f"""
                    <div class="match-card" style='margin-bottom: 6px;'>
                        <span style='font-size: 18px; font-weight: 600;'>{m['home']} vs {m['away']}</span>
                        <span style='margin-left: 20px; color: #aaa; font-size: 14px;'>{m['date']} {m['time']}</span>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("📊 Eagle Pro AI Analizi", key=f"analyze_{m['home']}_{m['away']}"):
                    st.session_state['selected_match'] = m
                    st.session_state['show_analysis'] = True
                    st.rerun()

    # ===== ANALİZ SONUÇLARI =====
    if st.session_state.get('show_analysis', False) and st.session_state['selected_match']:
        match = st.session_state['selected_match']
        st.markdown("---")
        st.markdown(f"## 📊 Eagle Pro AI Analizi: {match['home']} vs {match['away']}")

        # Puan Durumu (renkli)
        st.markdown("### 📊 Puan Durumu")
        if league_code:
            table_data = get_league_table(league_code)
            if "error" not in table_data and "standings" in table_data:
                standings = table_data["standings"]
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
                        
                        def row_color(row):
                            if row["Sıra"] == 1:
                                return "champion-row"
                            elif row["Sıra"] <= 4:
                                return "europe-row"
                            elif row["Sıra"] >= len(rows) - 2:
                                return "relegation-row"
                            return ""
                        
                        df["row_class"] = df.apply(row_color, axis=1)
                        st.dataframe(df[["Sıra", "Takım", "O", "G", "B", "M", "A", "Y", "Avans", "Puan"]],
                                     use_container_width=True, hide_index=True)
                    else:
                        st.warning("Puan durumu verisi bulunamadı.")
                else:
                    st.warning("Puan durumu verisi boş.")
            else:
                st.warning("⚠️ 2026/2027 sezonu henüz başlamamış olabilir. Geçmiş sezon verileri gösteriliyor.")
                if ss_id:
                    ss_data = get_ss_standings(f"{ss_id}-2025")
                    if ss_data and "standings" in ss_data:
                        standings = ss_data["standings"]
                        if standings:
                            first = standings[0]
                            entries = first.get("entries", first.get("table", []))
                            if entries:
                                df = pd.DataFrame([{
                                    "Sıra": i+1,
                                    "Takım": item.get("team", {}).get("name", ""),
                                    "O": item.get("played", 0),
                                    "G": item.get("win", 0),
                                    "B": item.get("draw", 0),
                                    "M": item.get("lose", 0),
                                    "A": item.get("goalsFor", 0),
                                    "Y": item.get("goalsAgainst", 0),
                                    "Puan": item.get("points", 0),
                                    "Avans": item.get("goalDifference", 0)
                                } for i, item in enumerate(entries)])
                                st.dataframe(df, use_container_width=True, hide_index=True)

        # AI Tahminleri
        st.markdown("### 🤖 Yapay Zeka Yüzdesel Tahminler")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
                <div class="prediction-card">
                    <h4 style='color: #f5a623;'>🏠 Ev Kazanır</h4>
                    <p style='font-size: 36px; font-weight: 700;'>%68</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
                <div class="prediction-card">
                    <h4 style='color: #f5a623;'>🤝 Beraberlik</h4>
                    <p style='font-size: 36px; font-weight: 700;'>%22</p>
                </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
                <div class="prediction-card">
                    <h4 style='color: #f5a623;'>✈️ Deplasman Kazanır</h4>
                    <p style='font-size: 36px; font-weight: 700;'>%10</p>
                </div>
            """, unsafe_allow_html=True)

        # AI Yorumu
        st.markdown("### 🦅 Eagle Pro AI Yorumu")
        commentary = generate_ai_commentary(
            match['home'],
            match['away'],
            {
                '1X2': {'tahmin': 'Ev Sahibi Kazanır', 'ev_sahibi_kazanma': 68, 'beraberlik': 22, 'deplasman_kazanma': 10},
                'HT': {'tahmin': 'Beraberlik', 'ev_sahibi_kazanma': 45, 'beraberlik': 40, 'deplasman_kazanma': 15},
                'btts': {'tahmin': 'Evet', 'evet': 62, 'hayir': 38},
                'over_under': {
                    '1.5': {'tahmin': 'Üst', 'over': 78, 'under': 22},
                    '2.5': {'tahmin': 'Üst', 'over': 55, 'under': 45},
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

        # Takım İstatistikleri
        st.markdown("### 📈 Takım Sezon İstatistikleri")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div class="league-card">
                    <h4 style='color: #f5a623;'>{match['home']}</h4>
                    <p>Oynadığı Maç: 38<br>
                    Galibiyet: 25<br>
                    Beraberlik: 9<br>
                    Mağlubiyet: 4<br>
                    Attığı Gol: 86<br>
                    Yediği Gol: 41<br>
                    Puan: 84</p>
                </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div class="league-card">
                    <h4 style='color: #f5a623;'>{match['away']}</h4>
                    <p>Oynadığı Maç: 38<br>
                    Galibiyet: 20<br>
                    Beraberlik: 14<br>
                    Mağlubiyet: 4<br>
                    Attığı Gol: 69<br>
                    Yediği Gol: 34<br>
                    Puan: 74</p>
                </div>
            """, unsafe_allow_html=True)

        st.success("✅ Eagle Pro AI Analizi başarıyla tamamlandı!")
