"""Kerangka aplikasi: sidebar akrostik, header, pencarian global, notifikasi, router dialog."""
from __future__ import annotations

import streamlit as st

from . import data as D
from . import style as S
from .state import ASSISTANT, go, open_dialog, open_target
from .views import assistant, invoice, vendor

SLASH_JS = """<script>
(function () {
  if (window.__pkSlash) return; window.__pkSlash = true;
  document.addEventListener('keydown', function (e) {
    if (e.key !== '/' || e.ctrlKey || e.metaKey || e.altKey) return;
    var t = document.activeElement;
    if (t && (/INPUT|TEXTAREA|SELECT/.test(t.tagName) || t.isContentEditable)) return;
    var b = document.querySelector('.st-key-gsearch button');
    if (b) { e.preventDefault(); b.click(); }
  });
  // fokus otomatis ke kolom pencarian saat dialog pencarian terbuka
  setInterval(function () {
    var i = document.querySelector('input[placeholder^="Ketik menu"]');
    if (i && !i.dataset.pkFocused) { i.dataset.pkFocused = '1'; i.focus(); }
  }, 150);
})();
</script>"""



# ---------------------------------------------------------------- sidebar
def sidebar() -> None:
    s = st.session_state
    kb = D.k3_badge(s.V)
    with st.sidebar:
        st.html('<div class="pk-brand"><span class="pk-logo">P</span><span><b>PROSPEK</b>'
                '<small>Supply Chain & Vendor Portal</small></span></div>')
        st.toggle("Mode ringkas (akrostik)", key="compact", help="Tampilkan hanya huruf akrostik P-R-O-S-P-E-K")
        with st.container(key="nav_home"):
            st.button("Beranda", icon=":material/home:", on_click=go, args=(-1,), width="stretch")
        st.html('<div class="pk-acro">P · R · O · S · P · E · K</div>')
        for i, m in enumerate(D.MENU):
            on = s.mod == i
            badge = f" :orange-badge[{kb}]" if m["L"] == "E" else ""
            state = "on" if on else "off"
            if not m["subs"] or s.compact:
                with st.container(key=f"navb{i}_{state}"):
                    if m["L"]:
                        lab = f"**{m['L']}**" if s.compact else f"**{m['L']}** {m['t']}{badge}"
                        st.button(lab, key=f"nb{i}", help=m["t"], on_click=go, args=(i,), width="stretch")
                    else:
                        st.button("Settings & Tutorial" if not s.compact else "Settings", key=f"nb{i}", icon=m["icon"],
                                  on_click=go, args=(i,), width="stretch")
                continue
            with st.container(key=f"nav{i}_{state}"):
                with st.expander(f"**{m['L']}** {m['t']}{badge}", expanded=on):
                    for j, sb in enumerate(m["subs"]):
                        b2 = f" :orange-badge[{kb}]" if sb == "Sertifikasi K3/CQSMS" else ""
                        with st.container(key=f"sub{i}_{j}_{'on' if on and s.sub == sb else 'off'}"):
                            st.button(sb + b2, key=f"sb{i}_{j}", type="tertiary", on_click=go, args=(i, sb),
                                      width="stretch")
        st.divider()
        with st.container(key="nav_chat"):
            st.button("Asisten PROSPEK", icon=":material/smart_toy:", on_click=go, args=(ASSISTANT,), width="stretch")
        st.caption("Prototipe dengan data contoh. Klik ‹‹ di atas untuk menyembunyikan menu.")


# ---------------------------------------------------------------- header
def header() -> None:
    s = st.session_state
    if s.mod < 0:
        crumb = "PROSPEK / <b>Beranda</b>"
    elif s.mod == ASSISTANT:
        crumb = "PROSPEK / <b>Asisten PROSPEK</b>"
    else:
        crumb = f"PROSPEK / {S.esc(D.MENU[s.mod]['t'])}" + (f" / <b>{S.esc(s.sub)}</b>" if s.sub else "")
    L = D.notifs(s.V, s.I)
    c1, c2, c3, c4 = st.columns([3, 3.8, 1.3, 2.9], vertical_alignment="center")
    c1.html(f'<div class="pk-crumb">{crumb}</div>')
    with c2, st.container(key="gsearch"):
        st.button("Cari menu, BAP, NPWP, rekanan `/`", icon=":material/search:", key="gsb", shortcut="ctrl+k",
                  on_click=open_dialog, args=(("search",),), width="stretch")
    with c3:
        with st.popover(str(len(L)), icon=":material/notifications:", width="stretch", help="Notification Center"):
            st.markdown(f"**Tugas menunggu tindakan** · {len(L)} item")
            if not L:
                st.caption("Semua antrean sudah ditangani.")
            ic = {"red": ":material/error:", "yellow": ":material/schedule:", "blue": ":material/how_to_reg:"}
            for k, n in enumerate(L):
                st.button(f"**{n['t']}**  \n{n['s']}", key=f"nt{k}", icon=ic.get(n["c"], ":material/circle:"), type="tertiary",
                          on_click=open_target, args=(n["target"],), width="stretch")
    c4.html(f'<div class="pk-prof"><span class="pk-av">{D.USER["ini"]}</span><span><b>{D.USER["nama"]}</b>'
            f'<small>{D.USER["jabatan"]} · {D.USER["divisi"]}</small></span></div>')
    st.html(SLASH_JS, unsafe_allow_javascript=True)


# ---------------------------------------------------------------- pencarian global
@st.dialog("Pencarian global", width="large", on_dismiss="rerun")
def search_dialog() -> None:
    s = st.session_state
    q = st.text_input("Kata kunci", key="gq", placeholder="Ketik menu, nomor BAP, kontrak, NPWP, ID vendor atau nama rekanan",
                      live=True, icon=":material/search:", label_visibility="collapsed")
    q = (q or "").strip().lower()
    if not q:
        st.caption("Contoh: BAP-004, 01.234.567.8, VND-20413, beton, Sertifikasi K3")
        return
    menus = [(m["t"], i, None, "Modul") for i, m in enumerate(D.MENU)] + \
            [(sb, i, sb, m["t"]) for i, m in enumerate(D.MENU) for sb in m["subs"]]
    mm = [x for x in menus if q in x[0].lower()][:5]
    ii = [x for x in s.I if q in " ".join([x["no"], x["ktr"], x["pek"], x["proj"], s.V[x["vi"]]["nama"]]).lower()][:6]
    vv = [v for v in s.V if q in " ".join([v["nama"], v["npwp"], v["id"], v["sap_id"], v["email"], v["bidang"]]).lower()][:6]
    if not (mm or ii or vv):
        S.empty("Tidak ada hasil", "Coba nomor BAP, NPWP atau nama rekanan.")
        return
    target = None
    if mm:
        st.markdown("**Menu & layanan**")
        for k, (t, i, sb, p) in enumerate(mm):
            if st.button(f"{t}  \n{p}", key=f"gm{k}", type="tertiary", icon=D.MENU[i]["icon"]):
                target = ("go", i, sb)
    if ii:
        st.markdown("**Tagihan**")
        for x in ii:
            if st.button(f"**{x['no']}** · {x['pek']}  \n{s.V[x['vi']]['nama']} · {D.stage_name(x)} · {D.rps(x['nilai'])}",
                         key=f"gi{x['no']}", type="tertiary", icon=":material/receipt_long:"):
                target = ("invoice", x["no"])
    if vv:
        st.markdown("**Rekanan**")
        for v in vv:
            if st.button(f"**{v['nama']}**  \n{v['id']} · NPWP {v['npwp']} · {v['tahap']}", key=f"gv{v['i']}",
                         type="tertiary", icon=":material/handshake:"):
                target = ("vendor", v["i"])
    if target:
        s.pop("gq", None)
        open_target(target)
        st.rerun()


# ---------------------------------------------------------------- tombol asisten & router dialog
def fab() -> None:
    with st.container(key="fab"):
        st.button("Asisten PROSPEK", icon=":material/smart_toy:", type="primary", key="fabb",
                  on_click=open_dialog, args=(("chat",),))


def router() -> None:
    d = st.session_state.pop("dlg", None)
    if not d:
        return
    kind = d[0]
    if kind == "search":
        search_dialog()
    elif kind == "chat":
        assistant.chat_dialog()
    elif kind == "vendor" and 0 <= d[1] < len(st.session_state.V):
        vendor.vendor_dialog(d[1])
    elif kind == "invoice":
        invoice.invoice_dialog(d[1])
    elif kind == "addv":
        vendor.add_dialog()
    elif kind == "import":
        vendor.import_dialog()
    elif kind == "post":
        invoice.post_dialog()
