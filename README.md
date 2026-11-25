# PROSPEK · Supply Chain, Vendor Management & Invoice Approval Portal

Prototipe aplikasi Streamlit untuk operasional pengadaan proyek konstruksi dan infrastruktur.
Seluruh data adalah **data contoh (dummy)**; perubahan yang dilakukan (approval, verifikasi,
lock, rekanan baru) tersimpan selama sesi browser dan kembali ke awal saat sesi baru.

## Fitur

| Modul | Isi |
|---|---|
| Sidebar akrostik **P-R-O-S-P-E-K** | Sub-menu bertingkat, badge notifikasi, mode ringkas (huruf saja), sidebar bisa disembunyikan |
| Header | Breadcrumb, pencarian global (tekan `/` atau `Ctrl+K`), Notification Center, profil pengguna |
| Beranda | Banner sapaan, 4 kartu KPI, direktori modul dengan filter kategori, grafik Plotly |
| Partner & Vendor | 5 kartu metrik SAP, filter cepat + 10 filter lanjutan, toggle Locked/Unlocked, aksi massal (Lock, Unlock, Sync SAP, Export), verifikasi 4 stakeholder, Profil 360° (Legalitas, Performa, Audit Log), tambah & import rekanan |
| Payment & Invoice | 6 kartu tahapan, indikator SLA, Bulk Approve, detail tagihan dengan kelengkapan berkas, Visual Approval History, Approve & Lanjutkan Tahap, Return/Tolak dengan catatan wajib, Post Invoice |
| Modul lain | SPB, PO, pengiriman, penerimaan barang, kontrak, adendum, lelang, proses pengadaan, Sertifikasi K3/CQSMS (terhubung ke data rekanan), katalog harga, RUP |
| Asisten PROSPEK | Chatbot berbasis aturan: status/overdue tagihan, rekomendasi rekanan per bidang, sertifikat kedaluwarsa, SOP |
| Ekspor | CSV, Excel (.xlsx) dan PDF yang benar-benar bisa diunduh |

## Struktur folder

```
prospek-streamlit/
├── app.py                  # titik masuk aplikasi
├── requirements.txt
├── .streamlit/config.toml  # tema (warna, font, radius) sesuai DESIGN.md
└── prospek/
    ├── data.py             # data contoh + logika bisnis
    ├── style.py            # CSS sistem desain + komponen HTML
    ├── state.py            # session state & navigasi
    ├── shell.py            # sidebar, header, pencarian, router dialog
    ├── chatbot.py          # logika Asisten PROSPEK
    ├── exports.py          # CSV / Excel / PDF
    └── views/              # halaman: home, vendor, invoice, modules, settings, assistant
```

## Menjalankan di komputer sendiri

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Butuh Python 3.11 atau lebih baru (disarankan 3.12).

## Deploy ke Streamlit Community Cloud

1. Buat repository baru di GitHub, lalu unggah **seluruh isi** folder ini, termasuk folder
   `.streamlit` (di beberapa sistem folder yang diawali titik tersembunyi; pastikan ikut terunggah).
2. Buka https://share.streamlit.io dan masuk dengan akun GitHub.
3. Klik **Create app** → **Deploy a public app from GitHub**.
4. Pilih repository dan branch (`main`), isi **Main file path** dengan `app.py`.
5. Klik **Advanced settings**, pilih **Python 3.12**, lalu **Save**.
6. Klik **Deploy**. Proses instalasi pertama butuh sekitar 2–4 menit.

## Catatan

- Asisten PROSPEK belum memakai model AI; jawabannya dihitung langsung dari data di aplikasi.
- Integrasi ERP/SAP disimulasikan (tombol Sync hanya mengubah status di data contoh).
- Untuk data asli, ganti isi `VR` (rekanan), `IR` (tagihan) dan `GEN` (modul lain) di `prospek/data.py`,
  atau sambungkan ke database.
