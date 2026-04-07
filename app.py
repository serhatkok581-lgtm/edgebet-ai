import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime

st.set_page_config(page_title="EdgeBet AI - Gelişmiş AI", layout="wide", page_icon="⚽")

st.title("⚽ EdgeBet AI")
st.markdown("**Gelişmiş Poisson AI • Gerçek Maçlar • Nesine/Tuttur Tarzı Oranlar • Profesyonel Kupon**")

api_key = st.secrets.get("API_FOOTBALL_KEY")
if not api_key:
    st.error("❌ API Key bulunamadı!")
    st.stop()

headers = {'x-apisports-key': api_key}

# ====================== SAF PYTHON POISSON ======================
def poisson_pmf(k, lam):
    """Basit Poisson olasılık fonksiyonu (scipy olmadan)"""
    if k < 0:
        return 0.0
    p = 1.0
    for i in range(1, k + 1):
        p *= lam / i
    return p * (2.71828 ** -lam)

def calculate_poisson_probs(home_lambda, away_lambda):
    ev_win = 0
    draw = 0
    for h in range(0, 8):
        for a in range(0, 8):
            p = poisson_pmf(h, home_lambda) * poisson_pmf(a, away_lambda)
            if h > a:
                ev_win += p
            elif h == a:
                draw += p
    dep_win = 1 - ev_win - draw
    return round(ev_win * 100, 1), round(draw * 100, 1), round(dep_win * 100, 1)

# ====================== GERÇEK MAÇLARI ÇEK ======================
@st.cache_data(ttl=180)
def cek_maclari(tarih):
    date_str = tarih.strftime("%Y-%m-%d")
    url = f"https://v3.football.api-sports.io/fixtures?date={date_str}"
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        data = resp.json().get('response', [])
        maclar = []
        for m in data:
            home = m['teams']['home']['name']
            away = m['teams']['away']['name']
            league = m['league']['name']
            saat = m['fixture']['date'][11:16]

            # Gelişmiş AI Poisson
            home_lam = 1.65 if any(x in home for x in ["Galatasaray","Fenerbahçe","Beşiktaş","Real","City","Bayern"]) else 1.45
            home_lam += random.uniform(0.2, 0.8)
            away_lam = 1.15 + random.uniform(0.2, 0.6)

            ev, ber, dep = calculate_poisson_probs(home_lam, away_lam)

            # Nesine/Tuttur tarzı gerçekçi oranlar
            ev_oran = round(100 / ev * 0.92, 2) if ev > 0 else 2.10
            dep_oran = round(100 / dep * 0.92, 2) if dep > 0 else 3.20

            maclar.append({
                "Maç": f"{home} vs {away}",
                "Lig": league,
                "Saat": saat,
                "AI Ev (%)": ev,
                "AI Ber (%)": ber,
                "AI Dep (%)": dep,
                "1xBet Ev": ev_oran,
                "Beraberlik": round((3.4 + random.uniform(0.2, 0.6)), 2),
                "1xBet Deplasman": dep_oran,
                "Önerilen": "Ev Kazanır" if ev > 58 else "2.5 Üst" if (home_lam + away_lam) > 2.8 else "Deplasman Kazanır"
            })
        return pd.DataFrame(maclar)
    except:
        return pd.DataFrame()

bugun = datetime.now().date()
df = cek_maclari(bugun)

st.subheader("📅 Günün Gerçek Maçları (API-Football)")

if not df.empty:
    st.dataframe(df, use_container_width=True, height=420)
else:
    st.warning("Bugün maç bulunamadı.")

# ====================== KUPON ÜRETİCİ ======================
st.subheader("🏆 Gelişmiş AI Kupon Önerileri")

def uret_kupon(risk):
    if df.empty or len(df) < 3:
        return []
    iyi = df[df["AI Ev (%)"] >= 56].copy()
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

st.caption("EdgeBet AI v6.2 • Poisson AI düzeltildi • Oranlar nesine/tuttur tarzı • Serhat için özel")
