"""State aplikasi (st.session_state), navigasi, dan antrean notifikasi toast."""
from __future__ import annotations

import streamlit as st

from . import data as D

ASSISTANT = 8  # indeks halaman Asisten PROSPEK (di luar akrostik)


def ss():
    return st.session_state


def init() -> None:
    s = st.session_state
    if "V" not in s:
        s.V, s.I = D.build()
    defaults = {"mod": -1, "sub": None, "compact": False, "cat": "Semua Modul", "vpill": "Semua Data",
                "vf": {}, "istage": 0, "ikw": "", "idiv": "", "iproj": "", "idone": False, "ver": 0, "toasts": []}
    for k, v in defaults.items():
        if k not in s:
            s[k] = v
    for k in ("vsel", "isel"):
        if k not in s:
            s[k] = set()
    if "chat" not in s:
        s.chat = []


def reset_data() -> None:
    s = st.session_state
    s.V, s.I = D.build()
    s.vsel, s.isel = set(), set()
    s.vf, s.istage, s.chat = {}, 0, []
    s.ver += 1
    notify("Data demo dikembalikan ke kondisi awal.")


def notify(msg: str) -> None:
    st.session_state.toasts.append(msg)


def flush_toasts() -> None:
    for t in st.session_state.toasts:
        st.toast(t)
    st.session_state.toasts = []


def go(mod: int, sub: str | None = None) -> None:
    s = st.session_state
    s.mod = mod
    if 0 <= mod < len(D.MENU):
        m = D.MENU[mod]
        s.sub = sub or m.get("def") or (m["subs"][0] if m["subs"] else None)
    else:
        s.sub = None
    s.vsel, s.isel = set(), set()
    s.istage = 0
    s.ver += 1
    if mod == 4 and sub == "Post Invoice":
        s.dlg = ("post",)


def open_dialog(spec: tuple) -> None:
    st.session_state.dlg = spec


def open_target(t: tuple) -> None:
    s = st.session_state
    if t[0] == "invoice":
        x = next((i for i in s.I if i["no"] == t[1]), None)
        if x and s.mod != 4:
            go(4, "Tagihan Operasional/Kantor Pusat" if x["jenis"] == "Operasional" else "Monitoring Status Tagihan")
        s.dlg = ("invoice", t[1])
    elif t[0] == "vendor":
        if s.mod != 0:
            go(0, "Semua Rekanan")
        s.dlg = ("vendor", t[1])
    elif t[0] == "go":
        go(t[1], t[2] if len(t) > 2 else None)


def reopen(spec: tuple) -> None:
    """Simpan dialog yang harus dibuka kembali lalu jalankan ulang seluruh aplikasi."""
    st.session_state.dlg = spec
    st.rerun()
