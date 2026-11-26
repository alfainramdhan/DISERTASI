# HAIDAR SMART

Portal Supply Chain & Vendor dengan menu **AI DECISION** (50 kriteria, termasuk Green Supply Chain Management).
Tampilan dan fitur sama persis dengan prototipe artifact; Streamlit dipakai sebagai wadah untuk deploy.

## Isi project
```
app.py              pembungkus Streamlit
haidar.html         seluruh antarmuka dan data contoh
requirements.txt    hanya streamlit
.streamlit/config.toml
```

## Menu AI DECISION (di sidebar kiri)
1. Ringkasan AI Decision
2. Ranking & Rekomendasi Vendor (filter Vendor / Subkon / Mandor, 4 prioritas bobot, unduh CSV)
3. Performa 50 Kriteria (radar 10 kategori, kekuatan dan kelemahan, 50 kriteria, filter GSCM)
4. Bandingkan Vendor (sampai 3 rekanan)
5. Indeks Hijau (GSCM)
6. Bobot & Kriteria Penilaian (daftar 50 kriteria + slider bobot)
7. Peringatan Risiko
8. Model & Algoritma

Performa 50 kriteria juga muncul di **Profil 360° rekanan > Tab 3**.

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
- Data dan skor 50 kriteria adalah **data contoh** untuk demo. Skor AI dihitung dari bobot kategori, bukan dari model yang sudah dilatih.
- Perubahan data (approval, lock, bobot) hanya bertahan selama halaman terbuka.
