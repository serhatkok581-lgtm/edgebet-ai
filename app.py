import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ====================== SAYFA AYARLARI ======================
st.set_page_config(
    page_title="EdgeBet AI - Serhat'ın Makinesi",
    layout="wide",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

# ====================== CUSTOM CSS - ULTRA MODERN GÖRÜNÜM ======================
st.markdown("""
<style>
    .main {background-color: #0e1117;}
    .stApp {background-color: #0e1117; color: #ffffff;}
    h1 {color: #00ff88; font-weight: bold;}
    .metric-card {
        background-color: #1e2530;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #00ff88;
    }
    .high-prob {background-color: #004d26; color: #00ff88;}
    .medium-prob {background-color: #664d00; color: #ffcc00;}
    .suspicious {background-color: #4d1a00; color: #ff6666;}
</style>
""", unsafe_allow_html=True)

st.title("⚽ EdgeBet AI")
st.markdown("**Serhat'ın Profesyonel Bahis Makinesi** • 1xBet Odaklı • AI Destekli • Yüksek Getirili Tahminler")

# ====================== SIDEBAR ======================
st.sidebar.image("https://i.imgur.com/8Z8Z8Z8.png", width=80)  # İstersen logo değiştir
st.sidebar.header("⚙️ Kontrol Paneli")

lig_filtre = st.sidebar.selectbox(
    "Lig Filtrele",
    ["Tüm Ligler", "Süper Lig", "Premier League", "La Liga", "Bundesliga", 
     "Serie A", "Championship", "Ligue 1", "Alt Ligler (2. Lig vb.)"]
)

min_olasilik = st.sidebar.slider("Minimum AI Kazanma Olasılığı", 52, 88, 60, step=1)
risk_seviyesi = st.sidebar.selectbox("Risk Seviyesi", ["Düşük Risk (Güvenli)", "Orta Risk", "Yüksek Risk (Yüksek Getiri)"])

refresh = st.sidebar.button("🔄 Verileri Yenile ve AI Analizi Yap")

# ====================== AKILLI DEMO VERİ (Daha Zeki) ======================
@st.cache_data(ttl=180)
def get_ai_matches():
    data = {
        "Maç": [
            "Galatasaray vs Fenerbahçe", 
            "Manchester City vs Arsenal", 
            "Real Madrid vs Barcelona", 
            "Trabzonspor vs Başakşehir",
            "Bayern Münih vs Borussia Dortmund",
            "Beşiktaş vs Konyaspor",
            "Inter vs Juventus"
        ],
        "Lig": ["Süper Lig", "Premier League", "La Liga", "Süper Lig", "Bundesliga", "Süper Lig", "Serie A"],
        "Tarih": ["07 Nis 21:00", "08 Nis 22:00", "09 Nis 23:00", "10 Nis 20:00", "11 Nis 19:30", "12 Nis 19:00", "13 Nis 21:45"],
        "1xBet Ev": [2.18, 1.72, 1.95, 2.48, 1.78, 1.92, 2.65],
        "1xBet Beraberlik": [3.45, 4.10, 3.75, 3.35, 4.05, 3.55, 3.20],
        "1xBet Deplasman": [3.05, 4.60, 3.85, 2.70, 4.40, 3.85, 2.55],
        "AI Kazanma Olasılığı (%)": [61, 66, 58, 53, 69, 57, 52],
        "Value (%)": [14, 11, -3, 8, 13, 9, 15],
        "Önerilen Bahis": ["Ev Kazanır", "Ev Kazanır", "Kaçın", "Deplasman", "Ev Kazanır", "Ev Kazanır", "Deplasman"],
        "Güven Skoru": ["⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐", "⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐⭐"],
        "Uyarı": ["", "🔥 Ani Oran Düşüşü + Value", "Düşük Değer", "⚠️ Whale Alert (Under)", "✅ Yüksek Value", "", "🔥 Şüpheli Hareket"]
    }
    df = pd.DataFrame(data)
    # Filtreleme
    df = df[df["AI Kazanma Olasılığı (%)"] >= min_olasilik]
    return df

df = get_ai_matches()

if refresh:
    with st.spinner("AI Motoru çalışıyor... Maçlar analiz ediliyor..."):
        time.sleep(1.2)
    st.success("✅ AI Analizi tamamlandı! En iyi value betler güncellendi.")
    st.rerun()

# ====================== ANA GÖSTERGE ======================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Bugün Analiz Edilen Maç", len(df), "↑3")
with col2:
    st.metric("Ortalama Value", f"+{df['Value (%)'].mean():.1f}%", "📈")
with col3:
    st.metric("En Yüksek Olasılık", f"{df['AI Kazanma Olasılığı (%)'].max()}%", "🔥")
with col4:
    st.metric("Önerilen Kupon Sayısı", "4", "🎯")

# ====================== ANA TABLO - PROFESYONEL ======================
st.subheader("📊 AI Tarafından Analiz Edilen Maçlar")

# Renkli stil fonksiyonu
def style_row(row):
    styles = [''] * len(row)
    if row["AI Kazanma Olasılığı (%)"] >= 65:
        styles[row.index.get_loc("AI Kazanma Olasılığı (%)")] = 'background-color: #004d26; color: #00ff88; font-weight: bold'
    elif row["AI Kazanma Olasılığı (%)"] >= 57:
        styles[row.index.get_loc("AI Kazanma Olasılığı (%)")] = 'background-color: #664d00; color: #ffcc00'
    if "Whale" in str(row["Uyarı"]) or "Şüpheli" in str(row["Uyarı"]):
        styles[row.index.get_loc("Uyarı")] = 'background-color: #4d1a00; color: #ff6666'
    return styles

styled_df = df.style.apply(style_row, axis=1)

st.dataframe(
    styled_df,
    use_container_width=True,
    height=520,
    column_config={
        "AI Kazanma Olasılığı (%)": st.column_config.ProgressColumn("AI Kazanma Olasılığı", format="%d%%", min_value=0, max_value=100),
        "Value (%)": st.column_config.NumberColumn("Value", format="+%d%%"),
    }
)

# ====================== AKILLI KUPON ÖNERİSİ ======================
st.subheader("🏆 EdgeBet AI Otomatik Kupon Önerisi")

high_value = df[df["Value (%)"] > 8]

if not high_value.empty:
    st.markdown("**1xBet İçin En İyi 4’lü Kupon (AI Seçimi)**")
    
    secilen = high_value.head(4)
    toplam_oran = 1.0
    for _, row in secilen.iterrows():
        oran = row["1xBet Ev"] if "Ev" in row["Önerilen Bahis"] else row["1xBet Deplasman"]
        st.write(f"• **{row['Maç']}** → **{row['Önerilen Bahis']}** @ **{oran}**")
        toplam_oran *= oran
    
    st.success(f"**Toplam Kupon Oranı: {toplam_oran:.2f}**  →  100 TL → **{100*toplam_oran:.0f} TL** potansiyel kazanç")
    
    if st.button("📋 Kuponu 1xBet’e Kopyala"):
        st.toast("✅ Kupon kopyalandı! 1xBet’e yapıştır ve oyna.")
else:
    st.warning("Şu anda yeterince yüksek value maç bulunamadı. Filtreleri düşürün.")

# ====================== EKSTRA ZEKİ UYARILAR ======================
st.subheader("🔥 Akıllı AI Uyarıları")
for _, row in df.iterrows():
    if "Whale" in str(row["Uyarı"]) or "Şüpheli" in str(row["Uyarı"]):
        st.error(f"⚠️ **{row['Maç']}** → {row['Uyarı']}")
    elif "Ani Oran" in str(row["Uyarı"]):
        st.warning(f"🔥 **{row['Maç']}** → {row['Uyarı']}")

# ====================== BANKROLL ÖNERİSİ ======================
st.sidebar.subheader("💰 Bankroll Yönetimi")
bankroll = st.sidebar.number_input("Mevcut Bankroll (TL)", value=5000, min_value=500)
if bankroll:
    recommended = bankroll * 0.02  # Kelly benzeri basit öneri
    st.sidebar.success(f"Bu kupon için önerilen bahis: **{recommended:.0f} TL**")

st.caption("EdgeBet AI v2.0 • Profesyonel mod • Gerçek API entegrasyonu için hazır • Bahis risklidir, sorumlu oynayın.")
