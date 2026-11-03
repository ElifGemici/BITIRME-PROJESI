import pandas as pd
from pathlib import Path
from scipy import stats
import numpy as np
import pulp
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


dosya_yolu = (
    Path.home()
    / "Desktop"
    / "veri"
    / "talep_verisi.csv"
)

talep = pd.read_csv(dosya_yolu)

# 1. Veri setinin boyutu
print("\nVeri setinin boyutu:")
print(talep.shape)

# 2. Sütun bilgileri ve veri türleri
print("\nVeri bilgileri:")
talep.info()

# 3. İstatistiksel özet
print("\nİstatistiksel özet:")
print(talep.describe())

# 4. Eksik değer sayıları
print("\nEksik değerler:")
print(talep.isnull().sum())

# 5. Her bölgedeki kayıt sayısı
print("\nBölgelere göre kayıt sayısı:")
print(talep["bolge"].value_counts())

# Eksik değerlerin bulunduğu kayıtlar
print("\nEksik değer bulunan kayıtlar:")
print(talep[talep["talep_ton"].isnull()])

# En yüksek 10 talep değeri
print("\nEn yüksek 10 talep:")
print(talep.nlargest(10, "talep_ton"))

# 6. Eksik değerleri bölge ve aya göre incele
print("\nEksik değer bulunan kayıtlar:")
print(talep[talep["talep_ton"].isna()])

# 7. Bölgelere göre talep özeti
print("\nBölgelere göre talep özeti:")
print(talep.groupby("bolge")["talep_ton"].agg(
    ["count", "mean", "median", "min", "max"]
).round(2))

# 8. Aşırı yüksek talepleri kontrol et
print("\n500 ton üzerindeki talepler:")
print(talep[talep["talep_ton"] > 500])

# 6. IQR yöntemiyle aykırı değer analizi
Q1 = talep["talep_ton"].quantile(0.25)
Q3 = talep["talep_ton"].quantile(0.75)
IQR = Q3 - Q1
alt_sinir = Q1 - 1.5 * IQR
ust_sinir = Q3 + 1.5 * IQR
aykiri_degerler = talep[
    (talep["talep_ton"] < alt_sinir) |
    (talep["talep_ton"] > ust_sinir)
]
print("\nIQR yöntemiyle aykırı değer analizi:")
print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Alt sınır:", alt_sinir)
print("Üst sınır:", ust_sinir)
print("\nAykırı değer bulunan kayıtlar:")
print(aykiri_degerler)

# Aykırı değerleri veri setinden çıkarma

aykiri_degerler = (
    (talep["bolge"] == "Bursa") & (talep["talep_ton"] == 4034.0)
) | (
    (talep["bolge"] == "Antalya") & (talep["talep_ton"] == 4563.0)
)

talep_temiz = talep[~aykiri_degerler].copy()

print("\nAykırı değerler çıkarıldıktan sonra kalan kayıt sayısı:")
print(len(talep_temiz))



# Eksik talep değerlerini çıkar
talep_temiz = talep_temiz.dropna(subset=["talep_ton"])

# A3 - Aykırı değerler çıkarıldıktan sonra istatistiksel özet

ozet_temiz = talep_temiz.groupby("bolge")["talep_ton"].agg(
    ["mean", "std", "min", "max"]
)

ozet_temiz.columns = [
    "Ortalama",
    "Standart Sapma",
    "Minimum",
    "Maksimum"
]

print("\nA3 - Temizlenmiş Veriye Göre İstatistiksel Özet:")
print(ozet_temiz.round(2))

# A4 - Aykırı değerler çıkarıldıktan sonra %95 güven aralığı

print("\nA4 - Temizlenmiş Veriye Göre %95 Güven Aralıkları:")

for bolge, grup in talep_temiz.groupby("bolge"):
    veri = grup["talep_ton"].dropna()

    n = len(veri)
    ortalama = veri.mean()
    standart_sapma = veri.std()

    hata_payi = stats.t.ppf(0.975, df=n - 1) * (
        standart_sapma / np.sqrt(n)
    )

    alt_guven = ortalama - hata_payi
    ust_guven = ortalama + hata_payi

    print(
        f"{bolge}: Ortalama = {ortalama:.2f}, "
        f"%95 Güven Aralığı = ({alt_guven:.2f}, {ust_guven:.2f})"
    )

    # A5 - Shapiro-Wilk Normallik Testi

print("\nA5 - Shapiro-Wilk Normallik Testi:")

for bolge, grup in talep_temiz.groupby("bolge"):
    veri = grup["talep_ton"].dropna()

    W, p_degeri = stats.shapiro(veri)

    print(
        f"{bolge}: W = {W:.4f}, "
        f"p-değeri = {p_degeri:.4f}"
    )

    if p_degeri > 0.05:
        print("Sonuç: Normal dağılımdan anlamlı bir sapma bulunamadı.")
    else:
        print("Sonuç: Normal dağılım varsayımı reddedildi.")

        # A6 - Güzergah Başına Ortalama Taşıma Maliyeti

maliyet_dosya_yolu = (
    Path.home()
    / "Desktop"
    / "veri"
    / "tasima_maliyeti.csv"
)

maliyet = pd.read_csv(maliyet_dosya_yolu)

# Her depo-bölge güzergahı için ortalama maliyet
ortalama_maliyet = maliyet.pivot_table(
    index="depo",
    columns="bolge",
    values="maliyet_tl_ton",
    aggfunc="mean"
)

# 3x5 maliyet matrisini oluştur
bolge_sirasi = [
    "Bursa",
    "Konya",
    "Antalya",
    "Samsun",
    "Gaziantep"
]

depo_sirasi = [
    "Istanbul",
    "Ankara",
    "Izmir"
]

maliyet_matrisi = ortalama_maliyet.reindex(
    index=depo_sirasi,
    columns=bolge_sirasi
)

print("\nA6 - Ortalama Taşıma Maliyeti Matrisi (TL/ton):")
print(maliyet_matrisi.round(2))

# A7 - Optimizasyon Modeli Parametrelerinin Belirlenmesi

# Bölge başına aylık ortalama talep (d_j)
talep_parametresi = (
    talep_temiz.groupby("bolge")["talep_ton"]
    .mean()
    .reindex(bolge_sirasi)
)

# Güzergah başına ortalama birim maliyet (c_ij)
maliyet_parametresi = maliyet_matrisi.copy()

print("\nA7 - Model Parametreleri")

print("\nBölge Başına Aylık Ortalama Talep (d_j) - ton:")
print(talep_parametresi.round(2))

print("\nGüzergah Başına Ortalama Birim Maliyet (c_ij) - TL/ton:")
print(maliyet_parametresi.round(2))


# B - Optimizasyon Modeli

# Kapasite verilerini oku
kapasite_dosya_yolu = (
    Path.home() / "Desktop" / "veri" / "kapasite.csv"
)

kapasite_verisi = pd.read_csv(kapasite_dosya_yolu)

# Depo kapasitelerini sözlük olarak hazırla
kapasiteler = kapasite_verisi.set_index(
    "depo"
)["kapasite_ton_ay"].to_dict()

# Talep parametreleri: d_j
talepler = talep_temiz.groupby("bolge")[
    "talep_ton"
].mean().to_dict()

# Maliyet parametreleri: c_ij
maliyetler = maliyet_matrisi.to_dict()

depolar = list(kapasiteler.keys())
bolgeler = list(talepler.keys())

# Optimizasyon modelini oluştur
model = pulp.LpProblem(
    "Tasima_Maliyeti_Minimizasyonu",
    pulp.LpMinimize
)

# Karar değişkenleri: x_ij
x = pulp.LpVariable.dicts(
    "Tasima",
    [(i, j) for i in depolar for j in bolgeler],
    lowBound=0,
    cat="Continuous"
)

# Amaç fonksiyonu: toplam taşıma maliyetini minimize et
model += pulp.lpSum(
    maliyetler[j][i] * x[(i, j)]
    for i in depolar
    for j in bolgeler
)

# Kapasite kısıtları
for i in depolar:
    model += (
        pulp.lpSum(x[(i, j)] for j in bolgeler)
        <= kapasiteler[i],
        f"Kapasite_{i}"
    )

# Talep kısıtları
for j in bolgeler:
    model += (
        pulp.lpSum(x[(i, j)] for i in depolar)
        >= talepler[j],
        f"Talep_{j}"
    )

# Modeli çöz
model.solve(pulp.PULP_CBC_CMD(msg=False))

print("\nB1-B2 - Optimizasyon Sonuçları")
print("Çözüm durumu:", pulp.LpStatus[model.status])

if pulp.LpStatus[model.status] == "Optimal":
    print(
        "Minimum toplam taşıma maliyeti:",
        round(pulp.value(model.objective), 2),
        "TL"
    )

    # Sevkiyat tablosu
    sevkiyat = pd.DataFrame(
        0.0,
        index=depolar,
        columns=bolgeler
    )

    for i in depolar:
        for j in bolgeler:
            sevkiyat.loc[i, j] = pulp.value(x[(i, j)])

    print("\nSevkiyat Planı (ton):")
    print(sevkiyat.round(2))

    # Depo kapasite kullanımı
    print("\nDepo Kapasite Kullanımı:")
    for i in depolar:
        kullanilan = sevkiyat.loc[i].sum()
        kapasite = kapasiteler[i]

        print(
            f"{i}: {kullanilan:.2f} / {kapasite:.2f} ton "
            f"(%{kullanilan / kapasite * 100:.2f})"
        ) 

        
        # C1 - Bölgelere Göre Ortalama Talep ve %95 Güven Aralıkları

bolge_ozet = []

for bolge, grup in talep_temiz.groupby("bolge"):
    veri = grup["talep_ton"].dropna()

    n = len(veri)
    ortalama = veri.mean()
    standart_sapma = veri.std()

    hata_payi = stats.t.ppf(0.975, df=n - 1) * (
        standart_sapma / np.sqrt(n)
    )

    bolge_ozet.append({
        "Bolge": bolge,
        "Ortalama": ortalama,
        "Alt": ortalama - hata_payi,
        "Ust": ortalama + hata_payi
    })

grafik_verisi = pd.DataFrame(bolge_ozet)

hata_alt = (
    grafik_verisi["Ortalama"] - grafik_verisi["Alt"]
)
hata_ust = (
    grafik_verisi["Ust"] - grafik_verisi["Ortalama"]
)

plt.figure(figsize=(9, 5))

plt.errorbar(
    grafik_verisi["Bolge"],
    grafik_verisi["Ortalama"],
    yerr=[hata_alt, hata_ust],
    fmt="o",
    capsize=5
)

plt.title("Bölgelere Göre Ortalama Talep ve %95 Güven Aralıkları")
plt.xlabel("Bölge")
plt.ylabel("Ortalama Talep (ton)")
plt.tight_layout()
plt.savefig("C1_ortalama_talep_guven_araligi.png", dpi=300)
plt.show()

# C2 - Sevkiyat Planı Isı Haritası

plt.figure(figsize=(9, 5))

plt.imshow(sevkiyat.values, aspect="auto")

plt.xticks(
    range(len(sevkiyat.columns)),
    sevkiyat.columns,
    rotation=0
)

plt.yticks(
    range(len(sevkiyat.index)),
    sevkiyat.index
)

plt.colorbar(label="Taşınan Miktar (ton)")

plt.title("Depolardan Bölgelere Sevkiyat Planı")
plt.xlabel("Bölge")
plt.ylabel("Depo")

# Hücrelerin içine sevkiyat miktarlarını yaz
for i in range(len(sevkiyat.index)):
    for j in range(len(sevkiyat.columns)):
        plt.text(
            j,
            i,
            f"{sevkiyat.iloc[i, j]:.1f}",
            ha="center",
            va="center"
        )

plt.tight_layout()
plt.savefig("C2_sevkiyat_isi_haritasi.png", dpi=300)
plt.show()

# C3 - Depo Kapasitesi ve Kullanım Oranı

kullanilan_kapasiteler = sevkiyat.sum(axis=1)
toplam_kapasiteler = pd.Series(kapasiteler).reindex(sevkiyat.index)

bos_kapasiteler = toplam_kapasiteler - kullanilan_kapasiteler

plt.figure(figsize=(9, 5))

plt.bar(
    sevkiyat.index,
    kullanilan_kapasiteler,
    label="Kullanılan Kapasite"
)

plt.bar(
    sevkiyat.index,
    bos_kapasiteler,
    bottom=kullanilan_kapasiteler,
    label="Boş Kapasite"
)

plt.title("Depo Kapasitesi ve Kullanım Oranı")
plt.xlabel("Depo")
plt.ylabel("Kapasite (ton)")
plt.legend()

# Her deponun kullanım oranını göster
for i, depo in enumerate(sevkiyat.index):
    oran = (
        kullanilan_kapasiteler[depo]
        / toplam_kapasiteler[depo]
        * 100
    )

    plt.text(
        i,
        toplam_kapasiteler[depo] + 10,
        f"%{oran:.1f}",
        ha="center"
    )

plt.tight_layout()
plt.savefig("C3_depo_kapasite_kullanimi.png", dpi=300)
plt.show()

# D - Duyarlılık Analizi

def coz(kapasite_carpani=1.0, talep_carpani=1.0):
    # Senaryoya göre kapasite ve talepleri güncelle
    yeni_kapasiteler = {
        i: kapasiteler[i] * kapasite_carpani
        for i in depolar
    }

    yeni_talepler = {
        j: talepler[j] * talep_carpani
        for j in bolgeler
    }

    # Yeni optimizasyon modeli
    senaryo_modeli = pulp.LpProblem(
        "Duyarlilik_Analizi",
        pulp.LpMinimize
    )

    # Karar değişkenleri
    karar = pulp.LpVariable.dicts(
        "Gonderim",
        [(i, j) for i in depolar for j in bolgeler],
        lowBound=0,
        cat="Continuous"
    )

    # Amaç fonksiyonu
    senaryo_modeli += pulp.lpSum(
        maliyetler[j][i] * karar[(i, j)]
        for i in depolar
        for j in bolgeler
    )

    # Kapasite kısıtları
    for i in depolar:
        senaryo_modeli += (
            pulp.lpSum(karar[(i, j)] for j in bolgeler)
            <= yeni_kapasiteler[i]
        )

    # Talep kısıtları
    for j in bolgeler:
        senaryo_modeli += (
            pulp.lpSum(karar[(i, j)] for i in depolar)
            >= yeni_talepler[j]
        )

    # Çöz
    senaryo_modeli.solve(pulp.PULP_CBC_CMD(msg=False))

    durum = pulp.LpStatus[senaryo_modeli.status]

    if durum == "Optimal":
        maliyet = pulp.value(senaryo_modeli.objective)
    else:
        maliyet = None

    return durum, maliyet



    # Baz senaryo
baz_durum, baz_maliyet = coz(1.0, 1.0)

senaryolar = [
    ("Baz senaryo", 1.0, 1.0),
    ("Kapasiteler %10 azalır", 0.90, 1.0),
    ("Kapasiteler %10 artar", 1.10, 1.0),
    ("Talepler %5 azalır", 1.0, 0.95),
    ("Talepler %5 artar", 1.0, 1.05),
    ("Kapasite %10 azalır, talep %5 artar", 0.90, 1.05)
]

sonuclar = []

for ad, kapasite_carpani, talep_carpani in senaryolar:
    durum, maliyet = coz(kapasite_carpani, talep_carpani)

    if maliyet is not None and baz_maliyet is not None:
        fark_tl = maliyet - baz_maliyet
        fark_yuzde = fark_tl / baz_maliyet * 100
    else:
        fark_tl = None
        fark_yuzde = None

    sonuclar.append({
        "Senaryo": ad,
        "Çözüm Durumu": durum,
        "Toplam Maliyet (TL)": maliyet,
        "Değişim (TL)": fark_tl,
        "Değişim (%)": fark_yuzde
    })

sonuc_tablosu = pd.DataFrame(sonuclar)

print("\nD - DUYARLILIK ANALİZİ")
print(sonuc_tablosu.round(2).to_string(index=False))

# D - Senaryo sonuçlarını görselleştir

grafik_sonuclari = sonuc_tablosu.dropna(
    subset=["Toplam Maliyet (TL)"]
)

plt.figure(figsize=(11, 6))

plt.bar(
    grafik_sonuclari["Senaryo"],
    grafik_sonuclari["Toplam Maliyet (TL)"]
)

plt.title("Duyarlılık Analizi: Senaryolara Göre Toplam Taşıma Maliyeti")
plt.xlabel("Senaryo")
plt.ylabel("Toplam Taşıma Maliyeti (TL)")
plt.gca().yaxis.set_major_formatter(
    ticker.FuncFormatter(lambda x, pos: f"{x:,.0f}".replace(",", "."))
)
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("D_duyarlilik_analizi.png", dpi=300)
plt.show()