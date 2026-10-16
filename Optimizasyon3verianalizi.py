import pandas as pd
import numpy as np

"""
PROJE: Bitirme Projesi - Sprint 1 (Veri Analizi Modülü)
PROBLEM: Winston Tablo 83 - Çok Dönemli Üretim ve Envanter Veri Analizi
"""

print("=" * 70)
print("     WINSTON TABLO 83: ÇOK DÖNEMLİ ÜRETİM VE ENVANTER VERİ ANALİZİ")
print("=" * 70)

# TABLO 83 Verileri
veri = {
    'Ay': [1, 2, 3],
    'Uretim_Maliyeti': [13, 12, 13],
    'Birincil_Talep': [20, 15, 25],
    'Ikincil_Talep_Limiti': [15, 20, 15],
    'Satis_Fiyati': [15, 14, 16],
    'Maks_Uretim_Kapasitesi': [35, 35, 35],
    'Stok_Maliyeti': [1, 1, 1]
}

df = pd.DataFrame(veri)

print("\n--- 1. TABLO 83 ORİJİNAL VERİ SETİ ---")
print(df)

print("\n" + "-" * 70)
print("--- 2. İSTATİSTİKSEL ÖZETLER (Describe & NumPy) ---")
# Sayısal sütunların istatistiksel dağılımı
print(df[['Uretim_Maliyeti', 'Birincil_Talep', 'Ikincil_Talep_Limiti', 'Satis_Fiyati']].describe())

# Ortalama maliyet ve fiyat hesaplamaları
ortalama_maliyet = np.mean(df['Uretim_Maliyeti'])
ortalama_fiyat = np.mean(df['Satis_Fiyati'])
print(f"\n[NumPy] Ortalama Üretim Maliyeti : {ortalama_maliyet:.2f} $")
print(f"[NumPy] Ortalama Satış Fiyatı     : {ortalama_fiyat:.2f} $")

print("\n" + "-" * 70)
print("--- 3. VEKTÖREL HESAPLAMALAR VE DÖNEMSEL KÂR MARJLARI ---")
# Birim kâr marjı hesaplaması
df['Birim_Kar_Marji'] = df['Satis_Fiyati'] - df['Uretim_Maliyeti']

# Birincil talep üzerinden potansiyel brüt gelir ve net kârlar
df['Birincil_Brut_Gelir'] = df['Birincil_Talep'] * df['Satis_Fiyati']
df['Birincil_Uretim_Maliyeti'] = df['Birincil_Talep'] * df['Uretim_Maliyeti']
df['Birincil_Net_Kar'] = df['Birincil_Brut_Gelir'] - df['Birincil_Uretim_Maliyeti']

print(df[['Ay', 'Uretim_Maliyeti', 'Satis_Fiyati', 'Birim_Kar_Marji', 'Birincil_Net_Kar']])

print("\n" + "-" * 70)
print("--- 4. KOŞULLU FİLTRELEME VE ANALİZ ---")
# Birim kâr marjının en yüksek olduğu dönemler
en_karli = df[df['Birim_Kar_Marji'] == df['Birim_Kar_Marji'].max()]
print("Birim kâr marjının en yüksek olduğu dönemler:")
print(en_karli[['Ay', 'Birim_Kar_Marji', 'Uretim_Maliyeti', 'Satis_Fiyati']])

print("\n" + "=" * 70)
print("YÖNETSEL ÇIKARIMLAR VE VERİ ANALİZİ YORUMLARI:")
print("1. Ay 3, birim başına 3 $ kâr marjı (16 $ satış, 13 $ maliyet) ile en yüksek kârlılığa sahiptir.")
print("2. Ay 2, 12 $ birim üretim maliyeti ile en düşük maliyetli üretim dönemidir.")
print("3. Bu veri analizi çalışması dönemsel maliyet ve gelir yapısını betimsel olarak özetler;")
print("   optimum envanter ve üretim planı ise kısıtlar altında kurulan optimizasyon modeliyle belirlenecektir.")
print("=" * 70)