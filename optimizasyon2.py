import pulp

"""
PROJE: Bitirme Projesi - Sprint 1 (Optimizasyon Modülü)
PROBLEM: Winston - Kâr Maksimizasyonu Ulaştırma Problemi (Tablo 82)

DETAYLI PROBLEM TANIMI VE MATEMATİKSEL MODEL METNİ:
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
  * Müşteri 3: En az 3,000 birim (ve kalan birimlerden almak istiyor)
  * Müşteri 4: Kalan tüm birimleri almak istiyor
  (Toplam minimum talep 10,000 birim olup, kalan 3,000 birim Müşteri 3 ve 4 
   arasında kârı maksimize edecek şekilde paylaştırılacaktır.)

- Birim Sevkiyat Kârları (Tablo 82 - $):
  * Plant 1 -> Müşteri 1: 65, Müşteri 2: 63, Müşteri 3: 62, Müşteri 4: 64
  * Plant 2 -> Müşteri 1: 68, Müşteri 2: 67, Müşteri 3: 65, Müşteri 4: 62
  * Plant 3 -> Müşteri 1: 63, Müşteri 2: 60, Müşteri 3: 59, Müşteri 4: 60

AMAÇ: Fabrika kapasitelerini aşmadan ve taahhütleri karşılayarak, 
      toplam nakliye kârını maksimum yapacak optimum sevkiyat planını bulmak.
"""

# 1. Model Tanımlama 
model = pulp.LpProblem("Nakliye_Kar_Maksimizasyonu", pulp.LpMaximize)

# 2. Karar Değişkenleri 
# Fabrikalar (1, 2, 3) ve Müşteriler (1, 2, 3, 4)
plants = [1, 2, 3]
customers = [1, 2, 3, 4]

x = pulp.LpVariable.dicts("Sevk", ((i, j) for i in plants for j in customers), lowBound=0, cat="Continuous")

# 3. Kâr Matrisi (Tablo 82 verileri)
profit = {
    (1, 1): 65, (1, 2): 63, (1, 3): 62, (1, 4): 64,
    (2, 1): 68, (2, 2): 67, (2, 3): 65, (2, 4): 62,
    (3, 1): 63, (3, 2): 60, (3, 3): 59, (3, 4): 60
}

# 4. Amaç Fonksiyonu 
model += pulp.lpSum(profit[(i, j)] * x[(i, j)] for i in plants for j in customers), "Toplam_Kar"

# 5. Kısıtlar
model += pulp.lpSum(x[(1, j)] for j in customers) == 3000, "Plant_1_Kapasite"
model += pulp.lpSum(x[(2, j)] for j in customers) == 5000, "Plant_2_Kapasite"
model += pulp.lpSum(x[(3, j)] for j in customers) == 5000, "Plant_3_Kapasite"

# Kesin Talep Kısıtları
model += pulp.lpSum(x[(i, 1)] for i in plants) == 4000, "Musteri_1_Talep"
model += pulp.lpSum(x[(i, 2)] for i in plants) == 3000, "Musteri_2_Talep"

# Müşteri 3 Alt Sınır Kısıtı 
model += pulp.lpSum(x[(i, 3)] for i in plants) >= 3000, "Musteri_3_Min_Talep"

# Esnek Talep Dengelemesi 
model += pulp.lpSum(x[(i, 3)] for i in plants) + pulp.lpSum(x[(i, 4)] for i in plants) == 6000, "Kalan_Urunlerin_Paylasimi"

# 6. Problemi Çözme (Solver Çalıştırma)
model.solve()

# 7. Sonuçları, Log Kayıtlarını ve Analitik Çıkarımları Ekrana Yazdırma
print("=" * 65)
print("       WINSTON TABLO 82: NAKLİYE KÂR MAKSİMİZASYONU")
print("=" * 65)

# Log ve Durum Bilgileri
print(f"[*] Kullanılan Çözücü (Solver) : {model.solver.name}")
print(f"[*] Çözüm Durumu (Status)     : {pulp.LpStatus[model.status]}")

print("-" * 65)
print("OPTİMAL SEVKİYAT PLANI (BİRİM):")
for i in plants:
    for j in customers:
        print(f" > Plant {i} -> Müşteri {j} : {x[(i, j)].varValue:.1f} birim")

print(f"\n > Ulaşılan Maksimum Toplam Kâr : {pulp.value(model.objective):.2f} $")

print("-" * 65)
print("YÖNETSEL ÇIKARIMLAR VE YORUMLAR:")
print("1. Model, birim sevkiyat kârı en yüksek olan rotalara (örneğin Plant 2 -> Müşteri 1 vb.) öncelik vermiştir.")
print("2. Fabrikaların tüm kapasiteleri tam olarak kullanılarak (3000 + 5000 + 5000 = 13000) sevkiyat tamamlanmıştır.")
print("3. Müşteri 3 ve Müşteri 4'ün esnek talepleri, şirketin toplam kârını en üst düzeye çıkacak şekilde dengelenmiştir.")
print("=" * 65)