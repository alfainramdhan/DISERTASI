"""Data contoh (dummy) PROSPEK dan seluruh logika bisnisnya.

Semua data di sini fiktif dan hanya untuk demo. Perubahan (approval, verifikasi,
lock, dll.) disimpan di st.session_state sehingga kembali ke awal saat sesi baru.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Asia/Jakarta")
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
         "September", "Oktober", "November", "Desember"]
BLN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


# ---------------------------------------------------------------- waktu & format
def now() -> datetime:
    return datetime.now(TZ).replace(tzinfo=None, microsecond=0)


def today() -> datetime:
    return now().replace(hour=0, minute=0, second=0)


def add_d(n: int, h: int = 0, m: int = 0) -> datetime:
    return today() + timedelta(days=n, hours=h, minutes=m)


def fdate(d: datetime) -> str:
    return f"{d.day} {BLN[d.month - 1]} {d.year}"


def fdt(d: datetime) -> str:
    return f"{fdate(d)}, {d:%H.%M}"


def flong(d: datetime) -> str:
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def _num(x: float, dec: int) -> str:
    s = f"{x:.{dec}f}"
    ip, _, fp = s.partition(".")
    fp = fp.rstrip("0")
    ip = f"{int(ip):,}".replace(",", ".")
    return ip + ("," + fp if fp else "")


def rp(n: float) -> str:
    return "Rp " + f"{round(n):,}".replace(",", ".")


def rps(n: float) -> str:
    return f"Rp {_num(n / 1e9, 2)} M" if n >= 1e9 else f"Rp {_num(n / 1e6, 1)} jt"


# ---------------------------------------------------------------- master data
USER = {"nama": "Rina Kartika", "ini": "RK", "jabatan": "Manajer Pengadaan",
        "divisi": "Divisi Infrastruktur 1", "tim": "Tim Supply Chain Management"}

MENU = [
    {"L": "P", "t": "Partner & Vendor Management", "cat": "Partner & Vendor", "st": "Aktif",
     "def": "Dashboard Rekanan", "icon": ":material/handshake:",
     "d": "Registrasi, verifikasi 4 stakeholder, profil 360° dan performa rekanan.",
     "subs": ["Dashboard Rekanan", "Bakal Calon Rekanan", "Calon Perorangan", "Calon Rekanan",
              "Rekanan Terseleksi", "Rekanan Internasional", "Pengkinian Data Lama",
              "Cek Posisi Rekanan", "Semua Rekanan"]},
    {"L": "R", "t": "Requisition & Purchasing", "cat": "Requisition", "st": "Aktif",
     "icon": ":material/shopping_cart:", "d": "Permintaan pembelian proyek hingga penerbitan PO.",
     "subs": ["Permintaan Pembelian / SPB", "Pesanan Pembelian / PO"]},
    {"L": "O", "t": "Operational Logistics", "cat": "Logistics", "st": "Aktif",
     "icon": ":material/local_shipping:",
     "d": "Pelacakan pengiriman material dan penerimaan barang di proyek.",
     "subs": ["Pemantauan Pengiriman Material", "Penerimaan Barang Proyek"]},
    {"L": "S", "t": "Smart Contract", "cat": "Contract", "st": "Freeze", "icon": ":material/contract:",
     "d": "Daftar kontrak aktif, masa berlaku dan adendum.",
     "subs": ["Daftar Kontrak Aktif", "Monitoring Masa Berlaku & Adendum"]},
    {"L": "P", "t": "Payment & Invoice System", "cat": "Payment & Invoice", "st": "Aktif",
     "def": "Monitoring Status Tagihan", "icon": ":material/receipt_long:",
     "d": "Penagihan rekanan dengan approval berjenjang 5 tahap.",
     "subs": ["Tagihan Proyek", "Tagihan Operasional/Kantor Pusat", "Post Invoice",
              "Monitoring Status Tagihan"]},
    {"L": "E", "t": "E-Procurement", "cat": "E-Procurement", "st": "Aktif", "icon": ":material/gavel:",
     "d": "Informasi lelang, proses pengadaan dan sertifikasi K3/CQSMS.",
     "subs": ["Info Lelang", "Proses Pengadaan", "Sertifikasi K3/CQSMS"]},
    {"L": "K", "t": "Katalog & RUP", "cat": "Katalog", "st": "Non-Aktif", "icon": ":material/menu_book:",
     "d": "Katalog harga satuan dan rencana umum pengadaan.",
     "subs": ["Katalog Harga Satuan", "Rencana Umum Pengadaan"]},
    {"L": "", "t": "Settings & Tutorial", "cat": "Settings", "st": "Aktif", "icon": ":material/settings:",
     "d": "Profil pengguna, panduan demo dan reset data contoh.", "subs": []},
]
CATS = ["Semua Modul", "Partner & Vendor", "Payment & Invoice", "Requisition", "Logistics", "E-Procurement"]
STAGES = ["Bakal Calon Rekanan", "Calon Perorangan", "Calon Rekanan", "Rekanan Terseleksi",
          "Rekanan Internasional", "Pengkinian Data Lama"]
FINAL = ["Rekanan Terseleksi", "Rekanan Internasional"]
TAHAP_COLOR = {"Bakal Calon Rekanan": "gray", "Calon Perorangan": "yellow", "Calon Rekanan": "yellow",
               "Rekanan Terseleksi": "green", "Rekanan Internasional": "blue", "Pengkinian Data Lama": "red"}
TEAM = [("Tim Procurement", "Andi Pratama", "Staf Senior Pengadaan", "PRC"),
        ("Tim Legal", "Maya Sari, S.H.", "Legal Officer", "LGL"),
        ("Tim K3/QHSSE", "Hendra Wijaya", "QHSSE Officer", "K3"),
        ("Tim Keuangan", "Dewi Lestari", "Analis Keuangan", "KEU")]
VNOTE = ["Dokumen pengalaman & SBU sesuai bidang usaha.",
         "Akta, NIB dan susunan pengurus telah diverifikasi.",
         "SMK3 dan rencana K3 kontrak memenuhi standar CQSMS.",
         "Laporan keuangan & rekening bank terverifikasi."]
STG = ["Total Antrean", "Konfirmasi Proyek", "Verifikasi Operasi", "Verifikasi Keuangan",
       "Persetujuan Manajemen", "Validasi Fisik Berkas"]
STGP = ["Seluruh tagihan aktif", "Kepala Proyek / PM", "Manajer Operasi", "Manajer Keuangan",
        "VP / SVP", "Staf Verifikasi Berkas"]
APR = [("Ir. Bambang Hartono", "Project Manager"), ("Siti Rahmawati, S.T.", "Manajer Operasi Divisi"),
       ("Yusuf Hakim, S.E., Ak.", "Manajer Keuangan Divisi"), ("Dr. Ir. Agus Salim, M.T.", "SVP Divisi"),
       ("Lina Marlina", "Staf Verifikasi Berkas")]
AOK = ["Volume pekerjaan sesuai progres lapangan.", "Sesuai kontrak dan jadwal pelaksanaan.",
       "Nilai tagihan sesuai, faktur pajak valid.", "Disetujui untuk dibayarkan.",
       "Berkas fisik lengkap dan sesuai."]
PROJ = {"Jalan Tol Lintas Selatan Seksi 2": "Divisi Infrastruktur 1",
        "Jembatan Sungai Kahayan II": "Divisi Infrastruktur 1",
        "LRT Koridor Timur Fase 1": "Divisi Infrastruktur 1",
        "Bendungan Cikawung": "Divisi Infrastruktur 2",
        "Peningkatan Jalan Nasional Ruas Cikampek–Pamanukan": "Divisi Infrastruktur 2",
        "RSUD Tipe B Kota Mataram": "Divisi Gedung",
        "PLTU Mulut Tambang Kalsel 2×100 MW": "Divisi EPC",
        "Kantor Pusat": "Kantor Pusat"}
BANKS = ["Bank Mandiri", "BNI", "BRI", "BCA", "BTN"]
DIR2 = ["Sri Wahyuni", "Arief Budiman", "Lestari Handayani", "Dimas Prakoso", "Yuliana Putri", "Bayu Firmansyah"]
PJ = ["Tol Lingkar Utara Seksi 1", "Bendungan Sungai Lematang", "Gedung Kantor Pemkot Tegalsari",
      "Jembatan Batanghari III", "Terminal Bandara Pesisir", "Dermaga Curah Tahap 1",
      "RS Pendidikan Wilayah Timur", "Jalur KA Lintas Pesisir Seksi 4"]
EV = {"g": ["Selesai 2 minggu lebih cepat, dokumentasi lengkap.",
            "Mutu sesuai spesifikasi, responsif terhadap instruksi lapangan.",
            "Nol kecelakaan kerja selama pelaksanaan."],
      "m": ["Sempat terlambat 1 minggu karena pasokan material, tertangani.",
            "Ada 2 temuan NCR minor, ditutup dalam 14 hari.",
            "Koordinasi baik, administrasi tagihan perlu dipercepat."],
      "l": ["Keterlambatan mobilisasi alat 10 hari.", "Temuan NCR berulang pada perawatan alat.",
            "Perlu pembinaan pelaporan K3 harian."]}
SBU = {"Pekerjaan Beton": "BG009 – Konstruksi Gedung Lainnya",
       "Struktur Baja": "SI001 – Jembatan, Jalan Layang & Terowongan",
       "Pekerjaan Jalan & Aspal": "BS001 – Jalan Raya, Jalan Lingkungan",
       "Mekanikal Elektrikal": "EL010 – Instalasi Listrik Gedung",
       "Penyewaan Alat Berat": "PA001 – Penyewaan Alat Konstruksi",
       "Geoteknik & Pondasi": "SP005 – Pekerjaan Fondasi",
       "Precast": "IN003 – Pracetak Beton",
       "Jasa Survei & Pemetaan": "RE104 – Survei & Pemetaan",
       "Pompa & Hidrolik": "MK004 – Instalasi Pompa",
       "Logistik & Transportasi": "Non-konstruksi – Jasa Angkutan",
       "Material Kayu": "Non-konstruksi – Pemasok Material",
       "Perancah & Bekisting": "SP008 – Perancah & Bekisting"}
WILAYAH = ["Nasional", "Jawa", "Sumatera", "Kalimantan", "Sulawesi", "Internasional"]

# nama, email, kontak, npwp, sap, tahap, setuju, divisi, reg, locked, kual, bidang, wilayah,
# verif, ontime, kualitas, ncr, k3, k3exp, kota
VR = [
    ("PT Beton Prima Nusantara", "tender@betonprima.co.id", "Hendro Saputra", "01.234.567.8-012.000", 1, "Rekanan Terseleksi", -210, "Divisi Infrastruktur 1", -400, 1, "Besar", "Pekerjaan Beton", "Nasional", "1111", 94, 91, 1, 93, 320, "Jakarta Timur"),
    ("PT Baja Konstruksi Mandiri", "procurement@bajakm.co.id", "Ratna Dewi", "02.345.678.9-431.000", 1, "Rekanan Terseleksi", -180, "Divisi EPC", -365, 1, "Besar", "Struktur Baja", "Nasional", "1111", 88, 86, 2, 90, 25, "Cilegon"),
    ("PT Aspal Jaya Lestari", "admin@aspaljaya.co.id", "Joko Susilo", "03.456.789.0-321.000", 1, "Rekanan Terseleksi", -150, "Divisi Infrastruktur 2", -300, 0, "Menengah", "Pekerjaan Jalan & Aspal", "Jawa", "1111", 79, 82, 3, 84, 140, "Bekasi"),
    ("PT Mekanikal Elektrikal Sentosa", "info@mesentosa.co.id", "Fransiska Lim", "04.567.890.1-062.000", 0, "Calon Rekanan", None, "Divisi Gedung", -20, 0, "Menengah", "Mekanikal Elektrikal", "Jawa", "1010", 85, 80, 1, 78, 48, "Surabaya"),
    ("PT Geoteknik Bumi Persada", "kontak@geobumi.co.id", "Ahmad Fauzi", "05.678.901.2-511.000", 1, "Rekanan Terseleksi", -90, "Divisi Infrastruktur 1", -260, 1, "Menengah", "Geoteknik & Pondasi", "Sumatera", "1111", 91, 88, 0, 92, 210, "Medan"),
    ("PT Alat Berat Perkasa", "rental@abperkasa.co.id", "Yohanes Tan", "06.789.012.3-412.000", 1, "Rekanan Terseleksi", -300, "Divisi Infrastruktur 2", -500, 1, "Besar", "Penyewaan Alat Berat", "Nasional", "1111", 72, 74, 4, 70, -5, "Balikpapan"),
    ("PT Precast Indonesia Raya", "sales@precastir.co.id", "Wulan Sari", "07.890.123.4-024.000", 1, "Rekanan Terseleksi", -60, "Divisi Infrastruktur 1", -200, 1, "Besar", "Precast", "Nasional", "1111", 90, 93, 1, 89, 410, "Bogor"),
    ("Budi Santoso, S.T.", "budi.santoso.survei@gmail.com", "Budi Santoso", "08.901.234.5-603.000", 0, "Calon Perorangan", None, "Divisi Infrastruktur 2", -12, 0, "Kecil", "Jasa Survei & Pemetaan", "Jawa", "1000", None, None, 0, None, None, "Yogyakarta"),
    ("CV Sinar Teknik Abadi", "sinarteknik@yahoo.co.id", "Rudi Hartono", "09.012.345.6-711.000", 0, "Bakal Calon Rekanan", None, "Divisi Gedung", -5, 0, "Kecil", "Mekanikal Elektrikal", "Sulawesi", "0000", None, None, 0, None, None, "Makassar"),
    ("Ningbo Eastline Steel Trading Co., Ltd.", "export@eastlinesteel.cn", "Li Wei", "TIN 91330201-MA2K", 1, "Rekanan Internasional", -120, "Divisi EPC", -240, 1, "Besar", "Struktur Baja", "Internasional", "1111", 83, 85, 2, 86, 95, "Ningbo, Tiongkok"),
    ("PT Hydro Pompa Teknik", "sales@hydropompa.co.id", "Indra Gunawan", "10.123.456.7-215.000", 0, "Pengkinian Data Lama", -700, "Divisi Infrastruktur 1", -900, 0, "Menengah", "Pompa & Hidrolik", "Kalimantan", "1101", 76, 78, 3, 75, -40, "Banjarmasin"),
    ("PT Logistik Cepat Andalan", "ops@lcandalan.co.id", "Maria Ulfa", "11.234.567.8-045.000", 1, "Rekanan Terseleksi", -45, "Divisi Gedung", -150, 1, "Menengah", "Logistik & Transportasi", "Nasional", "1111", 87, 83, 1, 88, 55, "Tangerang"),
    ("PT Rekayasa Jembatan Nusantara", "tender@rjnusantara.co.id", "Gede Wirawan", "12.345.678.9-901.000", 0, "Calon Rekanan", None, "Divisi Infrastruktur 2", -15, 0, "Besar", "Struktur Baja", "Nasional", "1100", 89, 90, 1, 87, 180, "Denpasar"),
    ("PT Semen Hijau Indonesia", "b2b@semenhijau.co.id", "Taufik Hidayat", "13.456.789.0-407.000", 1, "Rekanan Terseleksi", -30, "Divisi Infrastruktur 1", -120, 0, "Besar", "Pekerjaan Beton", "Nasional", "1111", 92, 89, 0, 91, 15, "Gresik"),
    ("CV Kayu Lestari Jepara", "cvkayulestari@gmail.com", "Slamet Riyadi", "14.567.890.1-517.000", 0, "Bakal Calon Rekanan", None, "Divisi Gedung", -3, 0, "Kecil", "Material Kayu", "Jawa", "0000", None, None, 0, None, None, "Jepara"),
    ("CV Mitra Scaffolding", "cs@mitrascaff.co.id", "Agus Purnomo", "15.678.901.2-026.000", 0, "Calon Rekanan", None, "Divisi Gedung", -25, 1, "Menengah", "Perancah & Bekisting", "Jawa", "1110", 68, 66, 5, 64, 70, "Bandung"),
]

# no, kontrak, vendor, pekerjaan, proyek, jenis, nilai, tahap, hari di tahap, pernah dikembalikan
IR = [
    ("BAP-001", "KTR/INF1/2026/0142", 0, "Struktur pier P12–P18 termin 4", "Jalan Tol Lintas Selatan Seksi 2", "Proyek", 4285000000, 3, 4, 0),
    ("BAP-002", "KTR/INF1/2026/0157", 6, "Girder precast PCI H-210 (24 unit)", "Jalan Tol Lintas Selatan Seksi 2", "Proyek", 6120000000, 4, 1, 0),
    ("BAP-003", "KTR/INF2/2026/0088", 2, "Pengaspalan AC-WC STA 4+200–6+800", "Peningkatan Jalan Nasional Ruas Cikampek–Pamanukan", "Proyek", 1940000000, 2, 3, 1),
    ("BAP-004", "KTR/INF2/2026/0091", 5, "Sewa excavator PC200 & vibro roller Oktober 2026", "Bendungan Cikawung", "Proyek", 785500000, 1, 5, 0),
    ("BAP-005", "KTR/EPC/2026/0034", 9, "Impor baja WF 700 & plat 25 mm batch 2", "PLTU Mulut Tambang Kalsel 2×100 MW", "Proyek", 9870000000, 5, 2, 0),
    ("BAP-006", "KTR/INF1/2026/0120", 4, "Bored pile Ø1000 abutment A1 (32 titik)", "Jembatan Sungai Kahayan II", "Proyek", 2310000000, 1, 2, 0),
    ("BAP-007", "KTR/GDG/2026/0076", 11, "Jasa angkut material Oktober 2026", "RSUD Tipe B Kota Mataram", "Proyek", 312400000, 2, 1, 0),
    ("BAP-008", "KTR/INF1/2026/0163", 13, "Pasokan semen PCC 1.800 ton", "Jalan Tol Lintas Selatan Seksi 2", "Proyek", 2196000000, 3, 2, 0),
    ("BAP-009", "KTR/EPC/2026/0041", 1, "Fabrikasi struktur baja boiler house", "PLTU Mulut Tambang Kalsel 2×100 MW", "Proyek", 5430000000, 2, 6, 0),
    ("BAP-010", "KTR/KP/2026/0019", 11, "Jasa kurir dokumen & ekspedisi kantor pusat", "Kantor Pusat", "Operasional", 48750000, 1, 1, 0),
    ("BAP-011", "KTR/KP/2026/0022", 5, "Sewa forklift gudang pusat November 2026", "Kantor Pusat", "Operasional", 96300000, 3, 3, 0),
    ("BAP-012", "KTR/INF2/2026/0095", 2, "Pekerjaan marka & rambu jalan", "Peningkatan Jalan Nasional Ruas Cikampek–Pamanukan", "Proyek", 428000000, 4, 4, 0),
    ("BAP-013", "KTR/INF1/2026/0170", 0, "Ready mix K-350 untuk pile cap (1.240 m³)", "Jembatan Sungai Kahayan II", "Proyek", 1587000000, 5, 0, 0),
    ("BAP-014", "KTR/GDG/2026/0081", 6, "Panel precast fasad gedung tower B", "RSUD Tipe B Kota Mataram", "Proyek", 2765000000, 1, 0, 0),
    ("BAP-015", "KTR/INF1/2026/0174", 4, "Soil investigation & uji CPT 40 titik", "LRT Koridor Timur Fase 1", "Proyek", 618000000, 2, 2, 0),
    ("BAP-016", "KTR/INF1/2026/0142", 0, "Struktur pier P06–P11 termin 3", "Jalan Tol Lintas Selatan Seksi 2", "Proyek", 3960000000, 6, 0, 0),
    ("BAP-017", "KTR/GDG/2026/0076", 11, "Jasa angkut material September 2026", "RSUD Tipe B Kota Mataram", "Proyek", 287900000, 6, 0, 0),
]


def D(n):  # sel tanggal relatif (hari dari hari ini)
    return ("d", n)


def M(n):  # sel nilai rupiah
    return ("m", n)


GEN = {
    "Permintaan Pembelian / SPB": (["No. SPB", "Uraian kebutuhan", "Proyek", "Diminta oleh", "Tanggal", "Status"], [
        ["SPB/INF1/2026/0412", "Besi beton ulir D25 – 48 ton", "Jalan Tol Lintas Selatan Seksi 2", "Ir. Bambang Hartono", D(-3), "Menunggu Persetujuan"],
        ["SPB/INF2/2026/0388", "Sewa crane crawler 80 ton – 2 bulan", "Bendungan Cikawung", "Dedi Kurniawan", D(-6), "Diproses Pengadaan"],
        ["SPB/GDG/2026/0215", "Kabel NYY 4×95 mm² – 1.200 m", "RSUD Tipe B Kota Mataram", "Fajar Nugroho", D(-9), "Menjadi PO"],
        ["SPB/EPC/2026/0107", "Baut HTB M24 grade 10.9 – 6.000 set", "PLTU Mulut Tambang Kalsel 2×100 MW", "Rizal Effendi", D(-1), "Draf"]]),
    "Pesanan Pembelian / PO": (["No. PO", "Rekanan", "Uraian", "Nilai", "Jadwal kirim", "Status"], [
        ["PO/INF1/2026/0931", "PT Precast Indonesia Raya", "Girder PCI H-210 (24 unit)", M(6120000000), D(12), "Dikirim Sebagian"],
        ["PO/INF1/2026/0944", "PT Semen Hijau Indonesia", "Semen PCC 1.800 ton", M(2196000000), D(4), "Diterbitkan"],
        ["PO/GDG/2026/0402", "PT Logistik Cepat Andalan", "Jasa angkut material Nov 2026", M(318000000), D(7), "Diterbitkan"],
        ["PO/EPC/2026/0118", "Ningbo Eastline Steel Trading Co., Ltd.", "Baja WF 700 batch 3", M(10450000000), D(38), "Menunggu Persetujuan"]]),
    "Pemantauan Pengiriman Material": (["No. DO", "Material", "Rekanan", "Rute", "ETA", "Status"], [
        ["DO-PIR-1187", "Girder PCI H-210 (6 unit)", "PT Precast Indonesia Raya", "Bogor → Seksi 2 STA 12+400", D(1), "Dalam Perjalanan"],
        ["DO-SHI-0773", "Semen PCC 300 ton", "PT Semen Hijau Indonesia", "Gresik → Batching plant Seksi 2", D(0), "Tiba Hari Ini"],
        ["DO-NES-0042", "Baja WF 700 (MV Eastline 7)", "Ningbo Eastline Steel Trading Co., Ltd.", "Ningbo → Pelabuhan Trisakti", D(9), "Dalam Perjalanan"],
        ["DO-LCA-2210", "Panel fasad precast (14 unit)", "PT Logistik Cepat Andalan", "Surabaya → Mataram", D(-2), "Terlambat"]]),
    "Penerimaan Barang Proyek": (["No. BPB", "Material", "Volume", "Proyek", "Diterima oleh", "Status"], [
        ["BPB/INF1/2026/1503", "Ready mix K-350", "420 m³", "Jembatan Sungai Kahayan II", "Arif Rahman (Site Engineer)", "Diterima"],
        ["BPB/INF1/2026/1511", "Girder PCI H-210", "6 unit", "Jalan Tol Lintas Selatan Seksi 2", "Teguh Prasetyo (Logistik)", "Diterima"],
        ["BPB/GDG/2026/0688", "Kabel NYY 4×95 mm²", "600 m", "RSUD Tipe B Kota Mataram", "Nur Aini (QC)", "Diterima Bersyarat"],
        ["BPB/INF2/2026/0921", "Geotextile non-woven 300 g/m²", "4.000 m²", "Bendungan Cikawung", "Wahyu Hidayat (Logistik)", "Menunggu QC"]]),
    "Daftar Kontrak Aktif": (["No. Kontrak", "Rekanan", "Lingkup pekerjaan", "Nilai kontrak", "Periode", "Status"], [
        ["KTR/INF1/2026/0142", "PT Beton Prima Nusantara", "Struktur pier & pier head", M(28400000000), "Feb 2026 – Jun 2027", "Aktif"],
        ["KTR/INF1/2026/0157", "PT Precast Indonesia Raya", "Pengadaan girder PCI", M(24800000000), "Mar 2026 – Feb 2027", "Aktif"],
        ["KTR/EPC/2026/0034", "Ningbo Eastline Steel Trading Co., Ltd.", "Pasokan baja struktur impor", M(41200000000), "Jan 2026 – Des 2026", "Aktif"],
        ["KTR/INF2/2026/0088", "PT Aspal Jaya Lestari", "Perkerasan aspal & marka", M(12750000000), "Apr 2026 – Jan 2027", "Aktif"],
        ["KTR/INF1/2026/0120", "PT Geoteknik Bumi Persada", "Bored pile & uji PDA", M(9600000000), "Mei 2026 – Mar 2027", "Aktif"],
        ["KTR/GDG/2026/0076", "PT Logistik Cepat Andalan", "Jasa angkut material proyek", M(3450000000), "Jan 2026 – Des 2026", "Aktif"]]),
    "Monitoring Masa Berlaku & Adendum": (["No. Kontrak", "Rekanan", "Berakhir", "Sisa waktu", "Adendum", "Status"], [
        ["KTR/INF2/2026/0091", "PT Alat Berat Perkasa", D(20), "20 hari", "–", "Segera Berakhir"],
        ["KTR/EPC/2026/0034", "Ningbo Eastline Steel Trading Co., Ltd.", D(36), "36 hari", "Adendum I – perpanjangan waktu", "Proses Adendum"],
        ["KTR/INF2/2026/0088", "PT Aspal Jaya Lestari", D(67), "67 hari", "–", "Berlaku"],
        ["KTR/GDG/2026/0058", "PT Mekanikal Elektrikal Sentosa", D(-4), "Lewat 4 hari", "–", "Kedaluwarsa"]]),
    "Info Lelang": (["Kode lelang", "Paket pekerjaan", "HPS", "Batas pendaftaran", "Peserta", "Status"], [
        ["LL-2026-118", "Jalan akses quarry Bendungan Cikawung", M(8900000000), D(6), "7 rekanan", "Pendaftaran"],
        ["LL-2026-121", "Elevator & eskalator RSUD Mataram", M(14300000000), D(11), "4 rekanan", "Pendaftaran"],
        ["LL-2026-109", "Survei topografi LRT Koridor Timur", M(1250000000), D(-8), "9 rekanan", "Evaluasi"],
        ["LL-2026-097", "Bekisting sistem Tower B", M(3400000000), D(-30), "6 rekanan", "Selesai"]]),
    "Proses Pengadaan": (["Paket", "Metode", "Tahapan", "PIC", "Target selesai", "Status"], [
        ["Elevator & eskalator RSUD Mataram", "Lelang terbuka", "Aanwijzing", "Rina Kartika", D(21), "Berjalan"],
        ["Survei topografi LRT Koridor Timur", "Lelang terbatas", "Evaluasi teknis", "Andi Pratama", D(9), "Berjalan"],
        ["Sewa tower crane Tower B", "Penunjukan langsung", "Negosiasi harga", "Andi Pratama", D(4), "Berjalan"],
        ["Pasokan pipa HDPE Bendungan", "Lelang terbuka", "Penetapan pemenang", "Rina Kartika", D(-2), "Terlambat"]]),
    "Katalog Harga Satuan": (["Kode", "Item", "Satuan", "Harga satuan", "Rekanan", "Berlaku s.d."], [
        ["KHS-BTN-001", "Ready mix K-350 (slump 12±2)", "m³", M(1265000), "PT Beton Prima Nusantara", D(120)],
        ["KHS-BSI-014", "Besi beton ulir D25 BJTS 420", "kg", M(13850), "PT Baja Konstruksi Mandiri", D(45)],
        ["KHS-ASP-007", "Aspal AC-WC (hampar + padat)", "ton", M(1490000), "PT Aspal Jaya Lestari", D(200)],
        ["KHS-ALB-021", "Sewa excavator PC200 + operator", "jam", M(385000), "PT Alat Berat Perkasa", D(-10)],
        ["KHS-SMN-003", "Semen PCC 50 kg", "zak", M(61500), "PT Semen Hijau Indonesia", D(90)]]),
    "Rencana Umum Pengadaan": (["Kode RUP", "Paket", "Pagu", "Metode", "Jadwal", "Status"], [
        ["RUP-2027-001", "Jembatan Kahayan II tahap 2", M(186000000000), "Lelang terbuka", "Q1 2027", "Direncanakan"],
        ["RUP-2027-004", "Pembelian alat berat Divisi EPC", M(42500000000), "Lelang terbatas", "Q1 2027", "Direncanakan"],
        ["RUP-2026-077", "Fasad & MEP Tower B RSUD", M(38900000000), "Lelang terbuka", "Q4 2026", "Berjalan"],
        ["RUP-2026-052", "Bored pile LRT fase 1", M(27300000000), "Lelang terbuka", "Q3 2026", "Selesai"]]),
}

TREND = {"bulan": ["Jun", "Jul", "Agu", "Sep", "Okt", "Nov*"],
         "diajukan": [18.4, 22.1, 19.7, 26.3, 24.8, 31.2],
         "dibayar": [16.9, 20.4, 18.2, 23.5, 22.1, 12.6]}
DIVP = [("Divisi Infrastruktur 1", 92, 146.0, 38), ("Divisi Infrastruktur 2", 84, 98.5, 27),
        ("Divisi Gedung", 88, 63.2, 19), ("Divisi EPC", 79, 211.7, 14)]


# ---------------------------------------------------------------- penilaian
def score(v: dict) -> int | None:
    if v["ot"] is None:
        return None
    s = 0.35 * v["ot"] + 0.35 * v["ku"] + 0.3 * v["k3"] - v["ncr"] * 1.5
    return round(max(0, min(100, s)))


def grade(s: int | None) -> tuple[str, str]:
    if s is None:
        return "Belum dinilai", "gray"
    if s >= 85:
        return "Sangat Baik", "green"
    if s >= 75:
        return "Baik", "blue"
    if s >= 60:
        return "Cukup", "yellow"
    return "Perlu Pembinaan", "red"


def status_color(s: str) -> str:
    import re
    if re.search(r"Terlambat|Kedaluwarsa|Ditolak|Overdue|Lewat", s):
        return "red"
    if re.search(r"Bersyarat|Sebagian|Menunggu|Perlu|Segera|Proses|Draf|Pendaftaran|Evaluasi|Berjalan|Direncanakan|Diproses|Mendekati", s):
        return "yellow"
    if "Perjalanan" in s:
        return "blue"
    if re.search(r"Aktif|Berlaku|Diterima|Tiba|Selesai|PO|Diterbitkan|Disetujui|Terkirim|Valid|Normal|Synced", s):
        return "green"
    return "gray"


# ---------------------------------------------------------------- pembangun data
def mk_vendor(r: tuple, i: int) -> dict:
    (nama, email, kontak, npwp, sap, tahap, setuju, divisi, reg, locked, kual, bidang, wilayah,
     verif, ot, ku, ncr, k3, k3e, kota) = r
    v = {"i": i, "id": f"VND-{20410 + i}", "nama": nama, "email": email, "kontak": kontak, "npwp": npwp,
         "sap": bool(sap), "sap_id": str(1000452 + i * 7) if sap else "", "tahap": tahap,
         "setuju": None if setuju is None else add_d(setuju, 15, 20), "divisi": divisi,
         "reg": add_d(reg, 9, 5), "locked": bool(locked), "kual": kual, "bidang": bidang,
         "wilayah": wilayah, "verif": [int(c) for c in verif], "ot": ot, "ku": ku, "ncr": ncr,
         "k3": k3, "k3e": k3e, "kota": kota}
    v["perorangan"] = not (nama.startswith(("PT", "CV")) or "Ltd" in nama)
    v["bank"] = f"{BANKS[i % 5]} · {str(1370000000 + i * 48271913)[:10]} a.n. {nama}"
    v["dir"] = ([(kontak, "Pemilik / Tenaga Ahli")] if v["perorangan"] else
                [(kontak, "Direktur Utama"), (DIR2[i % 6], "Direktur Operasional"), (DIR2[(i + 3) % 6], "Komisaris")])
    sc = score(v)
    bank = None if sc is None else EV["g"] if sc >= 85 else EV["m"] if sc >= 70 else EV["l"]
    v["proj"] = [] if bank is None else [
        (PJ[(i + k * 3) % 8], 2025 - k, ((i % 5) + 2) * (k + 2) * 0.61e9 + 0.85e9, bank[k]) for k in range(3)]
    log = [{"t": v["reg"], "who": "Sistem e-Registrasi", "jab": "Portal Rekanan", "act": "Registrasi diajukan",
            "note": f"Akun didaftarkan oleh {kontak}.", "c": "blue"}]
    for k, f in enumerate(v["verif"]):
        if f:
            log.append({"t": add_d(reg + 1 + k, 10 + k, 30), "who": TEAM[k][1], "jab": f"{TEAM[k][2]} · {TEAM[k][0]}",
                        "act": "Verifikasi disetujui", "note": VNOTE[k], "c": "green"})
    if v["setuju"]:
        lab = "Rekanan Terseleksi" if tahap == "Pengkinian Data Lama" else tahap
        log.append({"t": v["setuju"], "who": "Ir. Hadi Susanto, M.M.", "jab": "Ketua Komite Seleksi Rekanan",
                    "act": f"Ditetapkan sebagai {lab}", "note": "Memenuhi seluruh persyaratan kualifikasi.", "c": "green"})
    if tahap == "Pengkinian Data Lama":
        log.append({"t": add_d(-14, 8), "who": "Sistem e-Registrasi", "jab": "Pengingat otomatis",
                    "act": "Wajib pengkinian data",
                    "note": "Data terakhir diperbarui lebih dari 18 bulan lalu; sertifikat K3 kedaluwarsa.", "c": "yellow"})
    v["log"] = sorted(log, key=lambda e: e["t"])
    return v


def mk_invoice(r: tuple, V: list[dict]) -> dict:
    no, ktr, vi, pek, proj, jenis, nilai, stage, hari, ret = r
    x = {"no": no, "ktr": ktr, "vi": vi, "pek": pek, "proj": proj, "div": PROJ.get(proj, "Kantor Pusat"),
         "jenis": jenis, "nilai": nilai, "stage": stage, "hari": hari, "ret": bool(ret), "hist": []}
    h, ven = x["hist"], V[vi]
    d = -(hari + min(stage, 6) * 2 + 2 + (4 if ret else 0))

    def at(day, hr):
        return add_d(day, hr, (len(h) * 17) % 60)

    h.append({"t": at(d, 9), "n": ven["kontak"], "j": f"Perwakilan {ven['nama']}", "s": "Diajukan",
              "tahap": "Pengajuan", "note": "Berkas tagihan diunggah melalui portal rekanan."})
    if ret:
        d += 2
        h.append({"t": at(d, 10), "n": APR[0][0], "j": APR[0][1], "s": "Disetujui", "tahap": STG[1], "note": AOK[0]})
        d += 1
        h.append({"t": at(d, 14), "n": APR[1][0], "j": APR[1][1], "s": "Dikembalikan", "tahap": STG[2],
                  "note": "Volume opname STA 5+000–5+400 belum sesuai gambar as-built. Mohon revisi BA opname."})
        d += 1
        h.append({"t": at(d, 11), "n": ven["kontak"], "j": f"Perwakilan {ven['nama']}", "s": "Diajukan ulang",
                  "tahap": "Revisi", "note": "BA opname telah direvisi dan ditandatangani ulang."})
    for s in range(1, min(stage, 6)):
        d += 2
        h.append({"t": at(d, 10 + s), "n": APR[s - 1][0], "j": APR[s - 1][1], "s": "Disetujui",
                  "tahap": STG[s], "note": AOK[s - 1]})
    return x


def build() -> tuple[list[dict], list[dict]]:
    V = [mk_vendor(r, i) for i, r in enumerate(VR)]
    I = [mk_invoice(r, V) for r in IR]
    return V, I


# ---------------------------------------------------------------- turunan
def active(I):
    return [x for x in I if x["stage"] <= 5]


def sla(x: dict) -> tuple[str, str]:
    if x["stage"] > 5:
        return "Selesai", "green"
    if x["hari"] > 3:
        return "Overdue > 3 Hari", "red"
    if x["hari"] >= 2:
        return "Mendekati Jatuh Tempo", "yellow"
    return "Normal", "green"


def sla_color(label: str) -> str:
    return {"Overdue > 3 Hari": "red", "Mendekati Jatuh Tempo": "yellow", "Normal": "green", "Selesai": "green"}.get(label, "gray")


def stage_name(x: dict) -> str:
    return "Selesai – siap bayar" if x["stage"] > 5 else STG[x["stage"]]


def k3_rows(V):
    rows = []
    for v in V:
        if v["k3e"] is None:
            continue
        st = "Kedaluwarsa" if v["k3e"] < 0 else "Perlu Pembaruan" if v["k3e"] <= 60 else "Valid"
        rows.append({"v": v, "exp": add_d(v["k3e"]), "st": st})
    return sorted(rows, key=lambda r: r["exp"])


def k3_badge(V) -> int:
    return sum(1 for r in k3_rows(V) if r["st"] != "Valid")


def notifs(V, I):
    L = []
    for x in active(I):
        if x["hari"] > 3:
            L.append({"c": "red", "t": f"{x['no']} overdue {x['hari']} hari",
                      "s": f"{STG[x['stage']]} · {V[x['vi']]['nama']}", "target": ("invoice", x["no"])})
    for x in active(I):
        if x["stage"] == 4 and x["hari"] <= 3:
            L.append({"c": "yellow", "t": f"{x['no']} menunggu persetujuan VP/SVP",
                      "s": f"{rps(x['nilai'])} · {x['proj']}", "target": ("invoice", x["no"])})
    for v in V:
        if v["tahap"] in ("Calon Rekanan", "Calon Perorangan"):
            n = sum(v["verif"])
            if n < 4:
                L.append({"c": "blue", "t": f"Verifikasi calon rekanan {n}/4", "s": v["nama"],
                          "target": ("vendor", v["i"])})
    for r in k3_rows(V):
        if r["st"] != "Valid":
            L.append({"c": "yellow", "t": f"Sertifikat K3 {r['st'].lower()}",
                      "s": f"{r['v']['nama']} · {fdate(r['exp'])}", "target": ("vendor", r["v"]["i"])})
    return L


# ---------------------------------------------------------------- filter
PILLS = ["Semua Data", "Akses Edit Terbuka", "Sudah ke SAP", "Belum ke SAP", "Kualifikasi Besar", "Kualifikasi Menengah"]


def vendor_filter(V, sub, pill, f):
    L = list(V)
    if sub in STAGES:
        L = [v for v in L if v["tahap"] == sub]
    pf = {"Akses Edit Terbuka": lambda v: not v["locked"], "Sudah ke SAP": lambda v: v["sap"],
          "Belum ke SAP": lambda v: not v["sap"], "Kualifikasi Besar": lambda v: v["kual"] == "Besar",
          "Kualifikasi Menengah": lambda v: v["kual"] == "Menengah"}.get(pill)
    if pf:
        L = [v for v in L if pf(v)]

    def has(a, b):
        return str(b).lower() in str(a).lower()

    digits = lambda s: "".join(c for c in str(s) if c.isdigit())
    if f.get("q"):
        L = [v for v in L if has(v["nama"] + " " + v["email"], f["q"])]
    if f.get("npwp"):
        L = [v for v in L if has(v["npwp"], f["npwp"]) or (digits(f["npwp"]) and digits(f["npwp"]) in digits(v["npwp"]))]
    if f.get("vid"):
        L = [v for v in L if has(v["id"] + " " + v["sap_id"], f["vid"])]
    for k, fld in (("tahap", "tahap"), ("bidang", "bidang"), ("wilayah", "wilayah"), ("kual", "kual"), ("appr", "divisi")):
        if f.get(k):
            L = [v for v in L if v[fld] == f[k]]
    if f.get("sap"):
        L = [v for v in L if v["sap"] == (f["sap"] == "Synced")]
    if f.get("akses"):
        L = [v for v in L if v["locked"] == (f["akses"] == "Locked")]
    return L


def jenis_of(sub):
    return {"Tagihan Proyek": "Proyek", "Tagihan Operasional/Kantor Pusat": "Operasional"}.get(sub, "")


def invoice_base(I, sub):
    j = jenis_of(sub)
    return [x for x in I if not j or x["jenis"] == j]


def invoice_filter(I, V, sub, stage, kw, div, proj, done):
    L = [x for x in invoice_base(I, sub) if done or x["stage"] <= 5]
    if stage:
        L = [x for x in L if x["stage"] == stage]
    if kw:
        k = kw.lower()
        L = [x for x in L if k in " ".join([x["no"], x["ktr"], x["pek"], V[x["vi"]]["nama"]]).lower()]
    if div:
        L = [x for x in L if x["div"] == div]
    if proj:
        L = [x for x in L if x["proj"] == proj]
    return sorted(L, key=lambda x: (x["stage"] > 5, -x["hari"]))


# ---------------------------------------------------------------- mutasi
def _log(v, act, note="", c="gray", jab=None):
    v["log"].append({"t": now(), "who": USER["nama"], "jab": jab or USER["jabatan"], "act": act, "note": note, "c": c})


def set_lock(v, locked: bool, bulk=False):
    if v["locked"] == locked:
        return
    v["locked"] = locked
    _log(v, ("Akses edit dikunci" if locked else "Akses edit dibuka") + (" (massal)" if bulk else ""),
         c="gray" if locked else "yellow")


def sync_sap(v) -> bool:
    if v["sap"]:
        return False
    v["sap"], v["sap_id"] = True, str(1000452 + v["i"] * 7)
    _log(v, "Dikirim ke SAP", f"Vendor master ID {v['sap_id']}", "green")
    return True


def set_verif(v, k: int, val: bool) -> str | None:
    v["verif"][k] = 1 if val else 0
    _log(v, "Verifikasi disetujui" if val else "Verifikasi dibatalkan", VNOTE[k] if val else "",
         "green" if val else "red", f"{USER['jabatan']} (input atas nama {TEAM[k][0]})")
    if v["tahap"] == "Bakal Calon Rekanan" and val:
        v["tahap"] = "Calon Perorangan" if v["perorangan"] else "Calon Rekanan"
        return v["tahap"]
    return None


def approve_vendor(v):
    v["tahap"] = "Rekanan Internasional" if v["wilayah"] == "Internasional" else "Rekanan Terseleksi"
    v["setuju"], v["locked"] = now(), True
    _log(v, f"Ditetapkan sebagai {v['tahap']}", "Verifikasi 4/4 lengkap.", "green",
         f"{USER['jabatan']} · Komite Seleksi Rekanan")


def approve_invoice(x, note=""):
    x["hist"].append({"t": now(), "n": USER["nama"], "j": USER["jabatan"], "s": "Disetujui",
                      "tahap": STG[x["stage"]], "note": note or AOK[x["stage"] - 1]})
    x["stage"] += 1
    x["hari"] = 0


def return_invoice(x, note):
    x["hist"].append({"t": now(), "n": USER["nama"], "j": USER["jabatan"], "s": "Dikembalikan",
                      "tahap": STG[x["stage"]], "note": note})
    x["stage"], x["hari"], x["ret"] = 1, 0, True


def add_vendor(V, o: dict) -> dict:
    i = len(V)
    v = mk_vendor((o["nama"], o["email"], o["kontak"], o["npwp"], 0, "Bakal Calon Rekanan", None,
                   o["divisi"], 0, 0, o["kual"], o["bidang"], o["wilayah"], "0000",
                   None, None, 0, None, None, o.get("kota") or "–"), i)
    v["reg"] = now()
    v["log"][0].update(t=now(), note=f"Ditambahkan oleh {USER['nama']}.")
    V.append(v)
    return v


def post_invoice(I, V, o: dict) -> dict:
    no = f"BAP-{len(I) + 1:03d}"
    jenis = "Operasional" if o["proj"] == "Kantor Pusat" else "Proyek"
    x = mk_invoice((no, o["ktr"], o["vi"], o["pek"], o["proj"], jenis, o["nilai"], 1, 0, 0), V)
    x["hist"][0] = {"t": now(), "n": USER["nama"], "j": USER["jabatan"], "s": "Diajukan", "tahap": "Post Invoice",
                    "note": "Tagihan diinput melalui menu Post Invoice."}
    I.append(x)
    return x
