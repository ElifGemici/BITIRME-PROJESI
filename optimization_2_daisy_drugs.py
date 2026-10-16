import pulp


model = pulp.LpProblem(
    "Daisy_Drugs",
    pulp.LpMaximize
)


x1 = pulp.LpVariable("Surec_1_Saat", lowBound=0)
x2 = pulp.LpVariable("Surec_2_Saat", lowBound=0)


kimyasal1_ilac1 = pulp.LpVariable("K1_Ilac1", lowBound=0)
kimyasal2_ilac1 = pulp.LpVariable("K2_Ilac1", lowBound=0)
kimyasal1_ilac2 = pulp.LpVariable("K1_Ilac2", lowBound=0)
kimyasal2_ilac2 = pulp.LpVariable("K2_Ilac2", lowBound=0)


ilac1 = kimyasal1_ilac1 + kimyasal2_ilac1
ilac2 = kimyasal1_ilac2 + kimyasal2_ilac2

# 4. Amaç fonksiyonu satış gelirini maksimize ediyoruz
model += 6 * ilac1 + 4 * ilac2, "Toplam_Satis_Geliri"


model += (
    kimyasal1_ilac1 + kimyasal1_ilac2
    == 3 * x1 + 3 * x2
), "Kimyasal_1_Dengesi"

model += (
    kimyasal2_ilac1 + kimyasal2_ilac2
    == 3 * x1 + x2
), "Kimyasal_2_Dengesi"


model += 3 * x1 + 2 * x2 <= 100, "Hammadde"
model += 2 * x1 + 3 * x2 <= 120, "Isçilik"


model += (
    kimyasal1_ilac1 >= 0.65 * ilac1
), "Ilac_1_Karisim_Orani"

model += (
    kimyasal1_ilac2 >= 0.55 * ilac2
), "Ilac_2_Karisim_Orani"


model.solve(pulp.PULP_CBC_CMD(msg=False))


print("DAISY DRUGS OPTİMİZASYON SONUÇLARI")
print("-----------------------------------")
print("Çözüm durumu:", pulp.LpStatus[model.status])

if pulp.LpStatus[model.status] == "Optimal":
    print(f"1. süreç çalışma süresi: {x1.value():.2f} saat")
    print(f"2. süreç çalışma süresi: {x2.value():.2f} saat")
    print(f"1. ilaç üretimi: {pulp.value(ilac1):.2f} oz")
    print(f"2. ilaç üretimi: {pulp.value(ilac2):.2f} oz")
    print(
        f"Maksimum satış geliri: "
        f"${pulp.value(model.objective):.2f}"
    )
    # Çıkarımlar
# Modelin çözüm sonuçlarını incelediğimizde birinci ilaçtan
# 200 ons üretilirken ikinci ilaçtan üretim yapılmadığını gördük.
# Modelin hesapladığı maksimum gelir 1.200 dolardır.
# Sonuçlar, elimizdeki kaynaklar ve modelde belirtilen kısıtlar
# altında her iki ilacı birden üretmenin zorunlu olmadığını gösterdi.
# Model, gelir hedefini en iyi karşılayan üretim kararını seçti.
# Bu problemden, üretim kararlarının yalnızca ürün miktarlarına
# göre değil, ürünlerin gelirlerine ve üretim sırasında kullanılan
# kaynaklara göre de değerlendirilmesi gerektiğini anladık.
# Böylece sınırlı kaynakların hangi ürüne ayrılacağının toplam
# geliri doğrudan etkileyebileceğini gördük.