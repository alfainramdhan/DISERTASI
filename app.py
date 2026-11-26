"""HAIDAR AI (Hub for Artificial Intelligence, Digital Acquisition & Resource Management).

Seluruh antarmuka ada di haidar.html (tampilan dan fitur persis seperti
prototipe artifact). File ini hanya membungkusnya agar bisa dijalankan
dan di-deploy di Streamlit Community Cloud.
"""
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="HAIDAR AI | Hub for AI, Digital Acquisition & Resource Management",
    page_icon=str(Path(__file__).parent / "logo.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Sembunyikan elemen bawaan Streamlit agar halaman penuh, tanpa jarak.
st.markdown(
    """
    <style>
      #MainMenu, header, footer, [data-testid="stToolbar"],
      [data-testid="stDecoration"], [data-testid="stStatusWidget"],
      [data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"]
        {display: none !important;}
      .stApp, [data-testid="stAppViewContainer"] {background: #0f1214;}
      .block-container, [data-testid="stMainBlockContainer"]
        {padding: 0 !important; max-width: 100% !important;}
      [data-testid="stVerticalBlock"] {gap: 0 !important;}
      iframe {height: 100vh !important; border: 0; display: block;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def muat_html() -> str:
    return (Path(__file__).parent / "haidar.html").read_text(encoding="utf-8")


components.html(muat_html(), height=900, scrolling=True)
