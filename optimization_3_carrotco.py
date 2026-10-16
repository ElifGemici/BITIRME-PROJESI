import pulp

model = pulp.LpProblem("Carrotco_Production_Cost", pulp.LpMinimize)


x11 = pulp.LpVariable("Urun1_Makine1", lowBound=0)
x12 = pulp.LpVariable("Urun1_Makine2", lowBound=0)
x21 = pulp.LpVariable("Urun2_Makine1", lowBound=0)
x22 = pulp.LpVariable("Urun2_Makine2", lowBound=0)


model += (
    1.50 * x11
    + 2.20 * x12
    + 0.40 * x21
    + 4.00 * x22
), "Toplam_Uretim_Maliyeti"


model += 0.70 * x11 + 0.75 * x21 <= 200, "Makine1_Kapasitesi"
model += 0.80 * x12 + 0.90 * x22 <= 200, "Makine2_Kapasitesi"


model += (
    0.75 * x11
    + 0.75 * x21
    + 1.20 * x12
    + 1.00 * x22
    <= 400
), "Iscilik_Kapasitesi"


model += x11 + x12 >= 200, "Urun1_Minimum"
model += x21 + x22 >= 240, "Urun2_Minimum"


model += x11 >= 0.5 * (x11 + x12), "Urun1_Makine1_Payi"


model += x22 >= 0.5 * (x21 + x22), "Urun2_Makine2_Payi"


model.solve(pulp.PULP_CBC_CMD(msg=False))


print("CARROTCO OPTİMİZASYON SONUÇLARI")
print("--------------------------------")
print("Çözüm durumu:", pulp.LpStatus[model.status])

if pulp.LpStatus[model.status] == "Optimal":
    print(f"Ürün 1 - Makine 1: {x11.value():.2f} adet")
    print(f"Ürün 1 - Makine 2: {x12.value():.2f} adet")
    print(f"Ürün 2 - Makine 1: {x21.value():.2f} adet")
    print(f"Ürün 2 - Makine 2: {x22.value():.2f} adet")
    print(f"Ürün 1 toplam: {x11.value() + x12.value():.2f} adet")
    print(f"Ürün 2 toplam: {x21.value() + x22.value():.2f} adet")
    print(f"Minimum toplam maliyet: ${pulp.value(model.objective):.2f}")
    # Çıkarımlar
# Modelin sonuçlarına göre birinci üründen toplam 200 birim,
# ikinci üründen ise toplam 240 birim üretilmesi gerektiğini gördük.
# Birinci ürünün 157,14 birimi birinci makinede, 42,86 birimi
# ikinci makinede üretilirken ikinci ürün iki makineye 120'şer
# birim olacak şekilde dağıtıldı.
# Bu üretim planında minimum toplam maliyet 858 dolar olarak
# hesaplandı. Sonuçlar, ürünlerin yalnızca toplam üretim miktarına
# karar vermenin yeterli olmadığını, üretimin makineler arasında
# nasıl dağıtıldığının da maliyet açısından önemli olduğunu gösterdi.
# Makine kapasiteleri, işçilik ve ürünlere ait üretim koşulları
# birlikte değerlendirilerek daha düşük maliyetli bir plan elde edildi.
