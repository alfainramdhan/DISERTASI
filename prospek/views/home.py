"""Portal Beranda (Dashboard Hub)."""
from __future__ import annotations

import plotly.graph_objects as go_
import streamlit as st

from .. import data as D
from .. import style as S
from ..state import go


def render() -> None:
    s = st.session_state
    V, I = s.V, s.I
    act, notes = D.active(I), D.notifs(V, I)
    h = D.now().hour
    sal = "Selamat pagi" if h < 11 else "Selamat siang" if h < 15 else "Selamat sore" if h < 18 else "Selamat malam"
    S.hero(
        f"{sal}, {D.USER['nama'].split()[0]}.", D.flong(D.now()),
        f"<b>{len(act)}</b> tagihan dan <b>{len(notes)}</b> tugas menunggu tindakan hari ini. "
        "Tekan <kbd>/</kbd> untuk mencari invoice, BAP, NPWP atau rekanan.",
        [D.USER["jabatan"], D.USER["tim"], D.USER["divisi"]],
        [n["t"] for n in notes[:3]])

    aktif = sum(1 for v in V if v["tahap"] in D.FINAL)
    lel = sum(1 for r in D.GEN["Info Lelang"][1] if r[5] != "Selesai")
    ktr = len(D.GEN["Daftar Kontrak Aktif"][1])
    nod = sum(1 for x in act if x["hari"] > 3)
    K = [("Rekanan Aktif", aktif, f"{len(V)} rekanan terdaftar", (0, "Rekanan Terseleksi")),
         ("Invoice Pending", len(act), f"{D.rps(sum(x['nilai'] for x in act))} · {nod} overdue", (4, "Monitoring Status Tagihan")),
         ("Lelang Aktif", lel, "2 paket masih pendaftaran", (5, "Info Lelang")),
         ("Kontrak Aktif", ktr, "1 kontrak perlu adendum", (3, "Daftar Kontrak Aktif"))]
    st.write("")
    cols = st.columns(4)
    for k, (lab, val, sub, tgt) in enumerate(K):
        with cols[k], st.container(key=f"kpi_h{k}"):
            st.button(f"{lab}\n\n**{val}**\n\n{sub}", key=f"kpih{k}", on_click=go, args=tgt, width="stretch")

    # ---------- direktori modul
    st.html('<div class="pk-section"><h2 class="pk-h2">Direktori modul</h2>'
            '<p class="pk-sub">Klik sub-fitur untuk langsung membuka halamannya.</p></div>')
    st.segmented_control("Kategori modul", D.CATS, key="cat", required=True, label_visibility="collapsed")
    mods = [(i, m) for i, m in enumerate(D.MENU) if s.cat == "Semua Modul" or m["cat"] == s.cat]
    kb = D.k3_badge(V)
    if not mods:
        S.empty("Tidak ada modul di kategori ini")
    for r in range(0, len(mods), 3):
        cols = st.columns(3)
        for c, (i, m) in zip(cols, mods[r:r + 3]):
            with c, st.container(key=f"card_mod{i}"):
                stc = {"Aktif": "green", "Freeze": "yellow", "Non-Aktif": "gray"}[m["st"]]
                st.html(f'<div class="pk-mod"><span class="lt">{m["L"] or "⚙"}</span><div style="flex:1">'
                        f'<b>{S.esc(m["t"])}</b><p>{S.esc(m["d"])}</p></div>{S.tag(m["st"], stc)}</div>')
                if m["subs"]:
                    for j, sb in enumerate(m["subs"]):
                        badge = f" :orange-badge[{kb}]" if sb == "Sertifikasi K3/CQSMS" else ""
                        with st.container(key=f"msub{i}_{j}"):
                            st.button(f"{j + 1}. {sb}{badge}", key=f"msb{i}_{j}", type="tertiary", on_click=go, args=(i, sb))
                else:
                    st.button("Buka pengaturan & tutorial", key=f"msb{i}", type="tertiary", on_click=go, args=(i,))

    # ---------- analitik
    st.html('<div class="pk-section"><h2 class="pk-h2">Analitik</h2>'
            '<p class="pk-sub">Tren nilai tagihan dan performa pengadaan per divisi.</p></div>')
    c1, c2 = st.columns([1.3, 1])
    T = D.TREND
    with c1, st.container(key="card_trend"):
        st.html(f'<b style="font-size:17px">Nilai tagihan naik ke Rp {D._num(T["diajukan"][-1], 1)} M bulan ini</b>'
                '<div class="pk-cap">Miliar rupiah per bulan. *November masih berjalan.</div>')
        f = go_.Figure()
        f.add_scatter(x=T["bulan"], y=T["diajukan"], name="Diajukan", mode="lines+markers",
                      line=dict(color="#030302", width=3, shape="spline"), marker=dict(size=8, color="#fff", line=dict(color="#030302", width=2)))
        f.add_scatter(x=T["bulan"][:5], y=T["dibayar"][:5], name="Disetujui & dibayar", mode="lines+markers",
                      line=dict(color="#ff4500", width=3, shape="spline"), marker=dict(size=8, color="#fff", line=dict(color="#ff4500", width=2)))
        f.add_scatter(x=T["bulan"][4:], y=T["dibayar"][4:], showlegend=False, mode="lines+markers", hoverinfo="skip",
                      line=dict(color="#ff4500", width=3, dash="dot"), marker=dict(size=8, color="#fff", line=dict(color="#ff4500", width=2)))
        f.add_annotation(x=T["bulan"][-1], y=T["diajukan"][-1], text=f"{D._num(T['diajukan'][-1], 1)} M", showarrow=False,
                         yshift=16, font=dict(family="Lora, serif", size=15))
        f.update_yaxes(title="Rp miliar", rangemode="tozero")
        st.plotly_chart(S.plot_layout(f, 320), theme=None, config={"displayModeBar": False})
    with c2, st.container(key="card_div"):
        st.html('<b style="font-size:17px">Performa pengadaan per divisi</b>'
                '<div class="pk-cap">Paket selesai tepat waktu, tahun berjalan. Target 85%.</div>')
        names = [d[0].replace("Divisi ", "") for d in D.DIVP]
        f2 = go_.Figure(go_.Bar(
            x=[d[1] for d in D.DIVP], y=names, orientation="h",
            marker=dict(color=["#9bd8a9" if d[1] >= 85 else "#ff4500" for d in D.DIVP], cornerradius=10),
            text=[f"{d[1]}% · {d[3]} paket · Rp {D._num(d[2], 1)} M" for d in D.DIVP], textposition="inside",
            insidetextanchor="start", textfont=dict(color="#030302"), hovertemplate="%{y}: %{x}%<extra></extra>"))
        f2.add_vline(x=85, line=dict(color="#030302", dash="dot", width=1.5))
        f2.update_xaxes(range=[0, 100], ticksuffix="%")
        f2.update_yaxes(autorange="reversed")
        st.plotly_chart(S.plot_layout(f2, 320), theme=None, config={"displayModeBar": False})
    st.html('<p class="pk-note">Divisi di bawah target 85% ditandai oranye. Semua angka di aplikasi ini adalah data contoh untuk demo.</p>')
