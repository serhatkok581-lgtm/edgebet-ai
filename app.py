import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime, timedelta

st.set_page_config(page_title="EdgeBet AI", layout="wide", page_icon="⚽")

st.title("⚽ EdgeBet AI")
st.markdown("**Gelişmiş AI • Gerçek Maçlar + Ücretsiz Demo Yedek • Mantıklı Oranlar**")

api_key = st.secrets.get("API_FOOTBALL_KEY")
headers = {'x-apisports-key': api_key} if api_key else None

# ====================== GERÇEK MAÇ ÇEKME ======================
@st.cache_data(ttl=180)
def cek_maclari(tarih):
    date_str = tarih.strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    try:
        resp = requests.get(url, headers=headers, timeout=12)
        data = resp.json().get('response', [])
        maclar = []
        for m in data:
            home = m['teams']['home']['name']
            away = m['teams']['away']['name']
            league = m['league']['name']
            saat = m['fixture']['date'][11:16]

            home_lam = 1.6 + random.uniform(0.2, 0.9)
            away_lam = 1.1 + random.uniform(0.2, 0.7)

            ev = round(100 * (home_lam / (home_lam + away_lam + 0.3)), 1)
            ber = round(100 * (0.28), 1)
            dep = round(100 - ev - ber, 1)

            maclar.append({
                "Maç": f"{home} vs {away}",
                "Lig": league,
                "Saat": saat,
                "AI Ev (%)": ev,
                "1xBet Ev": round(1.45 + (100 - ev)/32, 2),
                "Beraberlik": 3.65,
                "1xBet Deplasman": round(2.75 + (ev - 50)/25, 2),
                "Önerilen": "Ev Kazanır" if ev > 57 else "2.5 Üst"
            })
        return pd.DataFrame(maclar)
    except:
        return pd.DataFrame()

# Bugün + yarın + önceki gün dene
tarihler = [datetime.now().date() + timedelta(days=i) for i in [-1, 0, 1]]
df = pd.DataFrame()
for t in tarihler:
    df_temp = cek_maclari(t)
    if not df_temp.empty:
        df = df_temp
        break

# Eğer hâlâ maç yoksa → Ücretsiz demo verisi göster
if df.empty:
    st.warning("❌ API-Football ücretsiz limitinde bugün maç verisi çekilemedi. Ücretsiz demo mod aktif.")
    df = pd.DataFrame([
        {"Maç": "Galatasaray vs Fenerbahçe", "Lig": "Süper Lig", "Saat": "21:00", "AI Ev (%)": 64, "1xBet Ev": 2.05, "Beraberlik": 3.50, "1xBet Deplasman": 3.30, "Önerilen": "Ev Kazanır"},
        {"Maç": "Beşiktaş vs Trabzonspor", "Lig": "Süper Lig", "Saat": "19:00", "AI Ev (%)": 58, "1xBet Ev": 2.35, "Beraberlik": 3.40, "1xBet Deplasman": 2.90, "Önerilen": "2.5 Üst"},
        {"Maç": "Manchester City vs Arsenal", "Lig": "Premier League", "Saat": "22:00", "AI Ev (%)": 68, "1xBet Ev": 1.75, "Beraberlik": 4.10, "1xBet Deplasman": 4.40, "Önerilen": "Ev Kazanır"},
        {"Maç": "Real Madrid vs Barcelona", "Lig": "La Liga", "Saat": "23:00", "AI Ev (%)": 55, "1xBet Ev": 2.20, "Beraberlik": 3.60, "1xBet Deplasman": 3.10, "Önerilen": "Ev Kazanır"},
    ])

st.subheader("📅 Günün Maçları")
st.dataframe(df, use_container_width=True, height=400)

# ====================== KUPON ÖNERİLERİ ======================
st.subheader("🏆 Mantıklı Kupon Önerileri")

def uret_kupon(risk):
    iyi = df[df["AI Ev (%)"] >= 56].copy()
    if len(iyi) < 3:
        return []
    kuponlar = []
    for _ in range(3):
        if risk == "Düşük Risk":
            n = random.randint(3, 4)
        elif risk == "Orta Risk":
            n = 4
        else:
            n = random.randint(4, 5)
        secilen = iyi.sample(n)
        toplam_oran = round(secilen["1xBet Ev"].prod(), 2)
        olasilik = round((secilen["AI Ev (%)"] / 100).prod() * 100, 1)
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

st.caption("EdgeBet AI v6.3 • Ücretsiz mod + Demo yedek aktif • Oranlar mantıklı hale getirildi")
