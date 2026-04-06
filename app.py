import streamlit as st
import pandas as pd
import time

st.set_page_config(
    page_title="EdgeBet AI - Serhat'ın Makinesi",
    layout="wide",
    page_icon="⚽",
    initial_sidebar_state="expanded"
)

st.title("⚽ EdgeBet AI")
st.markdown("**Serhat'ın Bahis Makinesi** • 1xBet Odaklı • Yüksek Olasılıklı Tahminler • Sadece Futbol")

# Sidebar Filtreler
st.sidebar.header("⚙️ Filtreler")
selected_lig = st.sidebar.selectbox(
    "Lig Seçin",
    ["Tüm Ligler", "Süper Lig", "Premier League", "La Liga", "Bundesliga", "Serie A", "Championship", "Alt Ligler"]
)
min_prob = st.sidebar.slider("Minimum Kazanma Olasılığı (%)", 50, 90, 60)
refresh_btn = st.sidebar.button("🔄 Oranları ve Tahminleri Yenile")

# Demo Veri Tablosu
data = {
    "Maç": [
        "Galatasaray vs Fenerbahçe", 
        "Manchester City vs Arsenal", 
        "Real Madrid vs Barcelona", 
        "Trabzonspor vs Başakşehir", 
        "Bayern Münih vs Borussia Dortmund"
    ],
    "Lig": ["Süper Lig", "Premier League", "La Liga", "Süper Lig", "Bundesliga"],
    "Tarih": [
        "07 Nisan 2026 - 21:00", 
        "08 Nisan 2026 - 22:00", 
        "09 Nisan 2026 - 23:00", 
        "10 Nisan 2026 - 20:00", 
        "11 Nisan 2026 - 19:30"
    ],
    "1xBet Ev": [2.15, 1.68, 1.92, 2.45, 1.75],
    "1xBet Beraberlik": [3.50, 4.20, 3.80, 3.40, 4.10],
    "1xBet Deplasman": [3.10, 4.75, 3.95, 2.75, 4.50],
    "AI Kazanma Olasılığı (%)": [59, 64, 57, 51, 68],
    "Value Bet": ["✅ EVET (+14%)", "✅ EVET (+9%)", "❌ Hayır", "⚠️ Şüpheli", "✅ EVET (+11%)"],
    "Uyarı": ["", "Ani Oran Düşüşü!", "", "Whale Alert (Under)", ""]
}

df = pd.DataFrame(data)

if refresh_btn:
    st.success("✅ Oranlar ve tahminler yenilendi!")
    time.sleep(0.8)
    st.rerun()

# Ana Tablo
st.subheader("📊 Günün Maçları ve AI Tahminleri")
st.dataframe(
    df.style.background_gradient(cmap='RdYlGn', subset=['AI Kazanma Olasılığı (%)'])
    .apply(lambda x: ['background-color: #90EE90' if 'EVET' in str(v) else 'background-color: #FFB347' if 'Şüpheli' in str(v) else '' for v in x], axis=1),
    use_container_width=True,
    height=450
)

# Kupon ve Uyarılar
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🏆 Önerilen 1xBet Kuponu")
    st.markdown("**Güvenli 3’lü Kupon Önerisi**")
    st.write("• Galatasaray Kazanır → **2.15**")
    st.write("• Manchester City Kazanır → **1.68**")
    st.write("• Bayern Münih Kazanır → **1.75**")
    st.success("**Toplam Oran: 6.32**   →   100 TL bahis → **632 TL** potansiyel kazanç")
    
    if st.button("📋 Kuponu Kopyala"):
        st.toast("Kupon kopyalandı! 1xBet'e yapıştırabilirsin.")

with col2:
    st.subheader("🔥 AI Uyarıları ve Analiz")
    st.warning("**Man City maçı:** Oran ani düştü → Value fırsat!")
    st.info("**Galatasaray maçı:** Kadro ve xG üstünlüğü ev sahibinde (%59)")
    st.error("**Trabzonspor maçı:** Under tarafında yüksek hacim tespit edildi (Whale hareketi)")

# Alt Bilgi
st.caption("Bu şu an demo versiyondur. Gerçek API'ler eklendiğinde (The Odds API, API-Football) çok daha güçlü ve otomatik olacak.")
st.markdown("---")
st.markdown("❤️ Serhat için özel yapıldı • EdgeBet AI • Sadece Futbol")