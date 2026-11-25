"""Sistem desain PROSPEK (gaya "Craft Docs": scrapbook collage) dan helper HTML."""
from __future__ import annotations

import html
import random

import streamlit as st

from . import data as D

esc = html.escape

CSS = r"""
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Lora:ital,wght@0,400;0,500;1,400&display=swap');
:root {
  --color-canvas: #fff3e7; --color-ink: #030302; --color-white: #ffffff; --color-linen: #f7f7f7;
  --color-cloud: #efefef; --color-ash: #e1e1e1; --color-stone: #bebbba; --color-graphite: #41413f;
  --color-mint: #9bd8a9; --color-marigold: #fde99b; --color-periwinkle: #b8caf5; --color-sky: #9ed4ef;
  --gradient-sky: linear-gradient(in oklab, rgb(158, 212, 239) 0px, rgb(209, 238, 249) 100%);
  --color-papaya: #ff4500; --color-azure: #0087ff;
  --font-untitledseriffont: 'Lora', 'UntitledSerifFont', ui-serif, Georgia, Cambria, "Times New Roman", Times, serif;
  --font-untitledsansfont: 'Inter', 'UntitledSansFont', ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --text-caption: 12px; --text-body-sm: 14px; --text-body: 16px; --text-subheading: 24px;
  --text-heading-sm: 36px; --text-heading: 46px; --text-heading-lg: 56px; --text-display: 66px;
  --radius-xl: 14px; --radius-2xl: 20px; --radius-3xl: 24px; --radius-pills: 9999px;
  --shadow-xl: rgba(0,0,0,.01) 0px 50px 40px 0px, rgba(0,0,0,.02) 0px 50px 40px 0px, rgba(0,0,0,.05) 0px 20px 40px 0px, rgba(0,0,0,.08) 0px 3px 10px 0px;
  --shadow-sm: rgba(0,0,0,.1) 0px 4px 6px -1px, rgba(0,0,0,.1) 0px 2px 4px -2px;
  --shadow-md: rgba(0,0,0,.1) 0px 12px 12px 2px, rgba(0,0,0,.06) 0px 2px 4px -1px;
  --shadow-md-2: rgba(0,0,0,.08) 0px 4px 16px 0px;
  --shadow-subtle: rgba(0,0,0,.1) 0px 1px 3px 0px, rgba(0,0,0,.1) 0px 1px 2px -1px;
  --shadow-md-3: rgba(0,0,0,.1) 0px 4px 12px 0px;
}
html, body, .stApp { font-family: var(--font-untitledsansfont); color: var(--color-ink); letter-spacing: -0.24px; font-feature-settings: "liga"; }
.stApp { background: var(--color-canvas); }
[data-testid="stMainBlockContainer"] { max-width: 1280px; padding-top: 1.2rem; padding-bottom: 7rem; }
[data-testid="stHeader"] { background: transparent; }
h1, h2 { font-family: var(--font-untitledseriffont) !important; font-weight: 400 !important; color: var(--color-ink); }
h3, h4, h5, h6 { font-family: var(--font-untitledsansfont) !important; letter-spacing: -0.4px; }
.pk-h1 { font-family: var(--font-untitledseriffont); font-weight: 400; font-size: clamp(34px, 4vw, 46px); line-height: 1.1; letter-spacing: -1.38px; margin: 0; color: var(--color-ink); text-wrap: balance; }
.pk-h2 { font-family: var(--font-untitledseriffont); font-weight: 400; font-size: clamp(26px, 3vw, 36px); line-height: 1.2; letter-spacing: -0.72px; margin: 0; }
.pk-sub { color: var(--color-graphite); font-size: 16px; margin: 8px 0 0; }
.pk-cap { color: #75726f; font-size: 13px; letter-spacing: 0.12px; }
.pk-section { margin-top: 56px; }

/* ---------- tombol ---------- */
button[data-testid^="stBaseButton"] { font-family: var(--font-untitledsansfont); font-weight: 500; transition: box-shadow .15s, transform .15s; }
button[data-testid="stBaseButton-primary"] { background: var(--color-ink); border-color: var(--color-ink); color: #fff; border-radius: var(--radius-pills); }
button[data-testid="stBaseButton-primary"]:hover { background: #222; border-color: #222; box-shadow: var(--shadow-md); color: #fff; }
button[data-testid="stBaseButton-secondary"] { background: var(--color-white); border: 1px solid var(--color-ash); border-radius: var(--radius-pills); color: var(--color-ink); }
button[data-testid="stBaseButton-secondary"]:hover { border-color: var(--color-ink); box-shadow: var(--shadow-md-3); color: var(--color-ink); }
[data-testid="stDownloadButton"] button { border-radius: var(--radius-pills); }
button[data-testid="stBaseButton-tertiary"]:hover { color: var(--color-papaya); }

/* ---------- input ---------- */
[data-baseweb="input"], [data-baseweb="select"] > div, [data-baseweb="textarea"] { border-radius: var(--radius-xl) !important; background: #fff !important; }
[data-testid="stForm"] { background: #fff; border: 0; border-radius: var(--radius-3xl); box-shadow: var(--shadow-xl); padding: 24px; }

/* ---------- kartu ---------- */
[class*="st-key-card"] { background: var(--color-white); border-radius: var(--radius-3xl); box-shadow: var(--shadow-xl); padding: 24px; }
[data-testid="stExpander"] details { border-radius: var(--radius-xl); border-color: var(--color-ash); background: #fff; }
[data-testid="stDataFrame"], [data-testid="stDataFrameResizable"] { border-radius: 16px; overflow: hidden; box-shadow: var(--shadow-subtle); background: #fff; }
[data-testid="stPlotlyChart"] { border-radius: 16px; }
div[role="dialog"] { border-radius: var(--radius-3xl) !important; box-shadow: var(--shadow-xl) !important; background: #fff !important; }
div[role="dialog"] h2 { font-family: var(--font-untitledseriffont) !important; letter-spacing: -0.72px; }
[data-testid="stPopoverBody"] { border-radius: var(--radius-2xl); box-shadow: var(--shadow-md); }
[data-testid="stTabs"] button[role="tab"] p { font-weight: 600; font-size: 15px; }
[data-testid="stChatMessage"] { background: #fff; border-radius: 18px; padding: 12px 14px; box-shadow: var(--shadow-subtle); }

/* ---------- kartu KPI / metrik (tombol berbentuk kartu) ---------- */
[class*="st-key-kpi"] button { width: 100%; min-height: 138px; display: flex; justify-content: flex-start; align-items: flex-start; text-align: left;
  background: #fff; border: 0; border-radius: var(--radius-3xl); box-shadow: var(--shadow-xl); padding: 20px 22px; color: var(--color-ink); }
[class*="st-key-kpi"] button:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); color: var(--color-ink); }
[class*="st-key-kpi"] button div[data-testid="stMarkdownContainer"] { width: 100%; text-align: left; }
[class*="st-key-kpi"] button p { margin: 0 !important; font-size: 14px; color: var(--color-graphite); line-height: 1.45; text-align: left; }
[class*="st-key-kpi"] button p strong { display: block; font-family: var(--font-untitledseriffont); font-weight: 400; font-size: 44px; line-height: 1.1; letter-spacing: -1.4px; color: var(--color-ink); margin: 4px 0; }
[class*="st-key-kpi"][class*="_on"] button { box-shadow: 0 0 0 2px var(--color-ink), var(--shadow-xl); }

/* ---------- pipeline approval: kartu chevron ---------- */
[class*="st-key-stg"] button { width: 100%; min-height: 150px; display: flex; align-items: flex-start; justify-content: flex-start; text-align: left; border: 0;
  border-radius: 0; background: #fff; color: var(--color-ink); padding: 16px 30px 16px 26px;
  clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 50%, calc(100% - 18px) 100%, 0 100%, 18px 50%); }
.st-key-stg0_on button, .st-key-stg0_off button { clip-path: polygon(0 0, calc(100% - 18px) 0, 100% 50%, calc(100% - 18px) 100%, 0 100%); border-radius: 20px 0 0 20px; padding-left: 20px; }
[class*="st-key-stg"] button:hover { background: var(--color-linen); color: var(--color-ink); }
[class*="st-key-stg"][class*="_on"] button { background: var(--color-ink); color: #fff; }
[class*="st-key-stg"][class*="_on"] button:hover { background: #222; color: #fff; }
[class*="st-key-stg"] button div[data-testid="stMarkdownContainer"] { text-align: left; width: 100%; }
[class*="st-key-stg"] button p { margin: 0 !important; font-size: 13px; line-height: 1.4; text-align: left; }
[class*="st-key-stg"] button p strong { display: block; font-size: 15px; font-weight: 600; margin: 2px 0; }
[class*="st-key-stg"] button p em { display: block; font-style: normal; font-family: var(--font-untitledseriffont); font-size: 36px; line-height: 1.1; letter-spacing: -1px; }
.st-key-pipe [data-testid="stHorizontalBlock"] { gap: 4px; flex-wrap: nowrap; overflow-x: auto; padding-bottom: 4px; }
.st-key-pipe [data-testid="stColumn"] { min-width: 150px; }

/* tombol rata kiri */
[class*="st-key-kpi"] button > div, [class*="st-key-stg"] button > div, [class*="st-key-navb"] button > div, .st-key-nav_home button > div,
.st-key-nav_chat button > div, [class*="st-key-sub"] button > div, .st-key-gsearch button > div, [class*="st-key-msub"] button > div,
[data-testid="stPopoverBody"] button[data-testid="stBaseButton-tertiary"] > div, div[role="dialog"] button[data-testid="stBaseButton-tertiary"] > div { justify-content: flex-start; width: 100%; text-align: left; }
[data-testid="stPopoverBody"] button[data-testid="stBaseButton-tertiary"] p, div[role="dialog"] button[data-testid="stBaseButton-tertiary"] p { text-align: left; }
[data-testid="stPopover"] button { white-space: nowrap; }

/* ---------- sidebar akrostik ---------- */
[data-testid="stSidebar"] { box-shadow: var(--shadow-subtle); border-right: 0; }
[data-testid="stSidebar"] [data-testid="stExpander"] details { border: 0; background: transparent; }
[data-testid="stSidebar"] [data-testid="stExpander"] summary { border-radius: var(--radius-xl); padding: 6px 8px; }
[data-testid="stSidebar"] [data-testid="stExpander"] summary:hover { background: var(--color-canvas); }
[data-testid="stSidebar"] summary p { font-size: 14px; font-weight: 500; }
[class*="st-key-nav"] summary p strong:first-child, [class*="st-key-navb"] button p strong {
  display: inline-grid; place-items: center; width: 30px; height: 30px; border-radius: 10px; margin-right: 10px;
  background: var(--color-cloud); color: var(--color-ink); font-family: var(--font-untitledsansfont); font-size: 15px; font-weight: 700; }
[class*="st-key-nav"][class*="_on"] summary p strong:first-child, [class*="st-key-navb"][class*="_on"] button p strong { background: var(--color-ink); color: #fff; }
[class*="st-key-navb"] button, .st-key-nav_home button, .st-key-nav_chat button { justify-content: flex-start; width: 100%; border: 0; background: transparent; box-shadow: none; padding-left: 8px; border-radius: var(--radius-xl); }
[class*="st-key-navb"] button:hover, .st-key-nav_home button:hover, .st-key-nav_chat button:hover { background: var(--color-canvas); color: var(--color-ink); }
[class*="st-key-sub"] button { justify-content: flex-start; width: 100%; padding: 4px 10px; border-radius: 10px; min-height: 34px; }
[class*="st-key-sub"][class*="_on"] button { background: var(--color-marigold); color: var(--color-ink); font-weight: 600; }
.pk-brand { display: flex; align-items: center; gap: 12px; margin: 0 0 8px; }
.pk-logo { width: 44px; height: 44px; border-radius: 14px; background: var(--color-ink); color: #fff; display: grid; place-items: center; font-family: var(--font-untitledseriffont); font-size: 24px; transform: rotate(-4deg); box-shadow: var(--shadow-md-3); }
.pk-brand b { font-family: var(--font-untitledseriffont); font-weight: 400; font-size: 26px; letter-spacing: -0.6px; display: block; line-height: 1; }
.pk-brand small { color: #75726f; font-size: 12px; }
.pk-acro { font-family: var(--font-untitledsansfont); font-weight: 600; letter-spacing: 1px; white-space: nowrap; font-size: 13px; color: #75726f; margin: 14px 0 4px 6px; }

/* ---------- header ---------- */
.pk-crumb { font-size: 14px; color: #75726f; padding-top: 10px; }
.pk-crumb b { color: var(--color-ink); font-weight: 600; }
.st-key-gsearch button { width: 100%; justify-content: flex-start; background: #fff; border: 1px solid var(--color-ash); border-radius: var(--radius-xl); color: #8a8785; min-height: 44px; font-weight: 400; }
.st-key-gsearch button code { margin-left: auto; background: var(--color-cloud); color: var(--color-graphite); border-radius: 6px; padding: 0 7px; }
.st-key-gsearch button div[data-testid="stMarkdownContainer"] { width: 100%; }
.st-key-gsearch button p { display: flex; width: 100%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.st-key-gsearch button [data-testid="stMarkdownContainer"] { overflow: hidden; }
.pk-prof { display: flex; gap: 10px; align-items: center; justify-content: flex-end; }
.pk-av { width: 42px; height: 42px; border-radius: 50%; background: var(--color-mint); display: grid; place-items: center; font-weight: 700; flex: none; }
.pk-prof b { display: block; font-size: 14px; line-height: 1.2; }
.pk-prof small { color: #75726f; font-size: 12px; line-height: 1.3; display: block; }

/* ---------- tombol asisten mengambang ---------- */
.st-key-fab { position: fixed; right: 28px; bottom: 28px; z-index: 999; width: auto !important; }
.st-key-fab button { padding: 14px 22px; box-shadow: var(--shadow-md); font-weight: 600; }

/* ---------- tag / badge ---------- */
.pk-tag { display: inline-flex; align-items: center; gap: 4px; padding: 2px 10px; border-radius: 9999px; font-size: 12.5px; font-weight: 600; white-space: nowrap; letter-spacing: 0.12px; line-height: 20px; }
.pk-tag.green { background: var(--color-mint); color: #10331b; }
.pk-tag.yellow { background: var(--color-marigold); color: #4a3a00; }
.pk-tag.blue { background: var(--color-periwinkle); color: #172a5e; }
.pk-tag.red { background: #ffd9c9; color: #9e2a00; box-shadow: inset 0 0 0 1px rgba(255,69,0,.35); }
.pk-tag.gray { background: var(--color-cloud); color: var(--color-graphite); }
.pk-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }

/* ---------- hero kolase ---------- */
.pk-hero { position: relative; overflow: hidden; border-radius: 28px; background: var(--gradient-sky); padding: clamp(24px, 4vw, 48px); min-height: 330px; box-shadow: var(--shadow-xl); display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, .9fr); gap: 24px; align-items: center; }
.pk-hero::before { content: ""; position: absolute; inset: 0; background-image: radial-gradient(rgba(3,3,2,.13) 1px, transparent 1.4px); background-size: 18px 18px; pointer-events: none; }
.pk-hero > * { position: relative; }
.pk-hero .when { font-size: 14px; color: var(--color-graphite); }
.pk-hero h1 { font-family: var(--font-untitledseriffont) !important; font-weight: 400 !important; font-size: clamp(40px, 5.4vw, 66px); line-height: 1.05; letter-spacing: -2.64px; margin: 6px 0 12px; padding: 0; }
.pk-hero p { font-size: 17px; color: var(--color-graphite); max-width: 46ch; margin: 0; }
.pk-hero kbd { background: #fff; border: 1px solid var(--color-ash); border-radius: 6px; padding: 0 6px; font: 600 13px var(--font-untitledsansfont); }
.pk-hero .chips { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 18px; }
.pk-hero .chips span { background: rgba(255,255,255,.75); border-radius: 9999px; padding: 5px 12px; font-size: 13px; box-shadow: var(--shadow-subtle); }
.pk-hero img { width: 100%; height: auto; max-height: 300px; }
@media (max-width: 900px) { .pk-hero { grid-template-columns: minmax(0, 1fr); } .pk-hero img { max-height: 200px; } }

/* ---------- direktori modul ---------- */
.pk-mod { display: flex; gap: 12px; align-items: flex-start; }
.pk-mod .lt { width: 44px; height: 44px; flex: none; border-radius: 14px; display: grid; place-items: center; font-family: var(--font-untitledseriffont); font-size: 24px; background: var(--color-ink); color: #fff; }
.pk-mod b { font-size: 17px; display: block; line-height: 1.3; }
.pk-mod p { margin: 4px 0 0; color: var(--color-graphite); font-size: 14px; }
[class*="st-key-card_mod"] [class*="st-key-msub"] button { justify-content: flex-start; padding: 2px 0; min-height: 30px; }
[class*="st-key-card_mod"] [class*="st-key-msub"] button p { font-size: 14px; text-align: left; }

/* ---------- komponen detail ---------- */
.pk-kv { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(100%, 200px), 1fr)); gap: 14px 22px; }
.pk-kv dt { font-size: 12.5px; color: #75726f; } .pk-kv dd { margin: 2px 0 0; font-weight: 600; font-size: 15px; }
.pk-steps { display: grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap: 6px; }
.pk-steps div { font-size: 13px; font-weight: 600; color: #8a8785; border-top: 5px solid var(--color-ash); padding-top: 6px; line-height: 1.3; }
.pk-steps .d { border-color: var(--color-mint); color: #1f6b38; } .pk-steps .c { border-color: var(--color-ink); color: var(--color-ink); }
.pk-tl { list-style: none; margin: 0; padding: 0; }
.pk-tl li { position: relative; padding: 0 0 20px 34px; }
.pk-tl li::before { content: ""; position: absolute; left: 10px; top: 24px; bottom: 0; width: 2px; background: var(--color-ash); }
.pk-tl li:last-child::before { display: none; }
.pk-tl .dot { position: absolute; left: 0; top: 1px; width: 22px; height: 22px; border-radius: 50%; display: grid; place-items: center; font-size: 12px; font-weight: 700; }
.pk-tl .dot.green { background: var(--color-mint); } .pk-tl .dot.red { background: var(--color-papaya); color: #fff; }
.pk-tl .dot.blue { background: var(--color-periwinkle); } .pk-tl .dot.yellow { background: var(--color-marigold); } .pk-tl .dot.gray { background: var(--color-cloud); }
.pk-tl .who { font-weight: 600; } .pk-tl .jab { color: #75726f; }
.pk-tl .when { font-size: 13px; color: #75726f; }
.pk-tl .nt { margin-top: 6px; background: var(--color-linen); border-radius: 12px; padding: 8px 12px; font-size: 14px; }
.pk-bars { display: grid; gap: 16px; }
.pk-bar .lab { display: flex; justify-content: space-between; gap: 10px; font-size: 14px; margin-bottom: 6px; }
.pk-bar .tr { height: 12px; background: var(--color-cloud); border-radius: 9999px; overflow: hidden; }
.pk-bar .tr i { display: block; height: 100%; border-radius: 9999px; }
.pk-score { display: flex; gap: 22px; align-items: center; flex-wrap: wrap; }
.pk-paper { background: #fff; border-radius: 6px; padding: 28px; font-size: 14px; box-shadow: var(--shadow-md-2); transform: rotate(-.4deg); border-top: 6px solid var(--color-marigold); }
.pk-paper h4 { text-align: center; text-decoration: underline; margin: 0 0 4px; font-size: 15px; }
.pk-paper .c { text-align: center; color: #75726f; margin-bottom: 16px; }
.pk-paper table { width: 100%; border-collapse: collapse; } .pk-paper td { padding: 4px 0; vertical-align: top; } .pk-paper td:first-child { width: 42%; color: #75726f; }
.pk-paper .sig { margin-top: 22px; display: flex; justify-content: space-between; gap: 18px; font-size: 13px; color: #75726f; }
.pk-empty { text-align: center; padding: 40px 20px; background: #fff; border-radius: 24px; box-shadow: var(--shadow-subtle); }
.pk-empty b { display: block; font-size: 17px; margin: 10px 0 4px; } .pk-empty p { color: #75726f; margin: 0; }
.pk-banner { border-radius: 16px; padding: 12px 16px; font-size: 14px; margin-bottom: 14px; }
.pk-banner.yellow { background: var(--color-marigold); } .pk-banner.gray { background: var(--color-cloud); }
.pk-bulk { background: var(--color-ink); color: #fff; border-radius: 9999px; padding: 10px 18px; font-weight: 600; font-size: 14px; display: inline-block; }
.pk-note { font-size: 13px; color: #75726f; margin-top: 8px; }
.pk-vitem { border-radius: 14px; padding: 10px 12px; background: var(--color-linen); }
.pk-vitem.y { background: var(--color-mint); }
"""


def svg_img(svg: str, alt: str = "", style: str = "") -> str:
    """SVG ditampilkan sebagai <img> data-URI (st.html menyaring tag <svg> mentah)."""
    import base64
    if "xmlns=" not in svg:
        svg = svg.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)
    b64 = base64.b64encode(svg.encode("utf-8")).decode()
    return f'<img src="data:image/svg+xml;base64,{b64}" alt="{esc(alt)}" style="{style}">'


def inject() -> None:
    st.html(f"<style>{CSS}</style>")


def tag(text: str, color: str = "gray") -> str:
    return f'<span class="pk-tag {color}">{esc(str(text))}</span>'


def tags(*items: tuple[str, str]) -> str:
    return '<div class="pk-tags">' + "".join(tag(t, c) for t, c in items) + "</div>"


def page_header(title: str, sub: str = "") -> None:
    st.html(f'<div><h1 class="pk-h1">{esc(title)}</h1>' + (f'<p class="pk-sub">{esc(sub)}</p>' if sub else "") + "</div>")


def empty(title: str, sub: str = "Ubah kata kunci atau filter, lalu coba lagi.") -> None:
    st.html(f'<div class="pk-empty">{_empty_svg()}<b>{esc(title)}</b><p>{esc(sub)}</p></div>')


def _empty_svg() -> str:
    return svg_img('<svg width="96" height="78" viewBox="0 0 96 78">'
            f'<path d="{_torn(10, 14, 70, 56, 7)}" fill="#fde99b"/>'
            '<rect x="22" y="8" width="56" height="62" rx="8" fill="#fff" stroke="#030302" stroke-width="2"/>'
            '<path d="M32 26h36M32 38h28M32 50h18" stroke="#e1e1e1" stroke-width="5" stroke-linecap="round"/>'
            '<circle cx="70" cy="54" r="11" fill="#9bd8a9" stroke="#030302" stroke-width="2"/>'
            '<path d="M78 62l8 8" stroke="#030302" stroke-width="3" stroke-linecap="round"/></svg>', "", "width:96px;height:78px")


def _torn(x: float, y: float, w: float, h: float, seed: int, step: float = 7, amp: float = 3.2) -> str:
    """Path SVG persegi dengan tepi sobek (torn paper)."""
    r = random.Random(seed)
    pts = []
    n = max(3, int(w / step))
    for i in range(n + 1):
        pts.append((x + w * i / n, y + r.uniform(-amp, amp)))
    m = max(3, int(h / step))
    for i in range(1, m + 1):
        pts.append((x + w + r.uniform(-amp, amp), y + h * i / m))
    for i in range(n - 1, -1, -1):
        pts.append((x + w * i / n, y + h + r.uniform(-amp, amp)))
    for i in range(m - 1, 0, -1):
        pts.append((x + r.uniform(-amp, amp), y + h * i / m))
    return "M" + " L".join(f"{a:.1f} {b:.1f}" for a, b in pts) + " Z"


def hero(greet: str, when: str, text: str, chips: list[str], notes: list[str]) -> None:
    note_rows = "".join(
        f'<g transform="translate(0,{k * 30})"><rect x="250" y="{120}" width="14" height="14" rx="4" fill="none" stroke="#030302" stroke-width="1.6"/>'
        f'<text x="274" y="{132}" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#030302">{esc(n)}</text></g>'
        for k, n in enumerate([(t if len(t) <= 30 else t[:29] + "…") for t in notes[:3]]))
    svg = f'''<svg viewBox="0 0 520 330" width="520" height="330">
<path d="{_torn(20, 40, 230, 170, 3)}" fill="#9bd8a9"/>
<path d="{_torn(300, 10, 190, 120, 8)}" fill="#fde99b"/>
<path d="{_torn(60, 220, 210, 90, 11)}" fill="#b8caf5"/>
<g stroke="#030302" stroke-width="2.4" fill="none" stroke-linecap="round" stroke-linejoin="round">
<path d="M40 250 H300"/><path d="M60 250 V292 M140 250 V292 M220 250 V292 M290 250 V292"/>
<path d="M40 250 Q105 196 170 250 Q235 196 300 250"/>
{''.join(f'<path d="M{x} 250 V{250 - 26 + abs(x - (105 if x < 170 else 235)) * 0.42:.0f}"/>' for x in (75, 90, 105, 120, 135, 205, 220, 235, 250, 265))}
<path d="M120 40 V210"/><path d="M110 40 H230"/><path d="M110 40 L120 26 L130 40"/>
{''.join(f'<path d="M115 {y} L125 {y + 14}"/>' for y in range(52, 200, 18))}
<path d="M205 40 V96"/><rect x="194" y="96" width="22" height="16" rx="2" fill="#ff4500" stroke="#030302"/>
</g>
<g transform="rotate(-3 360 200)">
<rect x="236" y="88" width="268" height="150" rx="16" fill="#fff" stroke="#e1e1e1"/>
<rect x="236" y="88" width="268" height="6" rx="3" fill="#ff4500"/>
<text x="252" y="112" font-family="Georgia, serif" font-size="18" fill="#030302">Hari ini</text>
{note_rows}
</g>
</svg>'''
    chip_html = "".join(f"<span>{esc(c)}</span>" for c in chips)
    st.html(f'<section class="pk-hero"><div><div class="when">{esc(when)}</div><h1>{esc(greet)}</h1>'
            f'<p>{text}</p><div class="chips">{chip_html}</div></div>'
            f'{svg_img(svg, "Kolase proyek konstruksi", "width:100%;height:auto;max-height:300px")}</section>')


def kv(rows: list[tuple[str, str]]) -> str:
    return '<dl class="pk-kv">' + "".join(f"<div><dt>{esc(a)}</dt><dd>{esc(str(b))}</dd></div>" for a, b in rows) + "</dl>"


def steps(stage: int) -> str:
    out = []
    for k in range(1, 6):
        cls = "d" if stage > k else "c" if stage == k else ""
        out.append(f'<div class="{cls}">{k}. {esc(D.STG[k])}</div>')
    return '<div class="pk-steps">' + "".join(out) + "</div>"


_MARK = {"green": "✓", "red": "↺", "blue": "↑", "yellow": "!", "gray": "•"}


def timeline(items: list[dict]) -> str:
    out = []
    for it in items:
        c = it.get("c", "gray")
        out.append(f'<li><span class="dot {c}">{_MARK.get(c, "•")}</span>'
                   f'<div><span class="who">{esc(it["who"])}</span> · <span class="jab">{esc(it["jab"])}</span></div>'
                   f'<div class="pk-tags" style="margin-top:4px">{it.get("badge", "")}<span class="when">{esc(it["when"])}</span></div>'
                   + (f'<div class="nt">{esc(it["note"])}</div>' if it.get("note") else "") + "</li>")
    return '<ol class="pk-tl">' + "".join(out) + "</ol>"


def ring(score: int, color: str) -> str:
    col = {"green": "#2f9e57", "blue": "#5b7fd6", "yellow": "#e0b400", "red": "#ff4500"}.get(color, "#bebbba")
    dash = score / 100 * 314.16
    return svg_img(f'<svg width="124" height="124" viewBox="0 0 120 120">'
            '<circle cx="60" cy="60" r="50" fill="none" stroke="#efefef" stroke-width="12"/>'
            f'<circle cx="60" cy="60" r="50" fill="none" stroke="{col}" stroke-width="12" stroke-linecap="round" '
            f'stroke-dasharray="{dash:.1f} 314.16" transform="rotate(-90 60 60)"/>'
            f'<text x="60" y="71" text-anchor="middle" font-family="Georgia, serif" font-size="34" fill="#030302">{score}</text></svg>',
            f"Skor {score} dari 100", "width:124px;height:124px;flex:none")


def bars(rows: list[tuple[str, float, str, str]]) -> str:
    """rows: (label, persen 0-100, teks kanan, warna css)."""
    return '<div class="pk-bars">' + "".join(
        f'<div class="pk-bar"><div class="lab"><b>{esc(a)}</b><span>{esc(r)}</span></div>'
        f'<div class="tr"><i style="width:{p}%;background:{c}"></i></div></div>' for a, p, r, c in rows) + "</div>"


def paper(title: str, no: str, lines: list[tuple[str, str]], a: str, b: str) -> str:
    rows = "".join(f"<tr><td>{esc(k)}</td><td>: {esc(v)}</td></tr>" for k, v in lines)
    return (f'<div class="pk-paper"><h4>{esc(title.upper())}</h4><div class="c">Nomor: {esc(no)}</div>'
            f'<table>{rows}</table><div class="sig"><span>Pihak Pertama<br><br><br><b>{esc(a)}</b></span>'
            f'<span>Pihak Kedua<br><br><br><b>{esc(b)}</b></span></div></div>')


def plot_layout(fig, height=320):
    fig.update_layout(height=height, margin=dict(l=8, r=8, t=10, b=8), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", color="#030302", size=13),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), hoverlabel=dict(bgcolor="#fff"))
    fig.update_xaxes(showgrid=False, linecolor="#e1e1e1")
    fig.update_yaxes(gridcolor="#e1e1e1", zeroline=False)
    return fig
