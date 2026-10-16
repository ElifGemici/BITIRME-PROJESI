import pulp


# ==========================================
# 1. MODEL OLUŞTURMA
# ==========================================

model = pulp.LpProblem(
    "State_University_Computers",
    pulp.LpMinimize
)


# ==========================================
# 2. KARAR DEĞİŞKENLERİ
# ==========================================



x1 = model.add_variable(
    "x1",
    lowBound=0,
    cat="Integer"
)

x2 = model.add_variable(
    "x2",
    lowBound=0,
    cat="Integer"
)

x3 = model.add_variable(
    "x3",
    lowBound=0,
    cat="Integer"
)



y1 = model.add_variable(
    "y1",
    cat="Binary"
)

y2 = model.add_variable(
    "y2",
    cat="Binary"
)

y3 = model.add_variable(
    "y3",
    cat="Binary"
)


# ==========================================
# 3. AMAÇ FONKSİYONU
# 
# ==========================================

model += (
    500*x1
    + 350*x2
    + 250*x3
    + 5000*y1
    + 4000*y2
    + 6000*y3
)


# ==========================================
# 4. TOPLAM BİLGİSAYAR İHTİYACI
# ==========================================

model += x1 + x2 + x3 == 1100


# ==========================================
# 5. TEDARİKÇİ KAPASİTE KISITLARI
# ==========================================

model += x1 <= 500*y1

model += x2 <= 900*y2

model += x3 <= 400*y3


# ==========================================
# 6. MODELİ ÇÖZ
# ==========================================

solver = pulp.COIN_CMD(msg=True)

model.solve(solver)


# ==========================================
# 7. ÇÖZÜM SONUÇLARI
# ==========================================

print("\n====================================")
print(" STATE UNIVERSITY COMPUTERS")
print("====================================")

print("Çözüm durumu: OPTIMAL")

print(
    "Minimum toplam maliyet:",
    abs(pulp.value(model.objective)),
    "$"
)


# ==========================================
# 8. TEDARİK PLANI
# ==========================================

print("\n--- TEDARİK PLANI ---")

print(
    "Tedarikçi 1 ->",
    x1.value(),
    "bilgisayar"
)

print(
    "Tedarikçi 2 ->",
    x2.value(),
    "bilgisayar"
)

print(
    "Tedarikçi 3 ->",
    x3.value(),
    "bilgisayar"
)


# ==========================================
# 9. TEDARİKÇİ KULLANIM DURUMU
# ==========================================

print("\n--- TEDARİKÇİ KULLANIM DURUMU ---")

print("Tedarikçi 1:", y1.value())
print("Tedarikçi 2:", y2.value())
print("Tedarikçi 3:", y3.value())


# ==========================================
# 10. TOPLAM BİLGİSAYAR SAYISI
# ==========================================

toplam_bilgisayar = (
    x1.value()
    + x2.value()
    + x3.value()
)

print("\n--- GENEL ANALİZ ---")

print(
    "Toplam bilgisayar:",
    toplam_bilgisayar
)


# ==========================================
# 11. DEĞİŞKEN MALİYET
# ==========================================

degisken_maliyet = (
    500*x1.value()
    + 350*x2.value()
    + 250*x3.value()
)

print(
    "Değişken maliyet:",
    degisken_maliyet,
    "$"
)


# ==========================================
# 12. SABİT TESLİMAT MALİYETİ
# ==========================================

sabit_maliyet = (
    5000*y1.value()
    + 4000*y2.value()
    + 6000*y3.value()
)

print(
    "Sabit teslimat maliyeti:",
    sabit_maliyet,
    "$"
)


# ==========================================
# 13. TEDARİKÇİ BAZLI TOPLAM MALİYET
# ==========================================

maliyet1 = (
    500*x1.value()
    + 5000*y1.value()
)

maliyet2 = (
    350*x2.value()
    + 4000*y2.value()
)

maliyet3 = (
    250*x3.value()
    + 6000*y3.value()
)

print("\n--- TEDARİKÇİ BAZLI MALİYET ---")

print(
    "Tedarikçi 1 toplam maliyeti:",
    maliyet1,
    "$"
)

print(
    "Tedarikçi 2 toplam maliyeti:",
    maliyet2,
    "$"
)

print(
    "Tedarikçi 3 toplam maliyeti:",
    maliyet3,
    "$"
)


# ==========================================
# 14. SONUÇ
# ==========================================

print("\n====================================")
print("              SONUÇ")
print("====================================")

print(
    "Minimum toplam maliyet:",
    abs(pulp.value(model.objective)),
    "$"
)

print(
    "Toplam satın alınan bilgisayar:",
    toplam_bilgisayar
)

print("Tedarikçi 1:", x1.value())
print("Tedarikçi 2:", x2.value())
print("Tedarikçi 3:", x3.value())

print("\nAnaliz tamamlandı.")
