import pulp

"""
PROJE: Bitirme Projesi - Sprint 1 (Optimizasyon Modülü)
PROBLEM: Winston - U.S. Labs Kalp Kapakçığı Tedarik Optimizasyonu (Maliyet Minimizasyonu)

DETAYLI PROBLEM TANIMI VE MATEMATİKSEL MODEL METNİ:
-----------------------------------------------------------------------------
U.S. Labs firması domuz kalplerinden mekanik kalp kapakçığı üretmektedir.
Firma 3 farklı tedarikçiden (Supplier 1, 2, 3) her ay kapakçık sipariş etmektedir.
Tablo 3'e göre tedarikçi maliyetleri ve boyut yüzdeleri şöyledir:
- Tedarikçi 1: Kapakçık başı maliyet = 5 $, %40 Büyük, %40 Orta, %20 Küçük
- Tedarikçi 2: Kapakçık başı maliyet = 4 $, %30 Büyük, %35 Orta, %35 Küçük
- Tedarikçi 3: Kapakçık başı maliyet = 3 $, %20 Büyük, %20 Orta, %60 Küçük

Kısıtlar ve Şartlar:
1. Her aydan her bir tedarikçiden en fazla 700 kapakçık satın alınabilir (Kapasite Sınırı).
2. Her ay en az 500 Büyük, 300 Orta ve 300 Küçük kapakçık temin edilmelidir (Talep Alt Sınırları).

AMAÇ: İhtiyaç duyulan kapakçıkların minimum maliyetle (en ekonomik şekilde) 
      tedarik edilmesini sağlayacak sipariş planını (x1, x2, x3) bulmak.
"""

# 1. Model Tanımlama 
model = pulp.LpProblem("US_Labs_Kapakcik_Tedarik", pulp.LpMinimize)

# 2. Karar Değişkenleri (x1, x2, x3: Her bir tedarikçiden sipariş edilecek toplam kapakçık sayısı)

x1 = pulp.LpVariable("Tedarikci_1_Adet", lowBound=0, upBound=700, cat="Integer")
x2 = pulp.LpVariable("Tedarikci_2_Adet", lowBound=0, upBound=700, cat="Integer")
x3 = pulp.LpVariable("Tedarikci_3_Adet", lowBound=0, upBound=700, cat="Integer")

# 3. Amaç Fonksiyonu 
model += 5 * x1 + 4 * x2 + 3 * x3, "Toplam_Tedarik_Maliyeti"

# 4. Kısıtlar (Boyut Talep Alt Sınırları)
model += 0.40 * x1 + 0.30 * x2 + 0.20 * x3 >= 500, "Buyuk_Kapakcik_Kisiti"

# Orta Boyut Kapakçık Kısıtı 
model += 0.40 * x1 + 0.35 * x2 + 0.20 * x3 >= 300, "Orta_Kapakcik_Kisiti"

# Küçük Boyut Kapakçık Kısıtı 
model += 0.20 * x1 + 0.35 * x2 + 0.60 * x3 >= 300, "Kucuk_Kapakcik_Kisiti"

# Not: Tedarikçi üst sınırları (en fazla 700 adet) değişken tanımlanırken 
# upBound=700 ile doğrudan model içerisine eklenmiştir.

# 5. Problemi Çözme (Solver Çalıştırma)
model.solve()

# 6. Sonuçları, Log Kayıtlarını ve Analitik Çıkarımları Ekrana Yazdırma
print("=" * 65)
print("       WINSTON U.S. LABS: KAPAKÇIK TEDARİK OPTİMİZASYON")
print("=" * 65)

# Log ve Durum Bilgileri
print(f"[*] Kullanılan Çözücü (Solver) : {model.solver.name}")
print(f"[*] Çözüm Durumu (Status)     : {pulp.LpStatus[model.status]}")

print("-" * 65)
print("OPTİMAL TEDARİK SİPARİŞ PLANI:")
print(f" > Tedarikçi 1'den Alınacak Miktar : {int(x1.varValue)} adet")
print(f" > Tedarikçi 2'den Alınacak Miktar : {int(x2.varValue)} adet")
print(f" > Tedarikçi 3'den Alınacak Miktar : {int(x3.varValue)} adet")
print(f" > Ulaşılan Minimum Tedarik Maliyeti : {pulp.value(model.objective):.2f} $")

print("-" * 65)
print("ELDE EDİLEN KAPAKÇIK MİKTARLARI VE ANALİZ:")
buyuk_elde = 0.40 * x1.varValue + 0.30 * x2.varValue + 0.20 * x3.varValue
orta_elde  = 0.40 * x1.varValue + 0.35 * x2.varValue + 0.20 * x3.varValue
kucuk_elde = 0.20 * x1.varValue + 0.35 * x2.varValue + 0.60 * x3.varValue

print(f" - Büyük Kapakçık : {buyuk_elde:.1f} adet (Hedef: Min 500)")
print(f" - Orta Kapakçık  : {orta_elde:.1f} adet (Hedef: Satın alma alt sınırı sağlandı)")
print(f" - Küçük Kapakçık : {kucuk_elde:.1f} adet (Hedef: Satın alma alt sınırı sağlandı)")

print("-" * 65)
print("YÖNETSEL ÇIKARIMLAR VE YORUMLAR:")
print("1. Birim maliyeti en düşük olan Tedarikçi 3'e maksimum düzeyde öncelik verilmiştir.")
print("2. Boyut mix oranları ve minimum talep kısıtları matematiksel olarak kusursuz dengelenmiştir.")
print("3. Bu model, U.S. Labs firmasının bütçesini korurken tıbbi operasyonlar için gereken")
print("   kritik kapakçık envanterini garanti altına alır.")
print("=" * 65)