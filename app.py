import streamlit as st
import pandas as pd
from veri_analizi import analiz_verisini_hazirla

st.set_page_config(page_title="Airco Üretim Analizi", layout="wide")

st.title("Airco Üretim ve Maliyet Analizi")
st.write("Optimizasyon sonuçlarından elde edilen veri analizi.")

# Analiz dosyasından hesaplanmış tabloyu al
df = analiz_verisini_hazirla()
df["Ay"] = df["Ay"].apply(lambda ay: f"Ay {ay}")

# Genel göstergeler
col1, col2, col3 = st.columns(3)
col1.metric("Toplam Talep", f"{df['Talep'].sum():,.0f} birim")
col2.metric("Toplam Üretim", f"{df['Toplam Üretim'].sum():,.0f} birim")
col3.metric("Toplam Maliyet", f"${df['Toplam Maliyet ($)'].sum():,.0f}")

# Üretim ve talep grafiği
st.subheader("Aylık Talep ve Üretim")
uretim_verisi = df.set_index("Ay")[
    ["Talep", "New York Üretimi", "Los Angeles Üretimi"]
]
st.bar_chart(uretim_verisi)

# Analiz sonuçlarının grafikleri
st.subheader("Aylık Maliyet Analizi")
maliyet_verisi = df.set_index("Ay")[
    ["Üretim Maliyeti ($)", "Stok Maliyeti ($)"]
]
st.bar_chart(maliyet_verisi)

st.subheader("Talep Karşılama Oranı (%)")
st.line_chart(df.set_index("Ay")["Talep Karşılama (%)"])

# Analiz tablosu
st.subheader("Veri Analizi Sonuç Tablosu")
st.dataframe(df, use_container_width=True)

st.success(
    "Analiz tablosu veri_analizi.py dosyasından alınmıştır. "
    "Başlangıç stoku dahil tüm aylarda talep karşılanmaktadır."
)
