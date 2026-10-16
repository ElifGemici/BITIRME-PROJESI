import pandas as pd


data = {
    "Ürün": ["Slugger", "Easy Out"],
    "Şeker (oz)": [60, 40],
    "Fındık (oz)": [10, 10],
    "Çikolata (oz)": [30, 0],
    "Toplam Üretim (oz)": [100, 50],
    "Birim Fiyat ($/oz)": [0.20, 0.25]
}


df = pd.DataFrame(data)


df["Gelir ($)"] = (
    df["Toplam Üretim (oz)"] *
    df["Birim Fiyat ($/oz)"]
)

print("\n--- CANDY PROBLEMİ ÇÖZÜM TABLOSU ---")
print(df)


toplam_seker = df["Şeker (oz)"].sum()
toplam_findik = df["Fındık (oz)"].sum()
toplam_cikolata = df["Çikolata (oz)"].sum()

print("\n--- KAYNAK KULLANIMI ---")
print("Toplam şeker kullanımı:", toplam_seker, "oz")
print("Toplam fındık kullanımı:", toplam_findik, "oz")
print("Toplam çikolata kullanımı:", toplam_cikolata, "oz")


toplam_uretim = df["Toplam Üretim (oz)"].sum()


toplam_gelir = df["Gelir ($)"].sum()

print("\n--- GENEL SONUÇLAR ---")
print("Toplam üretim:", toplam_uretim, "oz")
print("Toplam gelir:", toplam_gelir, "$")


df["Üretim Payı (%)"] = (
    df["Toplam Üretim (oz)"] / toplam_uretim * 100
)

print("\n--- ÜRETİM PAYLARI ---")
print(df[["Ürün", "Üretim Payı (%)"]])
