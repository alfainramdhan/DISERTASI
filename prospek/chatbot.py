"""Asisten PROSPEK: chatbot berbasis aturan yang membaca data aktif di aplikasi.

Belum memakai model AI/LLM. Setiap jawaban dihitung langsung dari data vendor dan
tagihan di session_state, sehingga selalu konsisten dengan apa yang tampil di layar.
"""
from __future__ import annotations

import re

from . import data as D

CHIPS = ["Cek status invoice BAP-001", "Tagihan mana saja yang overdue?", "Rekomendasi vendor pekerjaan beton",
         "Dokumen vendor yang hampir kedaluwarsa", "SOP approval tagihan", "SOP registrasi rekanan"]

BIDANG = [("beton", "Pekerjaan Beton"), ("semen", "Pekerjaan Beton"), ("baja", "Struktur Baja"),
          ("jembatan", "Struktur Baja"), ("aspal", "Pekerjaan Jalan & Aspal"), ("jalan", "Pekerjaan Jalan & Aspal"),
          ("mekanikal", "Mekanikal Elektrikal"), ("elektrikal", "Mekanikal Elektrikal"), ("listrik", "Mekanikal Elektrikal"),
          ("alat berat", "Penyewaan Alat Berat"), ("excavator", "Penyewaan Alat Berat"),
          ("pondasi", "Geoteknik & Pondasi"), ("fondasi", "Geoteknik & Pondasi"), ("bored", "Geoteknik & Pondasi"),
          ("precast", "Precast"), ("girder", "Precast"), ("pompa", "Pompa & Hidrolik"),
          ("logistik", "Logistik & Transportasi"), ("angkut", "Logistik & Transportasi"), ("kayu", "Material Kayu"),
          ("survei", "Jasa Survei & Pemetaan"), ("perancah", "Perancah & Bekisting"),
          ("scaffold", "Perancah & Bekisting"), ("bekisting", "Perancah & Bekisting")]

HELP = ("Saya bisa membantu:\n"
        "- cek status dan posisi approval tagihan, misalnya *status BAP-005*\n"
        "- daftar tagihan yang overdue\n"
        "- rekomendasi rekanan per bidang (beton, baja, aspal, precast, alat berat, dan lainnya)\n"
        "- sertifikat K3 yang kedaluwarsa atau hampir habis\n"
        "- SOP approval tagihan dan registrasi rekanan\n\n"
        "Pilih pertanyaan cepat di bawah atau ketik pertanyaan Anda.")


def answer(q: str, V: list[dict], I: list[dict]) -> tuple[str, list[tuple[str, tuple]]]:
    s = q.lower()
    m = re.search(r"bap[\s-]*(\d{1,3})", s)
    if m:
        no = f"BAP-{int(m.group(1)):03d}"
        x = next((i for i in I if i["no"] == no), None)
        if not x:
            return f"Tagihan **{no}** tidak ditemukan. Nomor yang tersedia: BAP-001 sampai BAP-{len(I):03d}.", []
        last = x["hist"][-1]
        pos = "Selesai – siap bayar" if x["stage"] > 5 else f"{D.STG[x['stage']]} ({D.STGP[x['stage']]})"
        txt = (f"**{no}** · {V[x['vi']]['nama']}\n\n{x['pek']}\n\n"
               f"- Nilai: **{D.rp(x['nilai'])}**\n- Posisi: **{pos}**\n")
        if x["stage"] <= 5:
            txt += f"- SLA: {D.sla(x)[0]}, {x['hari']} hari di tahap ini\n"
        txt += f"- Aksi terakhir: {last['s']} oleh {last['n']}, {D.fdt(last['t'])}"
        return txt, [("Buka detail tagihan", ("invoice", no))]

    if re.search(r"overdue|terlambat|lewat|jatuh tempo", s):
        L = sorted([x for x in D.active(I) if x["hari"] > 3], key=lambda x: -x["hari"])
        W = [x for x in D.active(I) if 2 <= x["hari"] <= 3]
        if not L:
            return "Tidak ada tagihan overdue saat ini.", []
        txt = f"Ada **{len(L)} tagihan overdue** (lebih dari 3 hari di satu tahap):\n\n" + "\n".join(
            f"- **{x['no']}** · {x['hari']} hari di {D.STG[x['stage']]} · {D.rps(x['nilai'])}" for x in L)
        if W:
            txt += f"\n\n{len(W)} tagihan lain mendekati jatuh tempo."
        return txt, [("Buka antrean tagihan", ("go", 4, "Monitoring Status Tagihan"))] + [
            (f"Buka {x['no']}", ("invoice", x["no"])) for x in L[:2]]

    if re.search(r"rekomend|terbaik|bandingk|komparasi|vendor untuk|rekanan untuk", s):
        b = next((k for k in BIDANG if k[0] in s), None)
        L = [v for v in V if D.score(v) is not None and (not b or v["bidang"] == b[1])]
        L = sorted(L, key=lambda v: (v["tahap"] not in D.FINAL, -D.score(v)))[:3]
        if not L:
            return "Belum ada rekanan dengan riwayat performa untuk bidang tersebut.", []
        head = f"untuk **{b[1]}**" if b else "dengan skor tertinggi"
        rows = "\n".join(
            f"{k + 1}. **{v['nama']}** · skor {D.score(v)} ({D.grade(D.score(v))[0]}) · tepat waktu {v['ot']}% · "
            f"kualifikasi {v['kual']}" + ("" if v["tahap"] in D.FINAL else " · *belum terseleksi*")
            for k, v in enumerate(L))
        return (f"Rekomendasi rekanan {head}, berdasarkan skor performa proyek sebelumnya:\n\n{rows}",
                [(f"Profil {v['nama']}", ("vendor", v["i"])) for v in L[:2]])

    if re.search(r"kedaluwarsa|kadaluarsa|expired|masa berlaku|sertifikat|k3|risiko|dokumen", s):
        L = [r for r in D.k3_rows(V) if r["st"] != "Valid"]
        if not L:
            return "Semua sertifikat K3 masih berlaku lebih dari 60 hari.", []
        txt = f"**{len(L)} sertifikat K3/CQSMS** perlu perhatian:\n\n" + "\n".join(
            f"- **{r['v']['nama']}** · {r['st']} · {D.fdate(r['exp'])}" for r in L) + (
            "\n\nRekanan dengan sertifikat kedaluwarsa sebaiknya tidak diundang lelang sampai diperbarui.")
        return txt, [("Buka Sertifikasi K3/CQSMS", ("go", 5, "Sertifikasi K3/CQSMS"))]

    if re.search(r"sop|alur|cara|panduan|prosedur", s):
        if re.search(r"rekanan|registrasi|vendor|daftar", s):
            return ("**SOP registrasi rekanan**\n\n1. Rekanan mendaftar → status *Bakal Calon Rekanan*.\n"
                    "2. Kelengkapan dokumen → *Calon Rekanan* / *Calon Perorangan*.\n"
                    "3. Verifikasi 4 tim: Procurement, Legal, K3/QHSSE, Keuangan.\n"
                    "4. Setelah 4/4 → disetujui sebagai *Rekanan Terseleksi* dan dikirim ke SAP.",
                    [("Buka Calon Rekanan", ("go", 0, "Calon Rekanan"))])
        steps = "\n".join(f"{k}. {D.STG[k]} · {D.STGP[k]}" for k in range(1, 6))
        return (f"**SOP approval tagihan**\n\n{steps}\n\nBatas proses tiap tahap 3 hari kerja. "
                "Return wajib disertai catatan revisi dan tagihan kembali ke tahap 1.",
                [("Buka antrean tagihan", ("go", 4, "Monitoring Status Tagihan"))])

    if re.search(r"pending|antrean|berapa|ringkas", s):
        A = D.active(I)
        rows = "\n".join(f"- {D.STG[k]}: {sum(1 for x in A if x['stage'] == k)}" for k in range(1, 6))
        return f"Saat ini ada **{len(A)} tagihan** senilai {D.rps(sum(x['nilai'] for x in A))} di antrean:\n\n{rows}", []

    return HELP, []
