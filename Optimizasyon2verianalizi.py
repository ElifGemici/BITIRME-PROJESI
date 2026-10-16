import pandas as pd
import numpy as np

"""
PROJE: Bitirme Projesi - Sprint 1 (Veri Analizi Modülü)
PROBLEM: Winston Tablo 82 - 3 Fabrika ve 4 Müşteri Nakliye Kâr Veri Analizi

DETAYLI PROBLEM TANIMI VE VERİ SETİ METNİ:
-----------------------------------------------------------------------------
Tek ürün üreten bir firmanın 3 fabrikası (Plant) ve 4 müşterisi (Customer) vardır.
- Fabrika üretim kapasiteleri:
  * Plant 1: 3,000 birim
  * Plant 2: 5,000 birim
  * Plant 3: 5,000 birim
  (Toplam Arz = 13,000 birim)
- Müşteri taahhütleri ve talepleri:
  * Müşteri 1: Kesin taahhüt 4,000 birim
  * Müşteri 2: Kesin taahhüt 3,000 birim
  * Müşteri 3: En az 3,000 birim
  * Müşteri 3 ve 4 kalan birimleri paylaşmak istemektedir.
- Tablo 82 Birim Sevkiyat Kârları ($):
  * Plant 1 -> Müşteri 1: 65, Müşteri 2: 63, Müşteri 3: 62, Müşteri 4: 64
  * Plant 2 -> Müşteri 1: 68, Müşteri 2: 67, Müşteri 3: 65, Müşteri 4: 62
  * Plant 3 -> Müşteri 1: 63, Müşteri 2: 60, Müşteri 3: 59, Müşteri 4: 60
"""

print("=" * 70)
print("     WINSTON TABLO 82: NAKLİYE VE KÂR SAYISAL VERİ ANALİZİ")
print("=" * 70)

# Tablo 82 Kâr Matrisi ve Fabrika Arz Verilerini DataFrame Formatına Aktarma
veri = {
    'Fabrika': ['Plant 1', 'Plant 2', 'Plant 3'],
    'Uretim_Kapasitesi': [3000, 5000, 5000],
    'Musteri_1_Kar': [65, 68, 63],
    'Musteri_2_Kar': [63, 67, 60],
    'Musteri_3_Kar': [62, 65, 59],
    'Musteri_4_Kar': [64, 62, 60]
}

df = pd.DataFrame(veri)

print("\n--- 1. TABLO 82 ORİJİNAL KÂR VE KAPASİTE VERİ SETİ ---")
print(df)

print("\n" + "-" * 70)
print("--- 2. SAYISAL İSTATİSTİKSEL ÖZETLER (Describe & NumPy) ---")
# Kâr sütunlarının istatistiksel dağılımı
print(df[['Musteri_1_Kar', 'Musteri_2_Kar', 'Musteri_3_Kar', 'Musteri_4_Kar']].describe())

#  Genel ortalama kâr hesaplaması
tum_kar_degerleri = df[['Musteri_1_Kar', 'Musteri_2_Kar', 'Musteri_3_Kar', 'Musteri_4_Kar']].values
genel_ortalama_kar = np.mean(tum_kar_degerleri)
print(f"\n[NumPy Hesabı] Tüm Rotalar Geneli Ortalama Birim Kâr: {genel_ortalama_kar:.2f} USD")

print("\n" + "-" * 70)
print("--- 3. VEKTÖREL HESAPLAMALAR VE ROTA ORTALAMALARI ---")
# Fabrika bazında ortalama birim kâr marjları
df['Ortalama_Birim_Kar'] = df[['Musteri_1_Kar', 'Musteri_2_Kar', 'Musteri_3_Kar', 'Musteri_4_Kar']].mean(axis=1)

# NumPy np.select ile kâr seviyelendirmesi
kosullar = [df['Ortalama_Birim_Kar'] >= 65, df['Ortalama_Birim_Kar'] >= 62]
secenekler = ['Yüksek Kârlı Fabrika', 'Orta Kârlı Fabrika']
df['Fabrika_Kategori'] = np.select(kosullar, secenekler, default='Düşük Kârlı Fabrika')

print(df[['Fabrika', 'Uretim_Kapasitesi', 'Ortalama_Birim_Kar', 'Fabrika_Kategori']])

print("\n" + "-" * 70)
print("--- 4. KOŞULLU FİLTRELEME VE BETİMSEL ANALİZ ---")
# Birim kârın 65$ ve üzerinde olduğu rota eşikleri
yuksek_kar_filtresi = df[['Musteri_1_Kar', 'Musteri_2_Kar', 'Musteri_3_Kar', 'Musteri_4_Kar']] >= 65
print("Birim kârın 65 USD ve üzerinde olduğu rota matrisi (True/False):")
print(yuksek_kar_filtresi)

print("\n" + "=" * 70)
print("YÖNETSEL ÇIKARIMLAR VE VERİ ANALİZİ YORUMLARI:")
print("1. Plant 2, ortalama 65.50 USD birim kâr ile diğer fabrikalara kıyasla daha avantajlı bir yapı sunmaktadır.")
print("2. Müşteri 1 ve Müşteri 2 rotalarında birim kârlar genel olarak daha yüksek seyretmektedir.")
print("3. Bu veri analizi çalışması dönemsel birim kâr dağılımını betimsel olarak özetler;")
print("   kesin ve optimum sevkiyat planı ise kapasite ve talep kısıtları altında kurulan optimizasyon modeliyle belirlenecektir.")
print("=" * 70)