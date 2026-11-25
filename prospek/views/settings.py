"""Settings & Tutorial."""
from __future__ import annotations

import streamlit as st

from .. import data as D
from .. import style as S
from ..state import go, open_dialog, reset_data

STEPS = [
    ("Tekan / (atau Ctrl+K) lalu ketik “BAP-001” atau sebuah NPWP.", ("search",)),
    ("Di Partner & Vendor, buka Calon Rekanan lalu centang verifikasi 4 stakeholder.", ("go", 0, "Calon Rekanan")),
    ("Buka Profil 360° rekanan untuk melihat legalitas, performa dan audit log.", ("go", 0, "Rekanan Terseleksi")),
    ("Di Payment & Invoice, klik kartu tahapan lalu buka detail sebuah tagihan.", ("go", 4, "Monitoring Status Tagihan")),
    ("Tekan Approve & Lanjutkan Tahap; nama Anda tercatat di riwayat approval.", ("go", 4, "Monitoring Status Tagihan")),
    ("Buka Asisten PROSPEK di pojok kanan bawah dan pilih pertanyaan cepat.", ("chat",)),
]


def _do(t: tuple) -> None:
    if t[0] == "go":
        go(t[1], t[2])
    else:
        open_dialog(t)


def render() -> None:
    S.page_header("Settings & Tutorial", "Profil pengguna, panduan demo untuk presentasi, dan pengaturan data contoh.")
    st.write("")
    c1, c2 = st.columns([1.3, 1])
    with c1, st.container(key="card_steps"):
        st.html('<b style="font-size:17px">Panduan demo 6 langkah</b>')
        for k, (txt, tgt) in enumerate(STEPS):
            a, b = st.columns([5, 1], vertical_alignment="center")
            a.markdown(f"**{k + 1}.** {txt}")
            b.button("Buka", key=f"step{k}", on_click=_do, args=(tgt,), width="stretch")
    with c2:
        with st.container(key="card_prof"):
            st.html('<b style="font-size:17px;display:block;margin-bottom:12px">Profil pengguna</b>' + S.kv([
                ("Nama", D.USER["nama"]), ("Jabatan", D.USER["jabatan"]), ("Divisi", D.USER["divisi"]),
                ("Tim", D.USER["tim"]), ("Hak akses", "Approver semua tahap (mode demo)")]))
        st.write("")
        with st.container(key="card_data"):
            st.html('<b style="font-size:17px">Data contoh</b><p class="pk-cap" style="font-size:14px">Semua perubahan '
                    '(approval, verifikasi, lock, rekanan baru) tersimpan selama sesi browser ini dan hilang saat sesi berakhir.</p>')
            st.button("Reset data demo", icon=":material/restart_alt:", on_click=reset_data)
        st.write("")
        with st.container(key="card_about"):
            st.html('<b style="font-size:17px">Tentang prototipe</b><p class="pk-cap" style="font-size:14px">PROSPEK v0.2, '
                    'aplikasi Streamlit dengan data contoh. Asisten masih berbasis aturan (belum memakai model AI). '
                    'Integrasi ERP/SAP disimulasikan.</p>')
