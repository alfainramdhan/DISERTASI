"""PROSPEK · Enterprise Supply Chain, Vendor Management & Invoice Approval Portal.

Jalankan lokal:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(page_title="PROSPEK · Supply Chain & Vendor Portal", page_icon=":material/handshake:",
                   layout="wide", initial_sidebar_state="expanded")

from prospek import shell, style  # noqa: E402
from prospek.state import ASSISTANT, flush_toasts, init  # noqa: E402
from prospek.views import assistant, home, invoice, modules, settings, vendor  # noqa: E402

style.inject()
init()
flush_toasts()
shell.sidebar()
shell.header()

mod = st.session_state.mod
if mod < 0:
    home.render()
elif mod == 0:
    vendor.render()
elif mod == 4:
    invoice.render()
elif mod == 7:
    settings.render()
elif mod == ASSISTANT:
    assistant.page()
else:
    modules.render()

if mod != ASSISTANT:
    shell.fab()
shell.router()
