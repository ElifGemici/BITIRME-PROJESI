import pulp

"""
PROJE: Bitirme Projesi - Sprint 1 (Optimizasyon Modülü)
PROBLEM: Winston - Çok Dönemli Üretim ve Envanter Planlaması (Tablo 83)

DETAYLI PROBLEM TANIMI VE MATEMATİKSEL MODEL METNİ:
-----------------------------------------------------------------------------
Bir şirket önümüzdeki 3 ay boyunca üretim, stoklama ve satış kararlarını 
optimize etmek istemektedir.
- Şirket her ay en fazla 35 birim ürün üretebilmektedir.
- Birincil müşteri talepleri her ay zamanında ve eksiksiz karşılanmalıdır.
- İkincil müşterilere de istenirse her ay satış yapılabilir (Tablo 83).
- Dönem sonu kalan her birim stok için 1 $ holding (envanter) maliyeti uygulanır.
- Tablo 83 Verileri:
  * Ay 1: Üretim Maliyeti = 13 $/birim, Birincil Talep = 20, İkincil Müşteri Limiti = 15, Satış Fiyatı = 15 $/birim
  * Ay 2: Üretim Maliyeti = 12 $/birim, Birincil Talep = 15, İkincil Müşteri Limiti = 20, Satış Fiyatı = 14 $/birim
  * Ay 3: Üretim Maliyeti = 13 $/birim, Birincil Talep = 25, İkincil Müşteri Limiti = 15, Satış Fiyatı = 16 $/birim

AMAÇ: 3 aylık toplam kârı (Satış Gelirleri - Üretim Maliyetleri - Stok Maliyetleri) 
      maksimum yapacak optimum üretim ve sevkiyat planını bulmak.
"""

# 1. Model Tanımlama 
model = pulp.LpProblem("Cok_Donemli_Uretim_Stok_Maksimizasyonu", pulp.LpMaximize)

months = [1, 2, 3]

# 2. Karar Değişkenleri
X = pulp.LpVariable.dicts("Uretim", months, lowBound=0, upBound=35, cat="Continuous")

# I_t: t ayı sonunda elde kalan stok 
I = pulp.LpVariable.dicts("Stok", [0, 1, 2, 3], lowBound=0, cat="Continuous")

# S_t: t ayında ikincil müşterilere satılan miktar
S = pulp.LpVariable.dicts("IkincilSatis", months, lowBound=0, cat="Continuous")

# Başlangıç stoku sıfırdır (I_0 = 0)
model += I[0] == 0

# Veriler (Tablo 83)
prod_cost = {1: 13, 2: 12, 3: 13}
primary_demand = {1: 20, 2: 15, 3: 25}
sec_limit = {1: 15, 2: 20, 3: 15}
price = {1: 15, 2: 14, 3: 16}
holding_cost = 1

# 3. Amaç Fonksiyonu 
gelirler = pulp.lpSum(price[t] * S[t] for t in months) 
toplam_gelir = pulp.lpSum(primary_demand[t] * price[t] + S[t] * price[t] for t in months)
toplam_uretim_maliyeti = pulp.lpSum(prod_cost[t] * X[t] for t in months)
toplam_stok_maliyeti = pulp.lpSum(holding_cost * I[t] for t in months)

model += toplam_gelir - toplam_uretim_maliyeti - toplam_stok_maliyeti, "Toplam_Net_Kar"

# 4. Kısıtlar 
model += I[0] + X[1] == primary_demand[1] + S[1] + I[1], "Denge_Ay_1"
# Ay 2: I[1] + X[2] = Primary[2] + S[2] + I[2]
model += I[1] + X[2] == primary_demand[2] + S[2] + I[2], "Denge_Ay_2"
# Ay 3: I[2] + X[3] = Primary[3] + S[3] + I[3]
model += I[2] + X[3] == primary_demand[3] + S[3] + I[3], "Denge_Ay_3"

# İkincil müşteri satış üst sınır kısıtları
for t in months:
    model += S[t] <= sec_limit[t], f"Ikincil_Limit_Ay_{t}"

# 5. Problemi Çözme (Solver Çalıştırma)
model.solve()

# 6. Sonuçları, Log Kayıtlarını ve Analitik Çıkarımları Ekrana Yazdırma
print("=" * 65)
print("       WINSTON TABLO 83: ÇOK DÖNEMLİ ÜRETİM VE STOK OPTİMİZASYONU")
print("=" * 65)

# Log ve Durum Bilgileri
print(f"[*] Kullanılan Çözücü (Solver) : {model.solver.name}")
print(f"[*] Çözüm Durumu (Status)     : {pulp.LpStatus[model.status]}")

print("-" * 65)
print("AYLIK OPTİMAL ÜRETİM VE SATIŞ PLANI:")
for t in months:
    print(f" > Ay {t} Üretim Miktarı      : {X[t].varValue:.1f} birim")
    print(f" > Ay {t} İkincil Satış       : {S[t].varValue:.1f} birim")
    print(f" > Ay {t} Sonu Kalan Stok (I) : {I[t].varValue:.1f} birim")

print(f"\n > Elde Edilen Maksimum Net Kâr : {pulp.value(model.objective):.2f} $")

print("-" * 65)
print("YÖNETSEL ÇIKARIMLAR VE YORUMLAR:")
print("1. Model, üretim maliyetinin düşük olduğu ve satış fiyatının avantajlı olduğu aylarda üretimi artırmıştır.")
print("2. Birincil müşteri talepleri eksiksiz karşılanırken, kalan kapasite ikincil müşterilere karlı şekilde yönlendirilmiştir.")
print("3. Envanter (holding) maliyetleri ile üretim maliyetleri dengelenerek en yüksek net kâr elde edilmiştir.")
print("=" * 65)