import streamlit as st
import pandas as pd
import numpy as np

# Sayfa Yapılandırması
st.set_page_config(page_title="U.S. Labs Tedarik Analizi", page_icon="🏥", layout="wide")

# Başlık ve Açıklama
st.title("🏥 U.S. Labs Kalp Kapakçığı Tedarik ve Maliyet Analizi")
st.markdown("Bu panel, Winston Tablo 3 verilerine dayanarak **U.S. Labs** tedarikçi maliyetlerini ve boyut dağılımlarını incelemek için **Streamlit** ile hazırlanmıştır.")

# Veri Seti Tanımlama
veri = {
    'Tedarikci_ID': ['Tedarikçi 1', 'Tedarikçi 2', 'Tedarikçi 3'],
    'Birim_Maliyet_USD': [5, 4, 3],
    'Yuzde_Buyuk': [40, 30, 20],
    'Yuzde_Orta': [40, 35, 20],
    'Yuzde_Kucuk': [20, 35, 60],
    'Maks_Kapasite_Adet': [700, 700, 700]
}

df = pd.DataFrame(veri)

# Vektörel Hesaplamalar
df['Maks_Buyuk_Adet'] = (df['Maks_Kapasite_Adet'] * df['Yuzde_Buyuk']) / 100
df['Maks_Orta_Adet']  = (df['Maks_Kapasite_Adet'] * df['Yuzde_Orta']) / 100
df['Maks_Kucuk_Adet'] = (df['Maks_Kapasite_Adet'] * df['Yuzde_Kucuk']) / 100

# Ana Tabloyu Gösterme
st.subheader("📋 Tablo 3: Tedarikçi Maliyet ve Boyut Oranları")
st.dataframe(df, use_container_width=True)

# Temel Metrikler
col1, col2, col3 = st.columns(3)
col1.metric("Ortalama Birim Maliyet", f"{df['Birim_Maliyet_USD'].mean():.2f} $")
col2.metric("En Düşük Birim Maliyet", f"{df['Birim_Maliyet_USD'].min()} $ (Tedarikçi 3)")
col3.metric("Maksimum Tedarik Kapasitesi", f"{df['Maks_Kapasite_Adet'].sum()} Adet")

# Görselleştirme (Grafikler)
st.subheader("📈 Tedarikçi Birim Maliyet Karşılaştırması")
st.bar_chart(df.set_index('Tedarikci_ID')['Birim_Maliyet_USD'])

st.subheader("📊 Tedarikçilerin Boyut Dağılım Yüzdeleri (%)")
st.bar_chart(df.set_index('Tedarikci_ID')[['Yuzde_Buyuk', 'Yuzde_Orta', 'Yuzde_Kucuk']])

# Yönetsel Çıkarımlar 
st.markdown("---")
st.subheader("💡 Yönetsel Çıkarımlar ve Analiz Notları")
st.markdown("""
1. **Tedarikçi 3** $3 ile en ucuz birim fiyata sahiptir ancak %60 oranında küçük kapakçık sağlamaktadır.
2. Büyük kapakçık talebini karşılamak için **Tedarikçi 1** (%40 büyük payı) kritik bir rol oynamaktadır.
3. Bu görselleştirme, maliyet minimizasyonu optimizasyon modelinin arkasındaki kısıt dengelerini doğrulamaktadır.
""")