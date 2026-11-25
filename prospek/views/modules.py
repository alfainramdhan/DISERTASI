"""Modul lain: Requisition, Logistics, Smart Contract, E-Procurement, Katalog & RUP."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from .. import data as D
from .. import style as S
from ..state import go
from .vendor import _cell

MONEY = ("Nilai", "HPS", "Pagu", "Harga")


def _sub_change(key: str, mod: int) -> None:
    go(mod, st.session_state.get(key))


def _k3_select(key: str, ids: list[int]) -> None:
    rows = st.session_state[key]["selection"]["rows"]
    if rows:
        st.session_state.dlg = ("vendor", ids[rows[0]])
        st.session_state.ver += 1


def _frame(sub: str, V) -> tuple[pd.DataFrame, list[int] | None]:
    if sub == "Sertifikasi K3/CQSMS":
        R = D.k3_rows(V)
        df = pd.DataFrame([{
            "Rekanan": r["v"]["nama"], "Dokumen": f"SMK3 / CQSMS – {r['v']['id']}", "Skor CQSMS": r["v"]["k3"],
            "Kedaluwarsa": r["exp"].date(),
            "Sisa waktu": f"Lewat {-r['v']['k3e']} hari" if r["v"]["k3e"] < 0 else f"{r['v']['k3e']} hari", "Status": r["st"],
        } for r in R])
        return df, [r["v"]["i"] for r in R]
    cols, rows = D.GEN[sub]
    out = []
    for r in rows:
        rec = {}
        for c, val in zip(cols, r):
            if isinstance(val, tuple) and val[0] == "d":
                rec[c] = D.add_d(val[1]).date()
            elif isinstance(val, tuple) and val[0] == "m":
                rec[c] = val[1]
            else:
                rec[c] = val
        out.append(rec)
    return pd.DataFrame(out), None


def render() -> None:
    s = st.session_state
    m = D.MENU[s.mod]
    sub = s.sub or m["subs"][0]
    c1, c2 = st.columns([5, 1], vertical_alignment="bottom")
    with c1:
        S.page_header(m["t"], m["d"])
    with c2:
        st.html(S.tag(f"Status: {m['st']}", {"Aktif": "green", "Freeze": "yellow", "Non-Aktif": "gray"}[m["st"]]))
    if m["st"] == "Freeze":
        st.html('<div class="pk-banner yellow"><b>Modul berstatus Freeze.</b> Data hanya dapat dibaca; transaksi baru ditahan sementara.</div>')
    elif m["st"] == "Non-Aktif":
        st.html('<div class="pk-banner gray"><b>Modul Non-Aktif untuk divisi Anda.</b> Data di bawah adalah pratinjau.</div>')

    kb = D.k3_badge(s.V)
    key = f"msub_{s.mod}_{s.ver}"
    st.segmented_control("Sub-menu", m["subs"], default=sub, key=key, on_change=_sub_change, args=(key, s.mod),
                         format_func=lambda o: f"{o} ({kb})" if o == "Sertifikasi K3/CQSMS" else o, label_visibility="collapsed")
    df, ids = _frame(sub, s.V)
    if df.empty:
        S.empty("Belum ada data", "Data akan muncul setelah ada transaksi di modul ini.")
        return
    sty = df.style.map(lambda t: _cell(D.status_color(str(t))), subset=["Status"]) if "Status" in df else df.style
    cfg = {c: st.column_config.NumberColumn(f"{c} (Rp)", format="localized") for c in df.columns if c.startswith(MONEY)}
    cfg.update({c: st.column_config.DateColumn(format="D MMM YYYY") for c in df.columns if df[c].dtype == object and len(df) and hasattr(df[c].iloc[0], "isoformat")})
    if ids is not None:
        k = f"k3sel_{s.ver}"
        st.dataframe(sty, key=k, hide_index=True, width="stretch", column_config=cfg,
                     on_select=lambda: _k3_select(k, ids), selection_mode="single-row")
        st.html('<p class="pk-note">Data diambil langsung dari profil rekanan. Klik baris untuk membuka Profil 360°.</p>')
    else:
        st.dataframe(sty, hide_index=True, width="stretch", column_config=cfg)
        st.html('<p class="pk-note">Data contoh untuk keperluan demo.</p>')
