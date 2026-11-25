"""Asisten PROSPEK (chatbot) sebagai dialog mengambang dan sebagai halaman penuh."""
from __future__ import annotations

import streamlit as st

from .. import chatbot as C
from .. import data as D
from .. import style as S
from ..state import open_target

AV = {"assistant": ":material/smart_toy:", "user": ":material/person:"}


def _ensure() -> None:
    if not st.session_state.chat:
        st.session_state.chat = [{"role": "assistant", "actions": [],
                                  "content": f"Halo {D.USER['nama'].split()[0]}, saya Asisten PROSPEK. {C.HELP}"}]


def _ask(q: str) -> None:
    s = st.session_state
    s.chat.append({"role": "user", "content": q, "actions": []})
    txt, acts = C.answer(q, s.V, s.I)
    s.chat.append({"role": "assistant", "content": txt, "actions": acts})


def _body(where: str, height: int | None) -> None:
    _ensure()
    box = st.container(height=height, border=False) if height else st.container()
    with box:
        for k, m in enumerate(st.session_state.chat):
            with st.chat_message(m["role"], avatar=AV[m["role"]]):
                st.markdown(m["content"])
                if m["actions"]:
                    with st.container(horizontal=True):
                        for j, (lab, tgt) in enumerate(m["actions"]):
                            if st.button(lab, key=f"{where}_act{k}_{j}", icon=":material/arrow_outward:"):
                                open_target(tgt)
                                st.rerun()
    with st.container(horizontal=True):
        for j, c in enumerate(C.CHIPS):
            if st.button(c, key=f"{where}_chip{j}", type="secondary"):
                _ask(c)
                st.rerun(scope="fragment") if where == "dlg" else st.rerun()


@st.dialog("Asisten PROSPEK", width="large", on_dismiss="rerun")
def chat_dialog() -> None:
    st.caption("Simulasi berbasis aturan · membaca data vendor & tagihan yang aktif di aplikasi")
    _body("dlg", 380)
    q = st.chat_input("Tanya status BAP, vendor, SOP…", key="chat_dlg")
    if q:
        _ask(q)
        st.rerun(scope="fragment")


def page() -> None:
    S.page_header("Asisten PROSPEK", "Chatbot supply chain & procurement yang membaca data aktif di aplikasi (simulasi berbasis aturan).")
    _body("page", None)
    q = st.chat_input("Tanya status BAP, vendor, SOP…", key="chat_page")
    if q:
        _ask(q)
        st.rerun()
