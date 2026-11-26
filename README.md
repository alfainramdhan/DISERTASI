# HAIDAR AI

**H**ub for **A**rtificial **I**ntelligence, **D**igital **A**cquisition & **R**esource Management.
Portal Supply Chain & Vendor dengan menu AI DECISION (50 kriteria, termasuk Green Supply Chain Management).
Tampilan dan fitur sama dengan prototipe artifact; Streamlit dipakai sebagai wadah untuk deploy.

## Menu sidebar (akrostik H-A-I-D-A-R)
| Huruf | Menu | Isi |
|---|---|---|
| AI | AI DECISION (BARU) | Ringkasan, ranking, performa 50 kriteria, bandingkan, indeks hijau, bobot, risiko, model |
| H | Hub & Vendor Management | Verifikasi 4 stakeholder, Profil 360, scorecard performa, sinkronisasi SAP |
| A | Acquisition & E-Procurement | Info lelang, proses pengadaan, sertifikasi K3/CQSMS (dengan badge notifikasi) |
| I | Invoice & Payment System | Pipeline approval 6 tahap, SLA aging, riwayat approver |
| D | Digital & Smart Contract | Kontrak aktif, masa berlaku dan adendum |
| A | Asset & Operational Logistics | Pengiriman dan penerimaan material |
| R | Requisition, Purchasing & Catalog | SPB, PO, Katalog Harga Satuan, RUP |

## Isi project
```
app.py              pembungkus Streamlit
haidar.html         seluruh antarmuka dan data contoh
requirements.txt    hanya streamlit
.streamlit/config.toml
```

## Jalankan di komputer
```
pip install -r requirements.txt
streamlit run app.py
```

## Deploy ke Streamlit Community Cloud
1. Unggah semua file (termasuk folder `.streamlit`) ke repository GitHub.
2. Buka share.streamlit.io > Create app > pilih repository.
3. Main file path: `app.py`. Klik Deploy.

## Catatan
- Semua data dan skor adalah data contoh untuk demo. Skor AI dihitung dari bobot kategori, bukan dari model yang sudah dilatih.
- Perubahan data hanya bertahan selama halaman terbuka.
