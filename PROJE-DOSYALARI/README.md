# Taşıma Ağı Optimizasyonu

## Başlatma (Windows)
1. ZIP dosyasını **Tümünü Ayıkla** ile çıkarın.
2. Açılan `lojistik_optimizer_guncellenmis` klasörüne girin.
3. `Baslat.bat` dosyasına çift tıklayın.
4. İlk çalıştırmada gerekli Python paketleri kurulur. Kurulum için internet bağlantısı gerekir.
5. Streamlit açıldığında tarayıcıda uygulama görüntülenir.

Alternatif olarak bu klasörde terminal açıp:
```bash
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

## Klasör yapısı
- `app.py`: Streamlit arayüzü
- `src/data_utils.py`: Dosya okuma, sütun standardizasyonu, istatistiksel kontroller ve eksik veri yöntemi
- `src/optimization.py`: PuLP taşıma modeli ve duyarlılık analizi
- `src/visuals.py`: Grafikler
- `data/`: Örnek veri ve şablon dosyaları

## Eksik talep verileri
Talep dosyası yüklenirken eksik değerler **otomatik doldurulmaz ve silinmez**. Önce Veri Yönetimi ve İstatistiksel Analiz sayfalarında gösterilir. Kullanıcı İstatistiksel Analiz sayfasında bir yöntem seçtikten sonra yalnızca model için kullanılan ayrı kopya hazırlanır. Yüklenen orijinal veri korunur.

## Dosya biçimleri
CSV ve Excel (`.xlsx`, `.xls`) desteklenir. Sütun adlarında Türkçe karakter/büyük-küçük harf farkları normalize edilir.
