import pulp

model = pulp.LpProblem("Candy_Problem", pulp.LpMaximize)

x11 = model.add_variable("x11", lowBound=0)
x12 = model.add_variable("x12", lowBound=0)
x13 = model.add_variable("x13", lowBound=0)

x21 = model.add_variable("x21", lowBound=0)
x22 = model.add_variable("x22", lowBound=0)
x23 = model.add_variable("x23", lowBound=0)

model += 0.20 * (x11 + x12 + x13) + 0.25 * (x21 + x22 + x23)

model += x11 + x21 <= 100
model += x12 + x22 <= 20
model += x13 + x23 <= 30

model += x22 >= 0.20 * (x21 + x22 + x23)

model += x12 >= 0.10 * (x11 + x12 + x13)
model += x13 >= 0.10 * (x11 + x12 + x13)

model.solve()

# ==============================
# OPTİMİZASYON ÇIKTISI
# ==============================

print("\n==============================")
print("CANDY PROBLEM - ÇIKTI ANALİZİ")
print("==============================")

print("\n--- OPTİMAL ÇÖZÜM ---")

gelir = pulp.value(model.objective)

print("Maksimum gelir:", gelir, "$")

print("\n--- DEĞİŞKEN DEĞERLERİ ---")

print("x11 =", x11.value())
print("x12 =", x12.value())
print("x13 =", x13.value())
print("x21 =", x21.value())
print("x22 =", x22.value())
print("x23 =", x23.value())


# ==============================
# ÜRÜN BAZLI ANALİZ
# ==============================

slugger = x11.value() + x12.value() + x13.value()
easy_out = x21.value() + x22.value() + x23.value()

toplam_uretim = slugger + easy_out

print("\n--- ÜRÜN BAZLI ANALİZ ---")

print("Slugger üretimi:", slugger, "oz")
print("Easy Out üretimi:", easy_out, "oz")
print("Toplam üretim:", toplam_uretim, "oz")

print("Slugger geliri:", slugger * 0.20, "$")
print("Easy Out geliri:", easy_out * 0.25, "$")


# ==============================
# KAYNAK KULLANIMI
# ==============================

seker_kullanimi = x11.value() + x21.value()
findik_kullanimi = x12.value() + x22.value()
cikolata_kullanimi = x13.value() + x23.value()

print("\n--- KAYNAK KULLANIMI ---")

print("Şeker kullanımı:", seker_kullanimi, "/ 100 oz")
print("Fındık kullanımı:", findik_kullanimi, "/ 20 oz")
print("Çikolata kullanımı:", cikolata_kullanimi, "/ 30 oz")


# ==============================
# KAYNAK KULLANIM YÜZDESİ
# ==============================

print("\n--- KAYNAK KULLANIM ORANLARI ---")

print("Şeker kullanım oranı:",
      seker_kullanimi / 100 * 100, "%")

print("Fındık kullanım oranı:",
      findik_kullanimi / 20 * 100, "%")

print("Çikolata kullanım oranı:",
      cikolata_kullanimi / 30 * 100, "%")


# ==============================
# ÜRETİM PAYLARI
# ==============================

print("\n--- ÜRETİM PAYLARI ---")

print("Slugger üretim payı:",
      slugger / toplam_uretim * 100, "%")

print("Easy Out üretim payı:",
      easy_out / toplam_uretim * 100, "%")


# ==============================
# YORUM
# ==============================

print("\n--- ÇIKTI YORUMU ---")

print("Optimizasyon sonucunda kaynakların tamamının kullanıldığı görülmektedir.")
print("Slugger ve Easy Out için optimal üretim miktarları belirlenmiştir.")
print("Toplam gelir maksimum seviyeye çıkarılmıştır.")
