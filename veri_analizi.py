import numpy as np
import pandas as pd


def analiz_verisini_hazirla():
    veri = {
        "Ay": [1, 2, 3],
        "Talep": [300, 400, 500],
        "New York Üretimi": [100, 210, 210],
        "Los Angeles Üretimi": [0, 200, 280],
        "Ay Sonu Stoku": [0, 10, 0],
        "Önceki Stok": [200, 0, 10],
    }

    df = pd.DataFrame(veri)

    df["Toplam Üretim"] = (
        df["New York Üretimi"] + df["Los Angeles Üretimi"]
    )
    df["Kullanılabilir Miktar"] = (
        df["Toplam Üretim"] + df["Önceki Stok"]
    )
    df["Talep Karşılama (%)"] = (
        (df["Kullanılabilir Miktar"] - df["Ay Sonu Stoku"])
        / df["Talep"] * 100
    ).round(2)

    df["Üretim Maliyeti ($)"] = (
        df["New York Üretimi"] * 350
        + df["Los Angeles Üretimi"] * 400
    )
    df["Stok Maliyeti ($)"] = df["Ay Sonu Stoku"] * 100
    df["Toplam Maliyet ($)"] = (
        df["Üretim Maliyeti ($)"] + df["Stok Maliyeti ($)"]
    )

    return df


if __name__ == "__main__":
    df = analiz_verisini_hazirla()

    print("\nAIRCO VERİ ANALİZİ")
    print(df.to_string(index=False))
    print("\nGENEL GÖSTERGELER")
    print("Toplam talep:", df["Talep"].sum())
    print("Toplam üretim:", df["Toplam Üretim"].sum())
    print("Toplam üretim maliyeti: $", df["Üretim Maliyeti ($)"].sum())
    print("Toplam stok maliyeti: $", df["Stok Maliyeti ($)"].sum())
    print("Toplam maliyet: $", df["Toplam Maliyet ($)"].sum())