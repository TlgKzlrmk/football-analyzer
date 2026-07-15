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
        for season in ["2024", "2023"]:
            df = get_fbref_team_stats(league_name, season)
            if not df.empty and "Hata" not in df.columns:
                st.success(f"{season} sezonu verisi başarıyla çekildi!")
                
                # team sütununu düzelt (iç içe JSON'dan takım adını çıkar)
                if "team" in df.columns:
                    # team sütunundaki dict'ten 'name' alanını çıkar
                    df["team_name"] = df["team"].apply(
                        lambda x: x.get("name", str(x)) if isinstance(x, dict) else str(x)
                    )
                    # sütun sıralamasını düzenle
                    cols = ["position", "team_name", "played", "won", "drawn", "lost", 
                            "goals_for", "goals_against", "goal_difference", "points"]
                    df = df[[c for c in cols if c in df.columns]]
                    df.columns = ["Sıra", "Takım", "O", "G", "B", "M", "A", "Y", "Avans", "Puan"]
                else:
                    # team yoksa sadece sütun isimlerini Türkçeleştir
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

# StatsBomb turnuva listesi (GÜNCELLENMİŞ ID'LER)
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
            
            # Maç listesini oluştur (DOĞRU ANAHTARLARLA)
            match_options = []
            for idx, row in matches.iterrows():
                # home_team ve away_team sütunları sözlük olabilir
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
            
            if match_options:
                selected_match_label = st.selectbox(
                    "📅 Maç Seç",
                    options=[m["display"] for m in match_options]
                )
                selected_match = next(m for m in match_options if m["display"] == selected_match_label)
                match_id = selected_match["match_id"]
                
                if st.button(f"🚀 {selected_match['home']} vs {selected_match['away']} Olaylarını Göster"):
                    with st.spinner("Olaylar çekiliyor..."):
                        events = get_statsbomb_events(match_id)
                        if not events.empty:
                            st.success(f"{len(events)} olay bulundu!")
                            
                            # Olay türleri
                            event_types = events['type'].unique().tolist()
                            selected_types = st.multiselect(
                                "🔍 Olay Türlerini Filtrele",
                                options=event_types,
                                default=event_types[:5] if len(event_types) >= 5 else event_types
                            )
                            
                            if selected_types:
                                filtered_events = events[events['type'].isin(selected_types)]
                                st.dataframe(filtered_events, use_container_width=True)
                            else:
                                st.dataframe(events, use_container_width=True)
                            
                            # Özet
                            st.subheader("📊 Olay Özeti")
                            summary = events['type'].value_counts().reset_index()
                            summary.columns = ['Olay Türü', 'Sayı']
                            st.dataframe(summary, use_container_width=True)
                        else:
                            st.warning("Bu maç için olay verisi bulunamadı.")
            else:
                st.warning("Hiç maç bulunamadı. Farklı bir turnuva deneyin.")
        else:
            st.error("Maç listesi alınamadı. Turnuva ID'lerini veya internet bağlantınızı kontrol edin.")

# ==================== PAS AĞI GÖRSELLEŞTİRME ====================
st.markdown("---")
st.subheader("🔗 Pas Ağı Analizi (StatsBomb)")

if 'selected_match' in locals() and selected_match:
    if st.button(f"📊 {selected_match['home']} - {selected_match['away']} Pas Ağını Göster"):
        with st.spinner("Pas verileri işleniyor..."):
            try:
                # Maç olaylarını çek
                events = get_statsbomb_events(match_id)
                if events.empty:
                    st.warning("Bu maç için olay verisi bulunamadı.")
                else:
                    # Pas olaylarını filtrele
                    passes = events[events['type'] == 'Pass'].copy()
                    if passes.empty:
                        st.warning("Bu maçta pas verisi bulunamadı.")
                    else:
                        # Oyuncu pozisyonlarını hesapla (orta nokta)
                        import numpy as np
                        from mplsoccer import Pitch
                        
                        # Oyuncu bazında pas sayıları ve ortalama pozisyonlar
                        player_positions = {}
                        player_passes = {}
                        
                        for idx, row in passes.iterrows():
                            # Pası atan oyuncu
                            player = row.get('player', {}).get('name', 'Bilinmeyen')
                            if not player:
                                continue
                            
                            # Başlangıç koordinatları
                            start_x = row.get('location', [None, None])[0]
                            start_y = row.get('location', [None, None])[1]
                            
                            if start_x is None or start_y is None:
                                continue
                            
                            # Oyuncu pozisyonlarını güncelle
                            if player not in player_positions:
                                player_positions[player] = {'x': [], 'y': [], 'total_passes': 0}
                            player_positions[player]['x'].append(start_x)
                            player_positions[player]['y'].append(start_y)
                            player_positions[player]['total_passes'] += 1
                            
                            # Pas bağlantılarını kaydet (hedef oyuncu)
                            recipient = row.get('pass', {}).get('recipient', {}).get('name', None)
                            if recipient:
                                key = tuple(sorted([player, recipient]))
                                if key not in player_passes:
                                    player_passes[key] = 0
                                player_passes[key] += 1
                        
                        # En az 3 pas yapan oyuncuları filtrele
                        active_players = [p for p, data in player_positions.items() 
                                         if data['total_passes'] >= 3]
                        
                        if len(active_players) < 2:
                            st.warning("Yeterli pas verisi yok (en az 3 pas yapan oyuncu gerekli).")
                        else:
                            # Oyuncu pozisyonlarını hesapla (ortalama)
                            positions = {}
                            for player in active_players:
                                data = player_positions[player]
                                positions[player] = {
                                    'x': np.mean(data['x']),
                                    'y': np.mean(data['y']),
                                    'total_passes': data['total_passes']
                                }
                            
                            # Pas bağlantılarını filtrele (en az 2 pas)
                            pass_connections = {k: v for k, v in player_passes.items() 
                                                if k[0] in active_players and k[1] in active_players and v >= 2}
                            
                            if not pass_connections:
                                st.warning("Yeterli pas bağlantısı yok.")
                            else:
                                # Saha çiz
                                pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
                                fig, ax = pitch.draw(figsize=(12, 8))
                                
                                # Oyuncuları yerleştir
                                for player, pos in positions.items():
                                    x = pos['x'] / 1.0  # StatsBomb koordinatları 0-120, 0-80 arası
                                    y = pos['y'] / 1.0
                                    
                                    # Pas sayısına göre boyut
                                    size = 150 + (pos['total_passes'] * 5)
                                    ax.scatter(x, y, s=size, color='#00ffcc', edgecolors='white', zorder=5, alpha=0.8)
                                    ax.text(x, y-3, player, color='white', ha='center', fontsize=8, fontweight='bold')
                                
                                # Pas bağlantılarını çiz
                                for (p1, p2), count in pass_connections.items():
                                    if p1 in positions and p2 in positions:
                                        x1 = positions[p1]['x']
                                        y1 = positions[p1]['y']
                                        x2 = positions[p2]['x']
                                        y2 = positions[p2]['y']
                                        
                                        # Pas sayısına göre kalınlık ve renk
                                        linewidth = 1 + (count / 5)
                                        alpha = min(0.8, 0.3 + (count / 20))
                                        ax.plot([x1, x2], [y1, y2], 
                                               color='cyan', linewidth=linewidth, alpha=alpha, zorder=2)
                                
                                ax.set_title(f"Pas Ağı - {selected_match['home']} vs {selected_match['away']}", 
                                            color='white', fontsize=14)
                                
                                # İstatistik özeti
                                st.pyplot(fig)
                                
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Toplam Pas", len(passes))
                                with col2:
                                    st.metric("Aktif Oyuncu", len(active_players))
                                with col3:
                                    st.metric("En Çok Pas", 
                                             max(positions.items(), key=lambda x: x[1]['total_passes'])[0] if positions else "-")
                            
            except Exception as e:
                st.error(f"Pas ağı oluşturulurken hata: {str(e)}")
else:
    st.info("Önce yukarıdan bir maç seçip 'Olayları Göster' butonuna tıklayın, ardından burada pas ağını görebilirsiniz.")
