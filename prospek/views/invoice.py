"""Payment & Invoice System: pipeline approval berjenjang 5 tahap."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from .. import data as D
from .. import exports as X
from .. import style as S
from ..state import go, notify, open_dialog, reopen
from .vendor import _cell

SUBNAV = ["Tagihan Proyek", "Tagihan Operasional/Kantor Pusat", "Monitoring Status Tagihan"]
DOCS = ["Berita Acara Pembayaran (BAP)", "Faktur Pajak", "Kwitansi", "Berita Acara Opname"]


def _set_stage(k: int) -> None:
    st.session_state.istage = k
    st.session_state.isel = set()
    st.session_state.ver += 1


def _sub_change(key: str) -> None:
    go(4, st.session_state.get(key) or "Monitoring Status Tagihan")


def _reset() -> None:
    s = st.session_state
    s.istage, s.ikw, s.idiv, s.iproj, s.idone = 0, "", "", "", False
    s.ver += 1


def _edit(key: str, ids: list[str]) -> None:
    s = st.session_state
    for r, ch in s[key]["edited_rows"].items():
        x = next(i for i in s.I if i["no"] == ids[int(r)])
        if "Pilih" in ch:
            if x["stage"] > 5 and ch["Pilih"]:
                notify(f"{x['no']} sudah selesai dan tidak bisa dipilih.")
            else:
                (s.isel.add if ch["Pilih"] else s.isel.discard)(x["no"])
        if ch.get("Detail"):
            s.dlg = ("invoice", x["no"])
    s.ver += 1


def _bulk(action: str) -> None:
    s = st.session_state
    if action == "ok":
        L = [x for x in s.I if x["no"] in s.isel and x["stage"] <= 5]
        for x in L:
            D.approve_invoice(x, "Persetujuan massal (bulk approve).")
        notify(f"{len(L)} tagihan disetujui dan dipindahkan ke tahap berikutnya.")
    s.isel = set()
    s.ver += 1


def render() -> None:
    s = st.session_state
    V, I = s.V, s.I
    sub = s.sub or "Monitoring Status Tagihan"
    S.page_header("Payment & Invoice System", f"{sub} · approval berjenjang 5 tahap dengan pencatatan riwayat approver.")
    L = D.invoice_filter(I, V, sub, s.istage, s.ikw, s.idiv, s.iproj, s.idone)
    out = X.invoice_frame(L, V)

    with st.container(horizontal=True):
        st.button("Post Invoice", icon=":material/add:", type="primary", on_click=open_dialog, args=(("post",),))
        st.download_button("CSV", X.to_csv(out), "prospek_tagihan.csv", "text/csv", icon=":material/download:", on_click="ignore")
        st.download_button("Excel", X.to_xlsx(out, "Tagihan"), "prospek_tagihan.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", on_click="ignore")
        st.download_button("PDF", X.to_pdf(out, "Laporan Status Tagihan"), "prospek_tagihan.pdf", "application/pdf", on_click="ignore")

    key = f"isub_{sub}_{s.ver}"
    st.segmented_control("Jenis tagihan", SUBNAV, default=sub if sub in SUBNAV else "Monitoring Status Tagihan",
                         key=key, on_change=_sub_change, args=(key,), label_visibility="collapsed")

    B = [x for x in D.invoice_base(I, sub) if x["stage"] <= 5]
    with st.container(key="pipe"):
        cols = st.columns(6, gap=None)
        for k in range(6):
            Lk = B if k == 0 else [x for x in B if x["stage"] == k]
            od = sum(1 for x in Lk if x["hari"] > 3)
            lab = (f"{'Semua tahap' if k == 0 else f'Tahap {k}'}\n\n**{D.STG[k]}**\n\n*{len(Lk)}*\n\n"
                   f"{D.rps(sum(x['nilai'] for x in Lk))}{f' · {od} overdue' if od else ''}\n\n{D.STGP[k]}")
            with cols[k], st.container(key=f"stg{k}_{'on' if s.istage == k else 'off'}"):
                st.button(lab, key=f"stgb{k}", on_click=_set_stage, args=(k,), width="stretch")

    a, b, c, d = st.columns([2.2, 1.3, 1.8, 1.2], vertical_alignment="bottom")
    a.text_input("Kata kunci", key="ikw", placeholder="No. BAP, kontrak, rekanan, pekerjaan", live=True, icon=":material/search:")
    b.selectbox("Divisi", [""] + sorted({x["div"] for x in I}), key="idiv", format_func=lambda o: o or "Semua divisi")
    c.selectbox("Nama proyek", [""] + list(D.PROJ), key="iproj", format_func=lambda o: o or "Semua proyek")
    d.toggle("Tampilkan yang selesai", key="idone")

    if s.isel:
        picked = [x for x in I if x["no"] in s.isel]
        with st.container(horizontal=True, vertical_alignment="center"):
            st.html(f'<span class="pk-bulk">{len(picked)} tagihan dipilih</span>', width="content")
            st.button("Bulk Approve", icon=":material/done_all:", type="primary", on_click=_bulk, args=("ok",))
            st.download_button("Export terpilih", X.to_xlsx(X.invoice_frame(picked, V), "Tagihan"), "tagihan_terpilih.xlsx",
                               icon=":material/download:", on_click="ignore")
            st.button("Batal", type="tertiary", on_click=_bulk, args=("clear",))

    if not L:
        S.empty(f"Antrean {D.STG[s.istage]} kosong (0)" if s.istage else "Tidak ada tagihan yang cocok",
                "Tidak ada tagihan di tahap ini. Reset filter untuk melihat semua antrean." if s.istage else
                "Ubah kata kunci atau filter, lalu coba lagi.")
        st.button("Reset filter", on_click=_reset)
        return

    df = pd.DataFrame([{
        "Pilih": x["no"] in s.isel, "No. BAP": x["no"], "Kontrak": x["ktr"], "Rekanan": V[x["vi"]]["nama"],
        "Pekerjaan": x["pek"], "Proyek": x["proj"], "Divisi": x["div"], "Jenis": x["jenis"], "Nilai (Rp)": x["nilai"],
        "Tahap saat ini": D.stage_name(x), "Penanggung jawab": D.STGP[x["stage"]] if x["stage"] <= 5 else "–",
        "SLA": D.sla(x)[0], "Hari di tahap": x["hari"] if x["stage"] <= 5 else None,
        "Catatan": "Pernah dikembalikan" if x["ret"] else "", "Detail": False,
    } for x in L])
    sty = (df.style.map(lambda t: _cell(D.sla_color(t)) if t else "", subset=["SLA"])
           .map(lambda t: _cell("blue") if t != "Selesai – siap bayar" else _cell("green"), subset=["Tahap saat ini"])
           .map(lambda t: _cell("yellow") if t else "", subset=["Catatan"]))
    key = f"ied_{s.ver}"
    st.data_editor(
        sty, key=key, hide_index=True, width="stretch", on_change=_edit, args=(key, [x["no"] for x in L]),
        disabled=[c for c in df.columns if c not in ("Pilih", "Detail")],
        column_config={
            "Pilih": st.column_config.CheckboxColumn("Pilih", width="small"),
            "No. BAP": st.column_config.TextColumn(pinned=True),
            "Pekerjaan": st.column_config.TextColumn(width="large"),
            "Nilai (Rp)": st.column_config.NumberColumn(format="localized"),
            "Hari di tahap": st.column_config.NumberColumn(format="%d hari"),
            "Detail": st.column_config.CheckboxColumn("Detail", help="Centang untuk membuka detail tagihan"),
        })
    st.html('<p class="pk-note">Centang <b>Detail</b> untuk membuka berkas, riwayat approver, dan tombol Approve / Return. '
            'SLA: Normal ≤ 1 hari, Mendekati Jatuh Tempo 2–3 hari, Overdue lebih dari 3 hari di satu tahap.</p>')


# ---------------------------------------------------------------- dialog detail tagihan
@st.dialog("Detail Tagihan", width="large", on_dismiss="rerun")
def invoice_dialog(no: str) -> None:
    s = st.session_state
    x = next((i for i in s.I if i["no"] == no), None)
    if not x:
        st.error("Tagihan tidak ditemukan.")
        return
    v, done = s.V[x["vi"]], x["stage"] > 5
    sl, sc = D.sla(x)
    st.html(f'<div class="pk-cap">Tagihan {x["jenis"]} · {S.esc(x["ktr"])}</div><div class="pk-h2">{no} · {D.rp(x["nilai"])}</div>'
            + S.tags((D.stage_name(x), "green" if done else "blue"), (sl, sc),
                     *((("Pernah dikembalikan", "yellow"),) if x["ret"] else ())))
    st.html('<div style="margin:18px 0 6px">' + S.steps(6 if done else x["stage"]) + "</div>")

    with st.container(key=f"card_inv{no}"):
        st.html('<b style="font-size:17px;display:block;margin-bottom:12px">Rincian tagihan</b>' + S.kv([
            ("Rekanan", v["nama"]), ("Pekerjaan", x["pek"]), ("Proyek", x["proj"]), ("Divisi", x["div"]),
            ("Nilai tagihan (incl. PPN)", D.rp(x["nilai"])), ("Potongan retensi 5%", D.rp(x["nilai"] * 0.05)),
            ("Nilai dibayarkan", D.rp(x["nilai"] * 0.95)), ("Rekening tujuan", v["bank"])]))

    st.html(f'<b style="font-size:17px">Kelengkapan berkas</b> {S.tag("4/4 dokumen lengkap", "green")}')
    dc = st.columns(4)
    for k, (c, d) in enumerate(zip(dc, DOCS)):
        with c, st.container(key=f"card_idoc{no}_{k}"):
            st.html(f'<b>{d}</b><div class="pk-cap">PDF · diunggah {D.fdate(x["hist"][0]["t"])}</div>'
                    f'<div style="margin-top:6px">{S.tag("Lengkap", "green")}</div>')
            with st.popover("Pratinjau", icon=":material/visibility:", width="stretch"):
                st.html(S.paper(d, f"{no}/{''.join(w[0] for w in d.split() if w[0].isalpha()).upper()}",
                                [("Nomor kontrak", x["ktr"]), ("Pekerjaan", x["pek"]), ("Proyek", x["proj"]),
                                 ("Nilai", D.rp(x["nilai"])), ("Rekanan", v["nama"]), ("Tanggal", D.fdate(x["hist"][0]["t"]))],
                                D.APR[0][0], v["kontak"]))

    if done:
        st.success("Tagihan selesai diverifikasi dan siap dibayarkan. Tidak ada tindakan approval tersisa.")
    else:
        with st.container(key=f"card_act{no}"):
            st.html(f'<b style="font-size:17px">Tindakan Anda · {D.STG[x["stage"]]}</b>'
                    f'<div class="pk-cap">Penanggung jawab tahap: {D.STGP[x["stage"]]}</div>')
            note = st.text_area("Catatan (wajib untuk Return / Tolak)", key=f"note_{no}_{len(x['hist'])}",
                                placeholder="mis. Faktur pajak belum sesuai nilai DPP")
            b1, b2 = st.columns(2)
            nxt = D.STG[x["stage"] + 1] if x["stage"] < 5 else "status Selesai"
            if b1.button("Approve & Lanjutkan Tahap", type="primary", icon=":material/check:", width="stretch",
                         key=f"ok_{no}_{len(x['hist'])}"):
                frm = D.STG[x["stage"]]
                D.approve_invoice(x, note.strip())
                notify(f"{no}: {frm} → {D.stage_name(x)}")
                reopen(("invoice", no))
            if b2.button("Return / Tolak", icon=":material/undo:", width="stretch", key=f"ret_{no}_{len(x['hist'])}"):
                if not note.strip():
                    st.error("Catatan revisi wajib diisi sebelum mengembalikan berkas.")
                else:
                    D.return_invoice(x, note.strip())
                    notify(f"{no} dikembalikan ke rekanan untuk revisi.")
                    reopen(("invoice", no))
            st.caption(f"Disetujui atas nama {D.USER['nama']} ({D.USER['jabatan']}); tagihan pindah ke {nxt}.")

    st.html('<b style="font-size:17px;display:block;margin:18px 0 12px">Visual approval history</b>')
    items = []
    for h in x["hist"]:
        c = "red" if h["s"] == "Dikembalikan" else "blue" if h["s"].startswith("Diajukan") else "green"
        items.append({"who": h["n"], "jab": h["j"], "when": f"{h['tahap']} · {D.fdt(h['t'])}", "note": h["note"], "c": c,
                      "badge": S.tag(h["s"], c)})
    if not done:
        items.append({"who": f"Menunggu: {D.STGP[x['stage']]}", "jab": D.STG[x["stage"]],
                      "when": f"{x['hari']} hari di tahap ini", "note": "", "c": "yellow", "badge": S.tag("Menunggu", "yellow")})
    st.html(S.timeline(items))


# ---------------------------------------------------------------- dialog post invoice
@st.dialog("Post Invoice", on_dismiss="rerun")
def post_dialog() -> None:
    s = st.session_state
    vs = [v for v in s.V if v["tahap"] in D.FINAL]
    st.caption("Tagihan baru masuk ke tahap Konfirmasi Proyek.")
    with st.form("fpost", border=False):
        vi = st.selectbox("Rekanan *", [v["i"] for v in vs], format_func=lambda i: s.V[i]["nama"])
        ktr = st.text_input("No. kontrak *", "KTR/INF1/2026/0142")
        pek = st.text_input("Uraian pekerjaan *", placeholder="mis. Pekerjaan pier P19–P24 termin 5")
        proj = st.selectbox("Proyek", list(D.PROJ))
        nilai = st.number_input("Nilai tagihan (Rp) *", min_value=0, step=1_000_000, value=0, format="%d")
        ok = st.form_submit_button("Post Invoice", type="primary")
    if ok:
        if not pek.strip() or not ktr.strip() or nilai <= 0:
            st.error("Lengkapi uraian pekerjaan, nomor kontrak dan nilai tagihan.")
            return
        x = D.post_invoice(s.I, s.V, {"vi": vi, "ktr": ktr.strip(), "pek": pek.strip(), "proj": proj, "nilai": int(nilai)})
        notify(f"{x['no']} masuk antrean Konfirmasi Proyek.")
        go(4, "Tagihan Operasional/Kantor Pusat" if x["jenis"] == "Operasional" else "Monitoring Status Tagihan")
        reopen(("invoice", x["no"]))
