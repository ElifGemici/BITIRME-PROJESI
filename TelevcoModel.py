import pulp


# ==========================================
# 1. MODEL OLUŞTURMA
# ==========================================

model = pulp.LpProblem(
    "Televco_Problem",
    pulp.LpMaximize
)


# ==========================================
# 2. KARAR DEĞİŞKENLERİ
# ==========================================

x11 = model.add_variable("x11", lowBound=0)
x12 = model.add_variable("x12", lowBound=0)
x13 = model.add_variable("x13", lowBound=0)

x21 = model.add_variable("x21", lowBound=0)
x22 = model.add_variable("x22", lowBound=0)
x23 = model.add_variable("x23", lowBound=0)

x31 = model.add_variable("x31", lowBound=0)
x32 = model.add_variable("x32", lowBound=0)
x33 = model.add_variable("x33", lowBound=0)


# ==========================================
# 3. AMAÇ FONKSİYONU
# 
# ==========================================

model += (
    75*x11 + 60*x12 + 69*x13
    + 79*x21 + 73*x22 + 68*x23
    + 85*x31 + 76*x32 + 70*x33
)


# ==========================================
# 4. FABRİKA KAPASİTE KISITLARI
# ==========================================

model += x11 + x12 + x13 <= 50
model += x21 + x22 + x23 <= 100
model += x31 + x32 + x33 <= 50


# ==========================================
# 5. MÜŞTERİ TALEP KISITLARI
# ==========================================

model += x11 + x21 + x31 <= 80
model += x12 + x22 + x32 <= 90
model += x13 + x23 + x33 <= 100


# ==========================================
# 6. MODELİ ÇÖZ
# ==========================================

solver = pulp.COIN_CMD(msg=True)

model.solve(solver)


# ==========================================
# 7. ÇÖZÜM SONUÇLARI
# ==========================================

print("\n====================================")
print("     TELEVCO OPTİMİZASYON SONUCU")
print("====================================")

print("Çözüm durumu: OPTIMAL")

maksimum_kar = abs(pulp.value(model.objective))

print("Maksimum kâr:", maksimum_kar, "$")


# ==========================================
# 8. SEVKİYAT PLANI
# ==========================================

print("\n--- SEVKİYAT PLANI ---")

print("Fabrika 1 -> Müşteri 1:", x11.value(), "tüp")
print("Fabrika 1 -> Müşteri 2:", x12.value(), "tüp")
print("Fabrika 1 -> Müşteri 3:", x13.value(), "tüp")

print("Fabrika 2 -> Müşteri 1:", x21.value(), "tüp")
print("Fabrika 2 -> Müşteri 2:", x22.value(), "tüp")
print("Fabrika 2 -> Müşteri 3:", x23.value(), "tüp")

print("Fabrika 3 -> Müşteri 1:", x31.value(), "tüp")
print("Fabrika 3 -> Müşteri 2:", x32.value(), "tüp")
print("Fabrika 3 -> Müşteri 3:", x33.value(), "tüp")


# ==========================================
# 9. FABRİKA ANALİZİ
# ==========================================

f1 = x11.value() + x12.value() + x13.value()
f2 = x21.value() + x22.value() + x23.value()
f3 = x31.value() + x32.value() + x33.value()

print("\n--- FABRİKA ANALİZİ ---")

print("Fabrika 1 üretimi:", f1, "/ 50 tüp")
print("Fabrika 2 üretimi:", f2, "/ 100 tüp")
print("Fabrika 3 üretimi:", f3, "/ 50 tüp")

print(
    "Fabrika 1 kapasite kullanımı:",
    f1 / 50 * 100,
    "%"
)

print(
    "Fabrika 2 kapasite kullanımı:",
    f2 / 100 * 100,
    "%"
)

print(
    "Fabrika 3 kapasite kullanımı:",
    f3 / 50 * 100,
    "%"
)


# ==========================================
# 10. MÜŞTERİ ANALİZİ
# ==========================================

m1 = x11.value() + x21.value() + x31.value()
m2 = x12.value() + x22.value() + x32.value()
m3 = x13.value() + x23.value() + x33.value()

print("\n--- MÜŞTERİ ANALİZİ ---")

print("Müşteri 1:", m1, "/ 80 tüp")
print("Müşteri 2:", m2, "/ 90 tüp")
print("Müşteri 3:", m3, "/ 100 tüp")


# ==========================================
# 11. KARŞILANMAYAN TALEP
# ==========================================

eksik1 = 80 - m1
eksik2 = 90 - m2
eksik3 = 100 - m3

print("\n--- KARŞILANMAYAN TALEP ---")

print("Müşteri 1:", eksik1, "tüp")
print("Müşteri 2:", eksik2, "tüp")
print("Müşteri 3:", eksik3, "tüp")


# ==========================================
# 12. GENEL ANALİZ
# ==========================================

toplam_uretim = f1 + f2 + f3
toplam_talep = 80 + 90 + 100
toplam_eksik = eksik1 + eksik2 + eksik3

print("\n--- GENEL ANALİZ ---")

print("Toplam üretim:", toplam_uretim, "tüp")
print("Toplam talep:", toplam_talep, "tüp")
print(
    "Toplam karşılanmayan talep:",
    toplam_eksik,
    "tüp"
)

print(
    "Toplam fabrika kapasitesi:",
    200,
    "tüp"
)


# ==========================================
# 13. KAPASİTE KULLANIMI
# ==========================================

toplam_kapasite_kullanimi = (
    toplam_uretim / 200 * 100
)

print(
    "Toplam kapasite kullanım oranı:",
    toplam_kapasite_kullanimi,
    "%"
)


# ==========================================
# 14. SONUÇ VE ÇIKARIMLAR
# ==========================================

print("\n====================================")
print("            ÇIKARIMLAR")
print("====================================")

print(
    "1. Model optimal çözüme ulaşmıştır."
)

print(
    "2. Maksimum kâr:",
    maksimum_kar,
    "$"
)

print(
    "3. Toplam üretim:",
    toplam_uretim,
    "tüp"
)

print(
    "4. Toplam karşılanmayan talep:",
    toplam_eksik,
    "tüp"
)

print(
    "5. Fabrika 1 kapasite kullanımı:",
    f1 / 50 * 100,
    "%"
)

print(
    "6. Fabrika 2 kapasite kullanımı:",
    f2 / 100 * 100,
    "%"
)

print(
    "7. Fabrika 3 kapasite kullanımı:",
    f3 / 50 * 100,
    "%"
)

print(
    "8. Toplam kapasite kullanım oranı:",
    toplam_kapasite_kullanimi,
    "%"
)

print("\nAnaliz tamamlandı.")
