import streamlit as st
import pandas as pd
import plotly.express as px


# Sayfa ayarları
st.set_page_config(
    page_title="Candy Problem Analizi",
    page_icon="🍬",
    layout="wide"
)


# Başlık
st.title("🍬 Candy Production Problem")
st.subheader("Optimal Çözümün Veri Analizi ve Görselleştirilmesi")


# PuLP ile elde ettiğimiz optimal çözüm
data = {
    "Ürün": ["Slugger", "Easy Out"],
    "Şeker (oz)": [60, 40],
    "Fındık (oz)": [10, 10],
    "Çikolata (oz)": [30, 0],
    "Toplam Üretim (oz)": [100, 50],
    "Birim Fiyat ($/oz)": [0.20, 0.25]
}


# Pandas DataFrame oluşturma
df = pd.DataFrame(data)


# Gelir hesaplama
df["Gelir ($)"] = (
    df["Toplam Üretim (oz)"] *
    df["Birim Fiyat ($/oz)"]
)


# Toplam üretim ve gelir
toplam_uretim = df["Toplam Üretim (oz)"].sum()
toplam_gelir = df["Gelir ($)"].sum()


# Üretim yüzdesi
df["Üretim Payı (%)"] = (
    df["Toplam Üretim (oz)"] /
    toplam_uretim * 100
)


# -----------------------------------------
# GENEL SONUÇLAR
# -----------------------------------------

st.header("Genel Sonuçlar")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Toplam Üretim",
    f"{toplam_uretim:.0f} oz"
)

col2.metric(
    "Toplam Gelir",
    f"${toplam_gelir:.2f}"
)

col3.metric(
    "Ürün Sayısı",
    len(df)
)


# -----------------------------------------
# ÇÖZÜM TABLOSU
# -----------------------------------------

st.header("Optimal Çözüm Tablosu")

st.dataframe(
    df,
    use_container_width=True
)


# -----------------------------------------
# ÜRETİM GRAFİĞİ
# -----------------------------------------

st.header("Ürün Bazında Üretim")

fig1 = px.bar(
    df,
    x="Ürün",
    y="Toplam Üretim (oz)",
    title="Optimal Üretim Miktarları"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)


# -----------------------------------------
# GELİR GRAFİĞİ
# -----------------------------------------

st.header("Ürün Bazında Gelir")

fig2 = px.bar(
    df,
    x="Ürün",
    y="Gelir ($)",
    title="Ürünlerin Gelire Katkısı"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)


# -----------------------------------------
# ÜRETİM DAĞILIMI
# -----------------------------------------

st.header("Üretim Dağılımı")

fig3 = px.pie(
    df,
    names="Ürün",
    values="Toplam Üretim (oz)",
    title="Toplam Üretimin Ürünlere Göre Dağılımı"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)


# -----------------------------------------
# KAYNAK KULLANIMI
# -----------------------------------------

st.header("Kaynak Kullanımı")

kaynaklar = pd.DataFrame({
    "Kaynak": ["Şeker", "Fındık", "Çikolata"],
    "Kullanılan (oz)": [100, 20, 30],
    "Mevcut (oz)": [100, 20, 30]
})

st.dataframe(
    kaynaklar,
    use_container_width=True
)


fig4 = px.bar(
    kaynaklar,
    x="Kaynak",
    y=["Kullanılan (oz)", "Mevcut (oz)"],
    barmode="group",
    title="Kaynak Kullanımı"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)
