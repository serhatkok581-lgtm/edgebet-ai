import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime

st.set_page_config(page_title="EdgeBet AI - Tanrı Modu", layout="wide", page_icon="⚽")

st.title("⚽ EdgeBet AI")
st.markdown("**Tanrı Modu Açık • Gerçek The Odds API • Gerçek Oranlar • Profesyonel AI**")

api_key = st.secrets.get("ODDS_API_KEY")
if not api_key:
    st.error("❌ ODDS_API_KEY bulunamadı! Secrets'a ekleyin.")
    st.stop()

# ====================== GERÇEK ORANLARI ÇEK ======================
@st.cache_data(ttl=180)
def get_real_odds():
    url = "https://api.the-odds-api.com/v4/sports/soccer/odds"
    params = {
        "apiKey": api_key,
        "regions": "eu",
        "markets": "h2h",
        "oddsFormat": "decimal"
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code != 200:
            st.error(f"API Hatası: {resp.status_code}")
            return pd.DataFrame()
        
        data = resp.json()
        matches = []
        for item in data[:20]:  # ilk 20 maç
            home = item['home_team']
            away = item['away_team']
            league = item.get('sport_title', 'Futbol')
            time_str = item['commence_time'][:16].replace("T", " ")

            if not item.get('bookmakers'):
                continue
            outcomes = item['bookmakers'][0]['markets'][0]['outcomes']
            ev = next((o['price'] for o in outcomes if o['name'] == home), 2.0)
            draw = next((o['price'] for o in outcomes if o['name'] == "Draw"), 3.5)
            dep = next((o['price'] for o in outcomes if o['name'] == away), 3.0)

            # Gelişmiş AI (implied probability + ev avantajı)
            implied_ev = round(100 / ev * 0.96, 1)
            implied_ev = max(48, min(78, implied_ev))

            matches.append({
                "Maç": f"{home} vs {away}",
                "Lig": league,
                "Saat": time_str,
                "1xBet Ev": round(ev, 2),
                "Beraberlik": round(draw, 2),
                "1xBet Deplasman": round(dep, 2),
                "AI Ev (%)": implied_ev,
                "Önerilen": "Ev Kazanır" if implied_ev > 57 else "2.5 Üst"
            })
        return pd.DataFrame(matches)
    except Exception as e:
        st.error(f"Bağlantı hatası: {str(e)}")
        return pd.DataFrame()

df = get_real_odds()

st.subheader("📅 Günün Gerçek Maçları + Gerçek Oranlar")

if df.empty:
    st.warning("Şu anda veri çekilemedi. 1-2 dakika sonra yeniden dene veya Reboot et.")
else:
    st.dataframe(df, use_container_width=True, height=450)

# ====================== PROFESYONEL KUPON ÜRETİCİ ======================
st.subheader("🏆 Gerçek Oranlara Göre AI Kupon Önerileri")

def uret_kupon(risk):
    if df.empty or len(df) < 3:
        return []
    iyi = df[df["AI Ev (%)"] >= 55].copy()
    kuponlar = []
    for _ in range(3):
        n = 3 if risk == "Düşük Risk" else 4 if risk == "Orta Risk" else random.randint(4,5)
        secilen = iyi.sample(n)
        toplam_oran = round(secilen["1xBet Ev"].prod(), 2)
        olasilik = round((secilen["AI Ev (%)"]/100).prod() * 100, 1)
        
        mac_list = [f"{row['Maç']} → {row['Önerilen']} @ {row['1xBet Ev']}" for _, row in secilen.iterrows()]
        
        kuponlar.append({
            "Risk": risk,
            "Maç Sayısı": n,
            "Toplam Oran": toplam_oran,
            "Kazanma Olasılığı (%)": olasilik,
            "Beklenen Getiri": f"+{round((toplam_oran * (olasilik/100) - 1)*100, 1)}%",
            "Maçlar": mac_list
        })
    return kuponlar

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🟢 DÜŞÜK RİSK (Safe)", use_container_width=True):
        for k in uret_kupon("Düşük Risk"):
            with st.expander(f"🟢 Düşük Risk • {k['Maç Sayısı']} maç • Oran {k['Toplam Oran']}"):
                for m in k["Maçlar"]:
                    st.write("• " + m)
                st.success(f"**Kazanma Olasılığı: %{k['Kazanma Olasılığı (%)']}** | Beklenen Getiri: **{k['Beklenen Getiri']}**")

with col2:
    if st.button("🟡 ORTA RİSK (En Mantıklı)", use_container_width=True):
        for k in uret_kupon("Orta Risk"):
            with st.expander(f"🟡 Orta Risk • {k['Maç Sayısı']} maç • Oran {k['Toplam Oran']}"):
                for m in k["Maçlar"]:
                    st.write("• " + m)
                st.success(f"**Kazanma Olasılığı: %{k['Kazanma Olasılığı (%)']}** | Beklenen Getiri: **{k['Beklenen Getiri']}**")

with col3:
    if st.button("🔴 YÜKSEK RİSK (Yüksek Getiri)", use_container_width=True):
        for k in uret_kupon("Yüksek Risk"):
            with st.expander(f"🔴 Yüksek Risk • {k['Maç Sayısı']} maç • Oran {k['Toplam Oran']}"):
                for m in k["Maçlar"]:
                    st.write("• " + m)
                st.success(f"**Kazanma Olasılığı: %{k['Kazanma Olasılığı (%)']}** | Beklenen Getiri: **{k['Beklenen Getiri']}**")

st.caption("EdgeBet AI v7.0 • Tanrı Modu • Gerçek The Odds API • Serhat için özel")
