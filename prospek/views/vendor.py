"""Partner & Vendor Management: master data rekanan, verifikasi 4 stakeholder, Profil 360°."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from .. import data as D
from .. import exports as X
from .. import style as S
from ..state import go, notify, open_dialog, reopen

PASTEL = {"green": "#9bd8a9", "yellow": "#fde99b", "blue": "#b8caf5", "red": "#ffd9c9", "gray": "#efefef"}


def _cell(color: str) -> str:
    return f"background-color:{PASTEL[color]};color:#030302;font-weight:600"


# ---------------------------------------------------------------- callback
def _set_pill(p: str) -> None:
    st.session_state.vpill = p
    st.session_state.vsel = set()


def _stage_change(key: str) -> None:
    val = st.session_state.get(key) or "Semua Rekanan"
    go(0, val)


def _edit(key: str, ids: list[int]) -> None:
    s = st.session_state
    for r, ch in s[key]["edited_rows"].items():
        v = s.V[ids[int(r)]]
        if "Pilih" in ch:
            (s.vsel.add if ch["Pilih"] else s.vsel.discard)(v["i"])
        if "Unlocked" in ch:
            D.set_lock(v, not ch["Unlocked"])
            notify(f"{v['nama']}: {'Locked' if v['locked'] else 'Unlocked'}")
        if ch.get("Profil 360°"):
            s.dlg = ("vendor", v["i"])
    s.ver += 1


def _bulk(action: str) -> None:
    s = st.session_state
    L = [v for v in s.V if v["i"] in s.vsel]
    if action in ("lock", "unlock"):
        for v in L:
            D.set_lock(v, action == "lock", bulk=True)
        notify(f"{len(L)} rekanan di-{'Lock' if action == 'lock' else 'Unlock'}.")
    elif action == "sap":
        n = sum(D.sync_sap(v) for v in L)
        notify(f"{n} rekanan dikirim ke SAP." if n else "Semua rekanan terpilih sudah sinkron dengan SAP.")
    s.vsel = set()
    s.ver += 1


def _reset_filters() -> None:
    st.session_state.vf = {}
    st.session_state.vpill = "Semua Data"


# ---------------------------------------------------------------- halaman
def render() -> None:
    s = st.session_state
    V, sub = s.V, s.sub or "Dashboard Rekanan"
    S.page_header("Partner & Vendor Management", f"{sub} · verifikasi 4 stakeholder sebelum menjadi Rekanan Terseleksi.")
    L = D.vendor_filter(V, sub, s.vpill, s.vf)
    df_out = X.vendor_frame(L)

    with st.container(horizontal=True):
        st.button("Tambah Rekanan Baru", icon=":material/add:", type="primary", on_click=open_dialog, args=(("addv",),))
        st.button("Import Template Excel", icon=":material/upload_file:", on_click=open_dialog, args=(("import",),))
        st.download_button("CSV", X.to_csv(df_out), "prospek_rekanan.csv", "text/csv", icon=":material/download:", on_click="ignore")
        st.download_button("Excel", X.to_xlsx(df_out, "Rekanan"), "prospek_rekanan.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", on_click="ignore")
        st.download_button("PDF", X.to_pdf(df_out, "Laporan Data Rekanan"), "prospek_rekanan.pdf", "application/pdf", on_click="ignore")

    besar = sum(1 for v in V if v["kual"] == "Besar")
    men = sum(1 for v in V if v["kual"] == "Menengah")
    MC = [("Total Rekanan", len(V), f"{sum(1 for v in V if v['tahap'] in D.FINAL)} sudah terseleksi", "Semua Data"),
          ("Terkirim ke SAP", sum(v["sap"] for v in V), "Status Synced", "Sudah ke SAP"),
          ("Belum Sinkron SAP", sum(not v["sap"] for v in V), "Status Pending", "Belum ke SAP"),
          ("Akses Edit Terbuka", sum(not v["locked"] for v in V), "Unlocked untuk rekanan", "Akses Edit Terbuka"),
          ("Usaha Besar & Menengah", besar + men, f"{besar} besar · {men} menengah", "Kualifikasi Besar")]
    st.write("")
    cols = st.columns(5)
    for k, (lab, val, sm, pill) in enumerate(MC):
        on = s.vpill == pill and pill != "Semua Data"
        with cols[k], st.container(key=f"kpi_v{k}_{'on' if on else 'off'}"):
            st.button(f"{lab}\n\n**{val}**\n\n{sm}", key=f"kpiv{k}", on_click=_set_pill, args=(pill,), width="stretch")

    opts = ["Semua Rekanan"] + D.STAGES
    cnt = {o: (len(V) if o == "Semua Rekanan" else sum(1 for v in V if v["tahap"] == o)) for o in opts}
    pk = f"stage_{sub}_{s.ver}"
    st.pills("Posisi / tahapan rekanan", opts, default=sub if sub in D.STAGES else "Semua Rekanan",
             format_func=lambda o: f"{o} · {cnt[o]}", key=pk, on_change=_stage_change, args=(pk,))
    st.segmented_control("Filter cepat", D.PILLS, key="vpill", required=True)

    nf = sum(1 for v in s.vf.values() if v)
    with st.expander("Filter lanjutan" + (f" ({nf} aktif)" if nf else ""), icon=":material/filter_alt:",
                     expanded=sub == "Cek Posisi Rekanan"):
        f = s.vf
        uniq = lambda k: sorted({v[k] for v in V})
        sel = lambda lab, arr, k: st.selectbox(lab, [""] + list(arr), index=([""] + list(arr)).index(f.get(k, "")) if f.get(k, "") in arr else 0,
                                               format_func=lambda o: o or "Semua", key=f"vf_{k}")
        with st.form("vff", border=False):
            a, b, c, d = st.columns(4)
            with a:
                q = st.text_input("Nama perusahaan / email", f.get("q", ""), placeholder="mis. Beton Prima")
                tahap = sel("Posisi / tahapan terkini", D.STAGES, "tahap")
                sap = sel("Status SAP", ["Synced", "Pending"], "sap")
            with b:
                npwp = st.text_input("Nomor NPWP", f.get("npwp", ""), placeholder="01.234.567.8-…")
                bidang = sel("Bidang usaha", uniq("bidang"), "bidang")
                appr = sel("Divisi approver", uniq("divisi"), "appr")
            with c:
                vid = st.text_input("ID Vendor / ID SAP", f.get("vid", ""), placeholder="VND-20410")
                wil = sel("Cakupan wilayah", uniq("wilayah"), "wilayah")
                akses = sel("Status akses edit", ["Locked", "Unlocked"], "akses")
            with d:
                kual = sel("Kualifikasi", ["Besar", "Menengah", "Kecil"], "kual")
            b1, b2, _ = st.columns([1, 1, 4])
            apply = b1.form_submit_button("Terapkan Filter", type="primary", width="stretch")
            reset = b2.form_submit_button("Reset", width="stretch")
        if apply:
            s.vf = {"q": q, "npwp": npwp, "vid": vid, "tahap": tahap, "bidang": bidang, "wilayah": wil,
                    "kual": kual, "sap": sap, "appr": appr, "akses": akses}
            s.vsel, s.ver = set(), s.ver + 1
            st.rerun()
        if reset:
            s.vf = {}
            for k in ("tahap", "sap", "bidang", "appr", "wilayah", "akses", "kual"):
                s.pop(f"vf_{k}", None)
            st.rerun()

    if s.vsel:
        picked = [v for v in V if v["i"] in s.vsel]
        with st.container(horizontal=True, vertical_alignment="center"):
            st.html(f'<span class="pk-bulk">{len(picked)} rekanan dipilih</span>', width="content")
            st.button("Lock", icon=":material/lock:", on_click=_bulk, args=("lock",))
            st.button("Unlock", icon=":material/lock_open:", on_click=_bulk, args=("unlock",))
            st.button("Sync ke SAP", icon=":material/sync:", type="primary", on_click=_bulk, args=("sap",))
            st.download_button("Export terpilih", X.to_xlsx(X.vendor_frame(picked), "Rekanan"), "rekanan_terpilih.xlsx",
                               icon=":material/download:", on_click="ignore")
            st.button("Batal", type="tertiary", on_click=_bulk, args=("clear",))

    if not L:
        S.empty("Tidak ada rekanan yang cocok")
        st.button("Reset filter", on_click=_reset_filters)
        return
    df = pd.DataFrame([{
        "Pilih": v["i"] in s.vsel, "No": k + 1, "Nama Perusahaan": v["nama"],
        "Kontak · Email": f"{v['kontak']} · {v['email']}", "NPWP": v["npwp"], "ID Vendor": v["id"],
        "ID SAP": v["sap_id"] or "–", "SAP": "Synced" if v["sap"] else "Pending", "Posisi / Tahapan": v["tahap"],
        "Persetujuan": D.fdate(v["setuju"]) if v["setuju"] else "Menunggu verifikasi",
        "Verifikasi": sum(v["verif"]), "Divisi": v["divisi"], "Kualifikasi": v["kual"],
        "Tgl Registrasi": v["reg"].date(), "Unlocked": not v["locked"], "Profil 360°": False,
    } for k, v in enumerate(L)])
    sty = (df.style.map(lambda t: _cell(D.TAHAP_COLOR.get(t, "gray")), subset=["Posisi / Tahapan"])
           .map(lambda t: _cell("green" if t == "Synced" else "yellow"), subset=["SAP"]))
    key = f"ved_{s.ver}"
    editable = ["Pilih", "Unlocked", "Profil 360°"]
    st.data_editor(
        sty, key=key, hide_index=True, width="stretch", on_change=_edit, args=(key, [v["i"] for v in L]),
        disabled=[c for c in df.columns if c not in editable],
        column_config={
            "Pilih": st.column_config.CheckboxColumn("Pilih", help="Pilih untuk aksi massal", width="small"),
            "No": st.column_config.NumberColumn("No", width="small"),
            "Nama Perusahaan": st.column_config.TextColumn(width="medium", pinned=True),
            "Kontak · Email": st.column_config.TextColumn(width="large"),
            "Verifikasi": st.column_config.ProgressColumn("Verifikasi 4 tim", min_value=0, max_value=4, format="%d/4", width="small"),
            "Tgl Registrasi": st.column_config.DateColumn(format="D MMM YYYY"),
            "Unlocked": st.column_config.CheckboxColumn("Akses edit (Unlocked)", help="Centang = Unlocked, kosong = Locked"),
            "Profil 360°": st.column_config.CheckboxColumn("Profil 360°", help="Centang untuk membuka Profil 360° rekanan"),
        })
    st.html('<p class="pk-note">Centang <b>Profil 360°</b> untuk membuka profil, <b>Akses edit</b> untuk Lock/Unlock, '
            '<b>Pilih</b> untuk aksi massal. Klik sel lalu Ctrl+C untuk menyalin email, NPWP atau ID SAP. '
            'Verifikasi 4 tim = Procurement, Legal, K3/QHSSE dan Keuangan.</p>')


# ---------------------------------------------------------------- dialog Profil 360°
@st.dialog("Profil 360° Rekanan", width="large", on_dismiss="rerun")
def vendor_dialog(i: int) -> None:
    s = st.session_state
    v = s.V[i]
    n, fin, sc = sum(v["verif"]), v["tahap"] in D.FINAL, D.score(v)
    ver = len(v["log"])
    st.html(f'<div class="pk-cap">{v["id"]} · registrasi {D.fdate(v["reg"])}</div><div class="pk-h2">{S.esc(v["nama"])}</div>'
            + S.tags((v["tahap"], D.TAHAP_COLOR.get(v["tahap"], "gray")), (f"Kualifikasi {v['kual']}", "gray"),
                     (f"SAP {v['sap_id']}" if v["sap"] else "Belum ke SAP", "green" if v["sap"] else "yellow"),
                     ("Locked" if v["locked"] else "Unlocked", "gray" if v["locked"] else "green")))

    c1, c2 = st.columns([1.4, 1], vertical_alignment="center")
    unlocked = c1.toggle("Akses edit terbuka untuk rekanan (Unlocked)", value=not v["locked"], key=f"lk{i}_{ver}")
    if unlocked == v["locked"]:
        D.set_lock(v, not unlocked)
        notify(f"{v['nama']}: {'Locked' if v['locked'] else 'Unlocked'}")
        reopen(("vendor", i))
    if not v["sap"] and c2.button("Kirim ke SAP", icon=":material/sync:", key=f"sap{i}_{ver}"):
        D.sync_sap(v)
        notify(f"{v['nama']} dikirim ke SAP ({v['sap_id']}).")
        reopen(("vendor", i))

    with st.container(key=f"card_ver{i}"):
        st.html(f'<div style="display:flex;justify-content:space-between;align-items:center"><b style="font-size:17px">'
                f'Verifikasi lintas stakeholder</b>{S.tag(f"{n}/4 selesai", "green" if n == 4 else "yellow")}</div>')
        cols = st.columns(2)
        for k, t in enumerate(D.TEAM):
            val = cols[k % 2].checkbox(f"**{t[0]}** · {t[1]}, {t[2]}", value=bool(v["verif"][k]), disabled=fin,
                                       key=f"vchk{i}_{k}_{ver}")
            if val != bool(v["verif"][k]):
                up = D.set_verif(v, k, val)
                notify(f"{t[0]}: verifikasi {'disetujui' if val else 'dibatalkan'}." + (f" Tahapan naik ke {up}." if up else ""))
                reopen(("vendor", i))
        if fin:
            st.caption(f"Ditetapkan sebagai {v['tahap']}" + (f" pada {D.fdate(v['setuju'])}." if v["setuju"] else "."))
        else:
            target = "Rekanan Internasional" if v["wilayah"] == "Internasional" else "Rekanan Terseleksi"
            if st.button(f"Setujui sebagai {target}", type="primary", icon=":material/verified:", disabled=n < 4, key=f"vok{i}_{ver}"):
                D.approve_vendor(v)
                notify(f"{v['nama']} kini {v['tahap']}.")
                reopen(("vendor", i))
            if n < 4:
                st.caption("Tombol aktif setelah keempat tim memverifikasi.")

    t1, t2, t3 = st.tabs(["Profil & Legalitas", "Performa & Riwayat Proyek", "Riwayat Approval & Audit Log"])
    with t1:
        bentuk = ("Perorangan" if v["perorangan"] else "Persekutuan Komanditer (CV)" if v["nama"].startswith("CV")
                  else "Perusahaan asing" if v["wilayah"] == "Internasional" else "Perseroan Terbatas (PT)")
        st.html(S.kv([("Bentuk usaha", bentuk), ("Domisili", v["kota"]), ("Kontak", v["kontak"]), ("NPWP", v["npwp"]),
                      ("Bidang usaha", v["bidang"]), ("Cakupan wilayah", v["wilayah"]), ("Kualifikasi", v["kual"]),
                      ("Divisi approver", v["divisi"])]))
        a, b = st.columns(2)
        a.caption("Email (ikon kanan untuk menyalin)")
        a.code(v["email"], language=None)
        b.caption("ID SAP (ikon kanan untuk menyalin)")
        b.code(v["sap_id"] or "Belum sinkron", language=None)
        st.markdown("**Susunan pengurus / direksi**")
        st.dataframe(pd.DataFrame(v["dir"], columns=["Nama", "Jabatan"]), hide_index=True, width="stretch")
        st.html(f'<b>Rekening bank</b> {S.tag("Terverifikasi" if v["sap"] else "Menunggu verifikasi Keuangan", "green" if v["sap"] else "yellow")}'
                f'<p style="margin:6px 0 14px">{S.esc(v["bank"])}</p><b>Klasifikasi bidang usaha (SBU)</b>'
                f'<p style="margin:6px 0 14px">{S.esc(D.SBU.get(v["bidang"], v["bidang"]))} · kualifikasi {v["kual"]} · wilayah {v["wilayah"]}</p>'
                '<b>Dokumen lampiran</b>')
        docs = [("NIB", f"9120{str(301884 + i * 7713)[:6]}0042", D.add_d(-900 + i * 13), None),
                ("NPWP", v["npwp"], D.add_d(-1500 + i * 20), None),
                ("Akta Perusahaan", f"No. {12 + i} / Notaris R. Siregar, S.H.", D.add_d(-2400 + i * 40), None),
                ("Sertifikat K3 (SMK3)", "Belum diunggah" if v["k3e"] is None else f"SMK3-{4410 + i}",
                 None if v["k3e"] is None else D.add_d(v["k3e"] - 1095), None if v["k3e"] is None else D.add_d(v["k3e"]))]
        dc = st.columns(4)
        for c, (nm, no, terbit, exp) in zip(dc, docs):
            with c, st.container(key=f"card_doc{i}_{nm[:3]}"):
                if exp:
                    lab = ("Kedaluwarsa " if v["k3e"] < 0 else "Segera berakhir " if v["k3e"] <= 60 else "Berlaku s.d. ") + D.fdate(exp)
                    tg = S.tag(lab, D.status_color(lab.split(" ")[0] if v["k3e"] > 60 else lab))
                else:
                    tg = S.tag("Belum diunggah", "gray") if no == "Belum diunggah" else S.tag("Berlaku seterusnya", "green")
                st.html(f'<b>{nm}</b><div class="pk-cap">{S.esc(no)}</div><div class="pk-cap">Terbit {D.fdate(terbit) if terbit else "–"}</div>'
                        f'<div style="margin-top:6px">{tg}</div>')
                if no != "Belum diunggah":
                    with st.popover("Pratinjau", icon=":material/visibility:", width="stretch"):
                        st.html(S.paper(nm, no if nm == "NPWP" else f"{v['id']}/{nm.split()[0].upper()}",
                                        [("Nama pemegang", v["nama"]), ("Domisili", v["kota"]), ("Bidang usaha", v["bidang"]),
                                         ("Penanggung jawab", v["kontak"]),
                                         ("Status verifikasi", "Terverifikasi Tim Legal" if v["verif"][1] else "Menunggu verifikasi")],
                                        "Instansi Penerbit", v["kontak"]))
    with t2:
        if sc is None:
            S.empty("Belum ada riwayat proyek", "Rekanan baru dinilai setelah menyelesaikan proyek pertama.")
        else:
            gl, gc = D.grade(sc)
            st.html(f'<div class="pk-score">{S.ring(sc, gc)}<div style="flex:1"><div class="pk-cap">Skor evaluasi keseluruhan (0–100)</div>'
                    f'<div style="margin:6px 0 8px">{S.tag(gl, gc)}</div><p class="pk-cap" style="font-size:14px;margin:0">'
                    'Bobot: ketepatan waktu 35%, kualitas 35%, K3/CQSMS 30%, dikurangi 1,5 poin per temuan NCR.</p></div></div>')
            col = lambda x: "#9bd8a9" if x >= 75 else "#ff4500"
            st.html('<b style="display:block;margin:20px 0 12px">Metrik historis</b>' + S.bars([
                ("Ketepatan waktu pengiriman / pekerjaan", v["ot"], f"{v['ot']}%", col(v["ot"])),
                ("Skor kualitas pekerjaan", v["ku"], f"{v['ku']}/100 · {v['ncr']} temuan NCR", col(v["ku"])),
                ("Skor kepatuhan K3/CQSMS", v["k3"], f"{v['k3']}/100", col(v["k3"]))]))
            st.markdown("**Riwayat proyek sebelumnya**")
            st.dataframe(pd.DataFrame([{"Proyek": p[0], "Tahun": str(p[1]), "Nilai kontrak": D.rps(p[2]),
                                        "Catatan evaluasi tim proyek": p[3]} for p in v["proj"]]),
                         hide_index=True, width="stretch")
    with t3:
        st.caption("Urutan kronologis dari registrasi hingga keputusan terakhir.")
        st.html(S.timeline([{"who": e["who"], "jab": e["jab"], "when": D.fdt(e["t"]), "note": e["note"], "c": e["c"],
                             "badge": S.tag(e["act"], e["c"])} for e in v["log"]]))


# ---------------------------------------------------------------- dialog tambah & import
@st.dialog("Tambah Rekanan Baru", on_dismiss="rerun")
def add_dialog() -> None:
    st.caption("Rekanan baru masuk sebagai Bakal Calon Rekanan.")
    with st.form("fadd", border=False):
        nama = st.text_input("Nama perusahaan *")
        email = st.text_input("Email *")
        a, b = st.columns(2)
        kontak = a.text_input("Nama kontak *")
        npwp = b.text_input("NPWP *", placeholder="00.000.000.0-000.000")
        bidang = a.selectbox("Bidang usaha", list(D.SBU))
        wil = b.selectbox("Cakupan wilayah", D.WILAYAH)
        kual = a.selectbox("Kualifikasi", ["Besar", "Menengah", "Kecil"], index=1)
        div = b.selectbox("Divisi approver", sorted({v["divisi"] for v in st.session_state.V}))
        ok = st.form_submit_button("Simpan rekanan", type="primary")
    if ok:
        if not all(x.strip() for x in (nama, email, kontak, npwp)):
            st.error("Lengkapi semua kolom bertanda *.")
            return
        v = D.add_vendor(st.session_state.V, {"nama": nama.strip(), "email": email.strip(), "kontak": kontak.strip(),
                                              "npwp": npwp.strip(), "bidang": bidang, "wilayah": wil, "kual": kual, "divisi": div})
        notify(f"{v['nama']} ditambahkan sebagai Bakal Calon Rekanan.")
        go(0, "Bakal Calon Rekanan")
        st.rerun()


@st.dialog("Import Template Excel", width="large", on_dismiss="rerun")
def import_dialog() -> None:
    st.markdown("1. Unduh template, isi di Excel.  \n2. Unggah kembali file **.xlsx** atau **.csv**.  \n"
                "3. Periksa pratinjau, lalu klik Import.")
    st.download_button("Unduh template Excel", X.template_xlsx(), "template_rekanan_prospek.xlsx",
                       icon=":material/download:", on_click="ignore")
    up = st.file_uploader("File rekanan", type=["xlsx", "csv"])
    if not up:
        return
    try:
        df = X.read_import(up)
    except Exception as e:  # noqa: BLE001 - tampilkan pesan apa pun ke pengguna
        st.error(f"File tidak dapat dibaca: {e}")
        return
    df = df[df["nama_perusahaan"].astype(str).str.strip() != ""]
    st.dataframe(df, hide_index=True, width="stretch")
    if st.button(f"Import {len(df)} rekanan", type="primary", disabled=df.empty):
        for _, r in df.iterrows():
            g = lambda k, d="": str(r.get(k, d) or d).strip()
            D.add_vendor(st.session_state.V, {
                "nama": g("nama_perusahaan"), "email": g("email", "-"), "kontak": g("kontak", "-"), "npwp": g("npwp", "-"),
                "bidang": g("bidang_usaha", "Pekerjaan Beton"), "wilayah": g("wilayah", "Nasional"),
                "kual": g("kualifikasi", "Kecil"), "divisi": g("divisi", D.USER["divisi"])})
        notify(f"{len(df)} rekanan diimpor sebagai Bakal Calon Rekanan.")
        go(0, "Bakal Calon Rekanan")
        st.rerun()
