import pulp


model = pulp.LpProblem("Airco_Production_Planning", pulp.LpMinimize)


aylar = [1, 2, 3]

ny = pulp.LpVariable.dicts("New_York", aylar, lowBound=0)
la = pulp.LpVariable.dicts("Los_Angeles", aylar, lowBound=0)

stok = pulp.LpVariable.dicts("Stok", aylar, lowBound=0)

talep = {1: 300, 2: 400, 3: 500}
baslangic_stok = 200


model += pulp.lpSum(
    350 * ny[t] + 400 * la[t] + 100 * stok[t]
    for t in aylar
), "Toplam_Maliyet"


for t in aylar:
    model += 2 * ny[t] <= 420, f"NY_Iscilik_Ay_{t}"
    model += 1.5 * la[t] <= 420, f"LA_Iscilik_Ay_{t}"


for t in aylar:
    onceki_stok = baslangic_stok if t == 1 else stok[t - 1]
    model += (
        onceki_stok + ny[t] + la[t] - talep[t] == stok[t]
    ), f"Stok_Dengesi_Ay_{t}"


model.solve(pulp.PULP_CBC_CMD(msg=False))


print("AIRCO OPTİMİZASYON SONUÇLARI")
print("--------------------------------")
print("Çözüm durumu:", pulp.LpStatus[model.status])

if pulp.LpStatus[model.status] == "Optimal":
    for t in aylar:
        print(f"\nAy {t}:")
        print(f"  New York üretimi: {ny[t].value():.2f}")
        print(f"  Los Angeles üretimi: {la[t].value():.2f}")
        print(f"  Ay sonu stoku: {stok[t].value():.2f}")

    print(f"\nMinimum toplam maliyet: ${pulp.value(model.objective):.2f}")
    # Çıkarımlar
# Modeli çalıştırdığımızda üç aylık üretim planının toplam maliyetini
# 375.000 dolar olarak bulduk. Sonuçlara baktığımızda toplam talebin
# 1.200 birim, toplam üretimin ise 1.000 birim olduğunu gördük.
# İlk ayın başında elimizde bulunan 200 birimlik stok, talebin
# karşılanmasında önemli bir rol oynadı. Böylece üretim miktarı
# toplam talepten düşük olmasına rağmen üç aylık talep karşılandı.
# Ayrıca New York ve Los Angeles tesislerinin üretim miktarlarının
# aylara göre değiştiğini gördük. 