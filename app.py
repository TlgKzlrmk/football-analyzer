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
                st.warning("xG verisi alınamadı.")

# FBref Takım İstatistikleri (sports-skills ile)
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

# ==================== StatsBomb OLAY BAZLI VERİ ====================
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

# ==================== PAS AĞI GÖRSELLEŞTİRME (SAĞLAM VERSİYON) ====================
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
                    else:
                        # Hata ayıklama: sütunları göster
                        with st.expander("🔍 Sütunlar (Hata Ayıklama)"):
                            st.write(events.columns.tolist())
                        
                        # Pas olaylarını filtrele
                        if 'type' in events.columns:
                            passes = events[events['type'] == 'Pass'].copy()
                        else:
                            st.warning("'type' sütunu bulunamadı.")
                            passes = pd.DataFrame()
                        
                        if passes.empty:
                            st.warning("Bu maçta pas verisi bulunamadı.")
                        else:
                            import numpy as np
                            from mplsoccer import Pitch
                            
                            player_positions = {}
                            pass_counts = {}
                            
                            for idx, row in passes.iterrows():
                                # Oyuncu adını bul
                                player = None
                                if 'player' in row and isinstance(row['player'], dict):
                                    player = row['player'].get('name', None)
                                elif 'player_name' in row:
                                    player = row['player_name']
                                elif 'player' in row and isinstance(row['player'], str):
                                    player = row['player']
                                elif 'player_id' in row:
                                    player = f"P{row['player_id']}"
                                
                                if not player:
                                    continue
                                
                                # Konum bilgisi (float'a çevir)
                                if 'location' in row:
                                    loc = row['location']
                                    if isinstance(loc, list) and len(loc) >= 2:
                                        try:
                                            x = float(loc[0])
                                            y = float(loc[1])
                                        except (ValueError, TypeError):
                                            continue
                                    else:
                                        continue
                                else:
                                    continue
                                
                                if x is None or y is None:
                                    continue
                                
                                # Oyuncu pozisyonlarını güncelle
                                if player not in player_positions:
                                    player_positions[player] = {'x': [], 'y': [], 'total': 0}
                                player_positions[player]['x'].append(x)
                                player_positions[player]['y'].append(y)
                                player_positions[player]['total'] += 1
                                
                                # Pas alıcısını bul
                                recipient = None
                                if 'pass' in row and isinstance(row['pass'], dict):
                                    pdata = row['pass']
                                    if 'recipient' in pdata and isinstance(pdata['recipient'], dict):
                                        recipient = pdata['recipient'].get('name', None)
                                    elif 'recipient_name' in pdata:
                                        recipient = pdata['recipient_name']
                                    elif 'recipient' in pdata and isinstance(pdata['recipient'], str):
                                        recipient = pdata['recipient']
                                elif 'pass_recipient' in row:
                                    recipient = row['pass_recipient']
                                elif 'recipient' in row:
                                    recipient = row['recipient']
                                
                                if recipient and recipient != player:
                                    key = tuple(sorted([player, recipient]))
                                    if key not in pass_counts:
                                        pass_counts[key] = 0
                                    pass_counts[key] += 1
                            
                            # En az 3 pas yapan oyuncuları al
                            active = [p for p, data in player_positions.items() if data['total'] >= 3]
                            if len(active) < 2:
                                st.warning(f"Yeterli pas verisi yok (en az 3 pas yapan {len(active)} oyuncu bulundu, 2 gerekli).")
                            else:
                                # Pozisyon ortalamalarını hesapla
                                positions = {}
                                for p in active:
                                    data = player_positions[p]
                                    positions[p] = {
                                        'x': np.mean(data['x']),
                                        'y': np.mean(data['y']),
                                        'total': data['total']
                                    }
                                
                                # En az 2 pas olan bağlantıları al
                                connections = {k: v for k, v in pass_counts.items() 
                                               if k[0] in active and k[1] in active and v >= 2}
                                
                                if not connections:
                                    st.warning("Yeterli pas bağlantısı yok (en az 2 pas olan bağlantı bulunamadı).")
                                    # Hata ayıklama: ilk 10 pası göster
                                    with st.expander("🔍 Ham Pas Verisi (İlk 10)"):
                                        show_cols = [c for c in ['player', 'location', 'pass'] if c in passes.columns]
                                        if show_cols:
                                            st.dataframe(passes[show_cols].head(10))
                                        else:
                                            st.dataframe(passes.head(10))
                                else:
                                    try:
                                        # Pas ağını çiz
                                        pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
                                        fig, ax = pitch.draw(figsize=(12, 8))
                                        
                                        # Oyuncuları yerleştir (tüm değerler float olmalı)
                                        for player, pos in positions.items():
                                            x = float(pos['x'])
                                            y = float(pos['y'])
                                            size = 150 + (pos['total'] * 3)
                                            ax.scatter(x, y, s=size, color='#00ffcc', edgecolors='white', zorder=5, alpha=0.8)
                                            ax.text(x, y-3, player, color='white', ha='center', fontsize=8, fontweight='bold')
                                        
                                        # Bağlantıları çiz
                                        for (p1, p2), count in connections.items():
                                            if p1 in positions and p2 in positions:
                                                x1 = float(positions[p1]['x'])
                                                y1 = float(positions[p1]['y'])
                                                x2 = float(positions[p2]['x'])
                                                y2 = float(positions[p2]['y'])
                                                
                                                linewidth = 1 + (count / 3)
                                                alpha = min(0.8, 0.2 + (count / 10))
                                                ax.plot([x1, x2], [y1, y2], 
                                                       color='cyan', linewidth=linewidth, alpha=alpha, zorder=2)
                                        
                                        ax.set_title(f"Pas Ağı - {selected_match['home']} vs {selected_match['away']}", 
                                                    color='white', fontsize=14)
                                        
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
                                        st.error(f"Pas ağı çizilirken hata: {str(e)}")
                                        # Hata detayı için positions ve connections değerlerini göster
                                        with st.expander("🔍 Hata Detayı (positions & connections)"):
                                            st.write("positions:", {k: v for k, v in positions.items()})
                                            st.write("connections:", connections)
                                    
                except Exception as e:
                    st.error(f"Pas ağı oluşturulurken hata: {str(e)}")
                    # Hata durumunda ham veriyi göster
                    with st.expander("🔍 Hata Ayıklama: Ham Olay Verisi (İlk 5)"):
                        if 'events' in st.session_state:
                            st.dataframe(st.session_state['events'].head(5))
else:
    st.info("Lütfen yukarıdan bir turnuva seçin, 'Maçları Listele' butonuna tıklayın ve bir maç seçin, ardından 'Olayları Göster' butonuna tıklayın.")
