import pandas as pd
import numpy as np

"""
PROJE: Bitirme Projesi - Sprint 1 (Veri Analizi Modülü)
PROBLEM: Winston Tablo 3 - U.S. Labs Kalp Kapakçığı Sayısal Veri Analizi
"""

print("=" * 70)
print("     WINSTON TABLO 3: U.S. LABS SAYISAL VERİ ANALİZİ (PANDAS & NUMPY)")
print("=" * 70)

# 1. Tablo 3 Verilerini Pandas DataFrame Formatına Aktarma
veri = {
    'Tedarikci_ID': [1, 2, 3],
    'Birim_Maliyet_USD': [5, 4, 3],
    'Yuzde_Buyuk': [40, 30, 20],
    'Yuzde_Orta': [40, 35, 20],
    'Yuzde_Kucuk': [20, 35, 60],
    'Maks_Kapasite_Adet': [700, 700, 700]
}

df = pd.DataFrame(veri)

print("\n--- 1. TABLO 3 ORİJİNAL VERİ SETİ ---")
print(df)

print("\n" + "-" * 70)
print("--- 2. TEDARİKÇİ VERİLERİNİN İSTATİSTİKSEL ÖZETİ (Describe) ---")
# Sayısal sütunların ortalama, min, max, standart sapma değerleri
print(df[['Birim_Maliyet_USD', 'Yuzde_Buyuk', 'Yuzde_Orta', 'Yuzde_Kucuk']].describe())

print("\n" + "-" * 70)
print("--- 3. VEKTÖREL HESAPLAMALAR VE POTANSİYEL KAPASİTE ANALİZİ ---")
# Maksimum kapasitede (700 adet) alım yapılırsa her tedarikçiden kaç adet büyük/orta/küçük kapakçık gelir?
df['Maks_Buyuk_Adet'] = (df['Maks_Kapasite_Adet'] * df['Yuzde_Buyuk']) / 100
df['Maks_Orta_Adet']  = (df['Maks_Kapasite_Adet'] * df['Yuzde_Orta']) / 100
df['Maks_Kucuk_Adet'] = (df['Maks_Kapasite_Adet'] * df['Yuzde_Kucuk']) / 100
df['Maks_Toplam_Maliyet_USD'] = df['Maks_Kapasite_Adet'] * df['Birim_Maliyet_USD']

print(df[['Tedarikci_ID', 'Birim_Maliyet_USD', 'Maks_Buyuk_Adet', 'Maks_Orta_Adet', 'Maks_Kucuk_Adet', 'Maks_Toplam_Maliyet_USD']])

print("\n" + "-" * 70)
print("--- 4. KOŞULLU FİLTRELEME VE KARŞILAŞTIRMA ---")
# En ucuz tedarikçi ($3) kimdir ve ürün dağılımı nasıldır?
en_ucuz_tedarikci = df[df['Birim_Maliyet_USD'] == df['Birim_Maliyet_USD'].min()]
print("En düşük birim maliyetli tedarikçi:")
print(en_ucuz_tedarikci[['Tedarikci_ID', 'Birim_Maliyet_USD', 'Yuzde_Buyuk', 'Yuzde_Orta', 'Yuzde_Kucuk']])

# Büyük kapakçık oranı %30 ve üzerinde olan tedarikçiler:
yuksek_buyuk_oran = df[df['Yuzde_Buyuk'] >= 30]
print("\nBüyük boy kapakçık oranı %30 ve üzerinde olan tedarikçiler:")
print(yuksek_buyuk_oran[['Tedarikci_ID', 'Birim_Maliyet_USD', 'Yuzde_Buyuk']])

print("\n" + "=" * 70)
print("YÖNETSEL ÇIKARIMLAR VE VERİ ANALİZİ YORUMLARI:")
print("1. Tedarikçi 3 en ucuz birim fiyata ($3) sahiptir ancak %60 oranında küçük kapakçık sağlamaktadır.")
print("2. Büyük kapakçık ihtiyacı (min 500 adet) en yüksek olan kısıt olduğu için,")
print("   %40 büyük kapakçık sunan Tedarikçi 1 ($5) kilit rol oynamaktadır.")
print("3. Bu veri analizi çalışması, optimizasyon modelinin alt yapısını ve kısıt dengelerini kanıtlamaktadır.")
print("=" * 70)