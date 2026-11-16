import streamlit as st
import io
import pandas as pd
from pathlib import Path

from src.data_utils import load_and_validate, summarize_data, quality_diagnostics, prepare_demand_for_model
from src.optimization import solve_transport, run_sensitivity, depot_capacity_opportunities
from src.visuals import demand_chart, shipment_heatmap, capacity_chart, sensitivity_chart

st.set_page_config(page_title="Logistics Optimizer", page_icon="🚚", layout="wide")

NAVY = "#142D4E"
st.markdown("""
<style>
/* Uygulama genelinde açık arka plan ve KOYU yazı */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: #F5F7FA !important;
    color: #111827 !important;
}

/* Ana içerikteki bütün metinleri koyu yap: başlık, açıklama, Bölüm A-E vb. */
[data-testid="stMain"] *,
[data-testid="stMain"] *::before,
[data-testid="stMain"] *::after {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Tüm başlıklar */
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] h4,
[data-testid="stMain"] h5,
[data-testid="stMain"] h6 {
    color: #142D4E !important;
    -webkit-text-fill-color: #142D4E !important;
    font-weight: 800 !important;
}

/* Başlık ve açıklama metinleri */
[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] span,
[data-testid="stMain"] small,
[data-testid="stMain"] li,
[data-testid="stMain"] .stCaption {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}

/* Sol menü de açık zemin ve koyu yazı */
section[data-testid="stSidebar"] {
    background: #E8EEF5 !important;
}
section[data-testid="stSidebar"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}

/* Metrik kartları */
div[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #C8D2DF !important;
    border-radius: 12px !important;
}
div[data-testid="stMetric"] *,
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] [data-testid="stMetricLabel"] {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}

/* Bilgi, başarı, uyarı ve hata kutuları */
[data-testid="stAlert"] {
    background: #E8EEF5 !important;
    border: 1px solid #C8D2DF !important;
}
[data-testid="stAlert"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}

/* Dosya yükleme alanları */
[data-testid="stFileUploader"] {
    background: #FFFFFF !important;
    border: 1px solid #C8D2DF !important;
    border-radius: 10px !important;
}
[data-testid="stFileUploader"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}

/* Metin kutuları, seçim alanları ve girişler */
[data-testid="stMain"] input,
[data-testid="stMain"] textarea,
[data-testid="stMain"] [data-baseweb="select"] *,
[data-testid="stMain"] [data-baseweb="input"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    background-color: #FFFFFF !important;
}

/* Butonlar: açık zemin, koyu yazı */
[data-testid="stMain"] div.stButton > button,
section[data-testid="stSidebar"] div.stButton > button {
    background: #E8EEF5 !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 1px solid #AAB8C8 !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}
[data-testid="stMain"] div.stButton > button *,
section[data-testid="stSidebar"] div.stButton > button * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Kod biçimindeki sütun adları */
[data-testid="stMain"] code {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    background: #E8EEF5 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    border: 1px solid #C8D2DF !important;
}

/* Tablolar */
[data-testid="stDataFrame"],
[data-testid="stDataEditor"] {
    color: #111827 !important;
}

/* İndirme ve diğer Streamlit butonları: siyah zemin/beyaz yazı sorununu önle */
[data-testid="stDownloadButton"] button,
.stDownloadButton button,
[data-testid="stFormSubmitButton"] button,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    background: #E8EEF5 !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    border: 1px solid #AAB8C8 !important;
    box-shadow: none !important;
}
[data-testid="stDownloadButton"] button *,
.stDownloadButton button *,
[data-testid="stFormSubmitButton"] button *,
[data-testid="stBaseButton-secondary"] *,
[data-testid="stBaseButton-primary"] * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("LOGISTICS OPTIMIZER")
st.sidebar.caption("Transportation Network Decision Support")
page = st.sidebar.radio(
    "MENÜ",
    ["Genel Bakış", "Veri Yönetimi", "İstatistiksel Analiz",
     "Optimizasyon", "Görselleştirme", "Duyarlılık Analizi", "Raporlama"]
)

st.markdown('<div class="main-title">Taşıma Ağı Optimizasyonu</div>', unsafe_allow_html=True)
st.caption("İstatistiksel parametre tahmini · Maliyet minimizasyonu · Duyarlılık analizi")

# Session defaults
for key in ["demand", "demand_original", "removed_outliers", "demand_model", "demand_processing_note", "costs", "capacity", "cleaning_notes", "solution", "sensitivity"]:
    if key not in st.session_state:
        st.session_state[key] = None

if page == "Genel Bakış":
    st.subheader("Yönetim Paneli")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Depo sayısı", "3")
    c2.metric("Müşteri bölgesi", "5")
    c3.metric("Talep gözlem dönemi", "36 ay")
    c4.metric("Model", "Min. maliyet")
    st.info("Başlamak için Veri Yönetimi sayfasından üç CSV dosyasını yükleyin.")
    st.markdown("#### Proje akışı")
    cols = st.columns(5)
    steps = [("01", "Veri yükleme"), ("02", "İstatistiksel analiz"),
             ("03", "Optimizasyon"), ("04", "Duyarlılık"), ("05", "Raporlama")]
    for col, (n, label) in zip(cols, steps):
        with col:
            st.markdown(f"### {n}")
            st.write(label)
    if st.session_state.solution:
        sol = st.session_state.solution
        st.success(f"Son çözüm durumu: {sol['status']}")

elif page == "Veri Yönetimi":
    st.subheader("Veri Yönetimi")
    st.write("PDF'de tanımlanan üç veri dosyasını yükleyin. Sütun adları otomatik olarak standartlaştırılır; Türkçe karakter, büyük/küçük harf ve boşluk farkları sorun oluşturmaz.")
    st.markdown("""
    - **talep_verisi.csv:** `ay`, `bolge`, `talep_ton`
    - **tasima_maliyeti.csv:** `depo`, `bolge`, `maliyet_tl_ton`
    - **kapasite.csv / kapasite.xlsx:** `depo`, `kapasite_ton` (dosyanızdaki `kapasite_ton_ay` adı da otomatik tanınır)

    CSV ve Excel (`.xlsx`, `.xls`) dosyaları desteklenir. Sağlanan Excel dosyalarındaki tek sütunda virgülle ayrılmış veri biçimi de otomatik ayrıştırılır.
    """)
    a, b, c = st.columns(3)
    with a:
        demand_file = st.file_uploader("Talep verisi", type=["csv", "xlsx", "xls"], key="demand_file")
    with b:
        cost_file = st.file_uploader("Taşıma maliyeti", type=["csv", "xlsx", "xls"], key="cost_file")
    with c:
        capacity_file = st.file_uploader("Depo kapasitesi", type=["csv", "xlsx", "xls"], key="capacity_file")

    if st.button("Verileri yükle ve kontrol et", disabled=not all([demand_file, cost_file, capacity_file])):
        try:
            demand, costs, capacity, notes = load_and_validate(
                demand_file, cost_file, capacity_file
            )

            # Keep the uploaded source intact for traceability.
            demand_original = demand.copy()

            # Remove the two specific anomalous observations identified in the
            # team's earlier analysis: Bursa 4034 ton and Antalya 4563 ton.
            demand_values = pd.to_numeric(demand["talep_ton"], errors="coerce")
            region_values = demand["bolge"].astype(str).str.strip().str.casefold()
            outlier_mask = (
                ((region_values == "bursa") & (demand_values == 4034.0)) |
                ((region_values == "antalya") & (demand_values == 4563.0))
            )
            removed_outliers = demand.loc[outlier_mask].copy()
            demand_clean = demand.loc[~outlier_mask].copy()

            st.session_state.demand_original = demand_original
            st.session_state.removed_outliers = removed_outliers
            st.session_state.demand = demand_clean

            missing_count = int(demand_clean["talep_ton"].isna().sum())
            # The cleaned demand data is used downstream; missing values still
            # follow the explicit handling choice in the Statistical Analysis page.
            st.session_state.demand_model = demand_clean.copy() if missing_count == 0 else None
            st.session_state.demand_processing_note = None
            st.session_state.costs = costs
            st.session_state.capacity = capacity
            st.session_state.cleaning_notes = notes
            st.session_state.solution = None
            st.session_state.sensitivity = None
            st.success(f"Dosyalar yüklendi. Önceki analizde belirlenen {len(removed_outliers)} aykırı gözlem (Bursa 4034 ton, Antalya 4563 ton) temizlenmiş talep verisinden çıkarıldı. Orijinal veri ayrıca korundu.")
        except Exception as e:
            st.error(f"Veri yüklenemedi: {e}")

    if st.session_state.demand is not None:
        st.markdown("#### Yüklenen veri önizlemeleri")
        for title, df in [("Talep", st.session_state.demand),
                          ("Taşıma maliyeti", st.session_state.costs),
                          ("Kapasite", st.session_state.capacity)]:
            with st.expander(title, expanded=True):
                st.dataframe(df, use_container_width=True)
        if st.session_state.removed_outliers is not None and not st.session_state.removed_outliers.empty:
            st.markdown("#### Önceki analizde belirlenen ve çıkarılan aykırı gözlemler")
            st.dataframe(st.session_state.removed_outliers, use_container_width=True)
            st.caption("Bu kayıtlar temizlenmiş talep verisinden çıkarılmıştır. Yüklenen orijinal veri ayrıca korunur.")

        st.markdown("#### Veri kontrol notları")
        for note in st.session_state.cleaning_notes:
            st.write("• " + note)
        missing_rows = st.session_state.demand[st.session_state.demand["talep_ton"].isna()]
        if not missing_rows.empty:
            st.warning(f"{len(missing_rows)} eksik talep gözlemi bulundu. Bu kayıtlar silinmedi veya doldurulmadı; kararınızı İstatistiksel Analiz sayfasında verebilirsiniz.")
            st.dataframe(missing_rows, use_container_width=True)

elif page == "İstatistiksel Analiz":
    st.subheader("Bölüm A — Veri hazırlama ve istatistiksel analiz")
    if st.session_state.demand is None:
        st.warning("Önce Veri Yönetimi sayfasından CSV dosyalarını yükleyin.")
    else:
        d = st.session_state.demand
        st.markdown("#### Temizlenmiş talep verisi genel görünümü")
        left, right = st.columns(2)
        with left:
            st.dataframe(d.describe(include="all"), use_container_width=True)
        with right:
            st.write("Eksik değer sayıları")
            st.dataframe(d.isna().sum().rename("Eksik değer").to_frame())
        missing_rows = d[d["talep_ton"].isna()]
        if not missing_rows.empty:
            st.markdown("#### Eksik talep gözlemleri — karar verilmeden önce inceleyin")
            st.dataframe(missing_rows, use_container_width=True)
            st.info("Eksik talep değerleri bilinmeyen değerlerdir; sıfır kabul edilmez. Otomatik doldurma veya silme yapılmadı.")
            method = st.radio(
                "İstatistiksel incelemeden sonra eksik değerleri nasıl ele almak istersiniz?",
                ["Henüz karar verilmedi", "Eksik gözlemleri çıkar", "Bölge medyanıyla doldur"],
                index=0,
                help="Seçim, optimizasyon için kullanılacak ayrı bir veri kopyasına uygulanır. Orijinal yüklenen veri korunur."
            )
            if st.button("Seçilen veri işleme yöntemini uygula", disabled=(method == "Henüz karar verilmedi")):
                try:
                    processed, note = prepare_demand_for_model(d, method)
                    st.session_state.demand_model = processed
                    st.session_state.demand_processing_note = note
                    st.session_state.solution = None
                    st.session_state.sensitivity = None
                    st.success(note + " Orijinal veri değiştirilmedi.")
                except Exception as e:
                    st.error(str(e))
        else:
            st.success("Eksik talep gözlemi yok. Orijinal talep verisi doğrudan kullanılabilir.")
        if st.session_state.demand_processing_note:
            st.caption("Optimizasyon için seçilen yöntem: " + st.session_state.demand_processing_note)
        # Tanımlayıcı istatistikler ve kalite testleri, eksik değerler için
        # kullanıcı tarafından uygulanmış yöntemin çıktısı üzerinden hesaplanır.
        # İlk veri özeti ve eksik gözlem listesi ise orijinal/temizlenmiş kaynak
        # veri olan d üzerinden gösterilmeye devam eder.
        analysis_demand = (
            st.session_state.demand_model.copy()
            if st.session_state.demand_model is not None
            else d.copy()
        )

        if st.session_state.demand_model is not None:
            st.info(
                "Aşağıdaki bölgesel istatistikler, güven aralıkları ve kalite "
                "testleri seçilip uygulanmış veri işleme yöntemine göre "
                "hesaplanmıştır."
            )
        elif d["talep_ton"].isna().any():
            st.warning(
                "Henüz eksik veri işleme yöntemi uygulanmadı. Aşağıdaki "
                "istatistikler mevcut eksik değerli veri üzerinden hesaplanır; "
                "eksik talep içeren satırlar bölgesel sayısal özetlere dahil edilmez."
            )

        stats, ci = summarize_data(analysis_demand)
        st.markdown("#### Bölge bazında tanımlayıcı istatistikler")
        st.dataframe(stats, use_container_width=True)
        st.markdown("#### Ortalama talep için %95 güven aralığı")
        st.dataframe(ci, use_container_width=True)
        st.caption(
            "Güven aralığı, seçilen veri işleme yönteminden sonra bölge bazında "
            "kalan aylık talep gözlemleri için t dağılımı kullanılarak hesaplanır."
        )
        outliers, normality = quality_diagnostics(analysis_demand)
        st.markdown("#### İşlenmiş veri üzerinde aykırı gözlem kontrolü (IQR yöntemi)")
        st.dataframe(outliers, use_container_width=True)
        st.caption(
            "Önceki analizde belirlenen Bursa 4034 ton ve Antalya 4563 ton "
            "kayıtları analizden önce çıkarılmıştır. Bu tablo, seçilen eksik "
            "veri işleme yönteminden sonra kalan veride IQR sınırları dışında "
            "kalan diğer gözlemleri gösterir; bunlar otomatik silinmez."
        )
        st.markdown("#### Normal dağılım değerlendirmesi (Shapiro-Wilk)")
        st.dataframe(normality, use_container_width=True)
        st.caption("H0: Veriler normal dağılımdan gelmektedir. p < 0.05 ise H0 reddedilir.")
        st.markdown("#### Ortalama güzergâh maliyeti matrisi")
        matrix = st.session_state.costs.pivot_table(index="depo", columns="bolge",
                                                     values="maliyet_tl_ton", aggfunc="mean")
        st.dataframe(matrix, use_container_width=True)

elif page == "Optimizasyon":
    st.subheader("Bölüm B — Taşıma modeli")
    if any(st.session_state[k] is None for k in ["demand", "costs", "capacity"]):
        st.warning("Optimizasyon için önce üç veri dosyasını yükleyin.")
    elif st.session_state.demand_model is None:
        st.warning("Talep verisinde eksik gözlemler var. Önce İstatistiksel Analiz sayfasında eksik verileri inceleyip bir işleme yöntemi seçin.")
    else:
        st.write("Model, her bölgenin ortalama aylık talebini karşılayacak şekilde toplam taşıma maliyetini minimize eder.")
        if st.session_state.demand_processing_note:
            st.caption("Kullanılan talep verisi: " + st.session_state.demand_processing_note)
        if st.button("Optimizasyonu çalıştır"):
            result = solve_transport(st.session_state.demand_model, st.session_state.costs, st.session_state.capacity)
            st.session_state.solution = result
        if st.session_state.solution:
            sol = st.session_state.solution
            st.metric("Çözüm durumu", sol["status"])
            if sol["status"] == "Optimal":
                st.metric("Minimum toplam maliyet", f"{sol['objective']:,.2f} TL")
                st.markdown("#### Sevkiyat planı (ton/ay)")
                st.dataframe(sol["shipments"].round(3), use_container_width=True)
                st.markdown("#### Depo kapasite kullanımı")
                st.dataframe(sol["capacity_usage"].round(3), use_container_width=True)
            else:
                st.error("Model uygulanabilir bir çözüm bulamadı. Toplam kapasite ve toplam talebi kontrol edin.")

elif page == "Görselleştirme":
    st.subheader("Bölüm C — Görselleştirme")
    if st.session_state.demand is None:
        st.warning("Grafikler için önce veri yükleyin.")
    elif st.session_state.demand_model is None:
        st.warning("Talep verisindeki eksik değerler için önce İstatistiksel Analiz sayfasında karar verin.")
    else:
        stats, ci = summarize_data(st.session_state.demand_model)
        st.plotly_chart(demand_chart(stats, ci), use_container_width=True)
        if st.session_state.solution and st.session_state.solution["status"] == "Optimal":
            st.plotly_chart(shipment_heatmap(st.session_state.solution["shipments"]), use_container_width=True)
            st.plotly_chart(capacity_chart(st.session_state.solution["capacity_usage"]), use_container_width=True)
        else:
            st.info("Sevkiyat ve kapasite grafiklerini görmek için önce optimizasyonu çalıştırın.")

elif page == "Duyarlılık Analizi":
    st.subheader("Bölüm D — Duyarlılık analizi")
    if any(st.session_state[k] is None for k in ["demand", "costs", "capacity"]):
        st.warning("Duyarlılık analizi için önce üç veri dosyasını yükleyin.")
    elif st.session_state.demand_model is None:
        st.warning("Talep verisindeki eksik değerler için önce İstatistiksel Analiz sayfasında karar verin.")
    else:
        st.write("Altı senaryo, aynı çözüm fonksiyonu kullanılarak yeniden çözülür.")
        if st.button("Altı senaryoyu çalıştır"):
            st.session_state.sensitivity = run_sensitivity(
                st.session_state.demand_model, st.session_state.costs, st.session_state.capacity
            )
        if st.session_state.sensitivity is not None:
            st.dataframe(st.session_state.sensitivity, use_container_width=True)
            st.plotly_chart(sensitivity_chart(st.session_state.sensitivity), use_container_width=True)
            st.caption("Maliyet değişimi baz senaryoya göre TL ve yüzde olarak raporlanır. Çözümsüz senaryolar ayrıca işaretlenir.")
        st.markdown("#### Depo bazında kapasite artırımı karşılaştırması")
        increase = st.select_slider("Her seferinde tek bir deponun kapasitesini artır", options=[0.05, 0.10], value=0.10,
                                    format_func=lambda x: f"%{int(x*100)}")
        if st.button("Depo alternatiflerini karşılaştır"):
            # Kapasite sütunu tam sayıysa, yüzde artışında float değer ataması
            # pandas kaynaklı int64 dönüştürme hatası verebilir.
            capacity_for_scenario = st.session_state.capacity.copy()
            capacity_for_scenario["kapasite_ton"] = pd.to_numeric(
                capacity_for_scenario["kapasite_ton"], errors="raise"
            ).astype(float)

            opportunities = depot_capacity_opportunities(
                st.session_state.demand_model, st.session_state.costs,
                capacity_for_scenario, increase
            )
            st.session_state.depot_opportunities = opportunities
        if st.session_state.get("depot_opportunities") is not None:
            st.dataframe(st.session_state.depot_opportunities, use_container_width=True)
            st.caption("En yüksek pozitif tasarrufu sağlayan depo, kapasite yatırımının maliyet etkisi açısından öncelikli adaydır. Sonuçlar model varsayımları altında yorumlanmalıdır.")

elif page == "Raporlama":
    st.subheader("Bölüm E — Raporlama")
    st.write(
        "Optimizasyon sonuçlarını Excel çalışma kitabı olarak dışa aktarabilirsiniz. "
        "Sayısal hücreler gerçek sayısal değer olarak kaydedilir; küsuratlar korunur."
    )
    if st.session_state.solution and st.session_state.solution["status"] == "Optimal":
        sol = st.session_state.solution
        st.markdown("#### Optimizasyon özeti")
        st.write(f"Çözüm durumu: **{sol['status']}**")
        st.write(f"Minimum toplam maliyet: **{sol['objective']:,.2f} TL**")

        # CSV yerine XLSX üret: Excel sayısal hücreleri metin olarak değil,
        # gerçek sayı olarak saklar. Böylece ondalık basamaklar korunur.
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
            sol["shipments"].to_excel(writer, sheet_name="Sevkiyat Planı")
            if sol.get("capacity_usage") is not None:
                sol["capacity_usage"].to_excel(writer, sheet_name="Kapasite Kullanımı")
            if st.session_state.demand_model is not None:
                demand_stats, demand_ci = summarize_data(st.session_state.demand_model)
                demand_stats.to_excel(writer, sheet_name="Bölgesel İstatistikler", index=False)
                demand_ci.to_excel(writer, sheet_name="Güven Aralıkları", index=False)
            if st.session_state.sensitivity is not None:
                st.session_state.sensitivity.to_excel(
                    writer, sheet_name="Duyarlılık Analizi", index=False
                )

            # Tüm sayfalardaki sayısal hücrelerde dört ondalık basamak göster.
            for worksheet in writer.book.worksheets:
                worksheet.freeze_panes = "A2"
                worksheet.auto_filter.ref = worksheet.dimensions
                for column_cells in worksheet.columns:
                    max_length = max(
                        (len(str(cell.value)) for cell in column_cells if cell.value is not None),
                        default=10,
                    )
                    worksheet.column_dimensions[column_cells[0].column_letter].width = min(
                        max(max_length + 2, 12), 28
                    )
                    for cell in column_cells:
                        if isinstance(cell.value, (int, float)) and not isinstance(cell.value, bool):
                            cell.number_format = "#,##0.0000"

        excel_buffer.seek(0)
        st.download_button(
            "Raporu indir (Excel)",
            data=excel_buffer.getvalue(),
            file_name="lojistik_optimizasyon_raporu.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.caption(
            "Dosyada sevkiyat planı ve kapasite kullanımı; mevcutsa bölgesel "
            "istatistikler, %95 güven aralıkları ve duyarlılık analizi ayrı sayfalarda bulunur."
        )
    else:
        st.info("Rapor oluşturmak için veri yükleyip optimizasyonu çalıştırın.")
