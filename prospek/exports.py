"""Ekspor laporan ke CSV, Excel dan PDF, serta template import rekanan."""
from __future__ import annotations

import io

import pandas as pd
from fpdf import FPDF

from . import data as D


def vendor_frame(L: list[dict]) -> pd.DataFrame:
    return pd.DataFrame([{
        "ID Vendor": v["id"], "Nama Perusahaan": v["nama"], "Kontak": v["kontak"], "Email": v["email"],
        "NPWP": v["npwp"], "ID SAP": v["sap_id"] or "-", "Status SAP": "Synced" if v["sap"] else "Pending",
        "Tahapan": v["tahap"], "Verifikasi": f"{sum(v['verif'])}/4", "Divisi": v["divisi"],
        "Bidang Usaha": v["bidang"], "Wilayah": v["wilayah"], "Kualifikasi": v["kual"],
        "Akses Edit": "Locked" if v["locked"] else "Unlocked", "Tgl Registrasi": D.fdate(v["reg"]),
    } for v in L])


def invoice_frame(L: list[dict], V: list[dict]) -> pd.DataFrame:
    return pd.DataFrame([{
        "No. BAP": x["no"], "Kontrak": x["ktr"], "Rekanan": V[x["vi"]]["nama"], "Pekerjaan": x["pek"],
        "Proyek": x["proj"], "Divisi": x["div"], "Jenis": x["jenis"], "Nilai (Rp)": x["nilai"],
        "Tahap": D.stage_name(x), "SLA": D.sla(x)[0], "Hari di Tahap": x["hari"],
    } for x in L])


def to_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8-sig")


def to_xlsx(df: pd.DataFrame, sheet: str = "Data") -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as xw:
        df.to_excel(xw, index=False, sheet_name=sheet)
        ws = xw.sheets[sheet]
        from openpyxl.styles import Font, PatternFill
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="030302")
        for col in ws.columns:
            w = max(len(str(c.value or "")) for c in col)
            ws.column_dimensions[col[0].column_letter].width = min(max(10, w + 2), 48)
        ws.freeze_panes = "A2"
    return buf.getvalue()


_MAP = str.maketrans({"–": "-", "—": "-", "×": "x", "²": "2", "³": "3", "→": "->", "’": "'", "“": '"', "”": '"', "…": "..."})


def _t(s) -> str:
    return str(s).translate(_MAP).encode("latin-1", "replace").decode("latin-1")


def to_pdf(df: pd.DataFrame, title: str) -> bytes:
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(True, 12)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 9, _t(f"PROSPEK · {title}"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 6, _t(f"Dicetak {D.fdt(D.now())} oleh {D.USER['nama']} ({D.USER['jabatan']}) · data contoh"),
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    cols = list(df.columns)
    lens = [max(len(_t(c)), *(len(_t(v)) for v in df[c])) if len(df) else len(c) for c in cols]
    total = sum(min(l, 40) for l in lens) or 1
    widths = [277 * min(l, 40) / total for l in lens]
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_fill_color(3, 3, 2)
    pdf.set_text_color(255, 255, 255)
    for c, w in zip(cols, widths):
        pdf.cell(w, 7, _t(c)[: int(w / 1.6)], border=0, fill=True)
    pdf.ln()
    pdf.set_text_color(3, 3, 2)
    pdf.set_font("Helvetica", "", 7.5)
    for k, (_, row) in enumerate(df.iterrows()):
        pdf.set_fill_color(255, 243, 231) if k % 2 else pdf.set_fill_color(255, 255, 255)
        for c, w in zip(cols, widths):
            v = row[c]
            s = D.rp(v) if c.startswith("Nilai") and isinstance(v, (int, float)) else _t(v)
            pdf.cell(w, 6.5, _t(s)[: int(w / 1.5)], border=0, fill=True)
        pdf.ln()
    return bytes(pdf.output())


TEMPLATE_COLS = ["nama_perusahaan", "email", "kontak", "npwp", "bidang_usaha", "wilayah", "kualifikasi", "divisi"]


def template_xlsx() -> bytes:
    df = pd.DataFrame([["PT Contoh Konstruksi", "admin@contoh.co.id", "Andi", "16.789.012.3-111.000",
                        "Pekerjaan Beton", "Jawa", "Menengah", "Divisi Gedung"]], columns=TEMPLATE_COLS)
    return to_xlsx(df, "Template Rekanan")


def read_import(file) -> pd.DataFrame:
    name = file.name.lower()
    df = pd.read_csv(file) if name.endswith(".csv") else pd.read_excel(file)
    df.columns = [str(c).strip().lower() for c in df.columns]
    missing = [c for c in ("nama_perusahaan", "email") if c not in df.columns]
    if missing:
        raise ValueError("Kolom wajib tidak ditemukan: " + ", ".join(missing))
    return df.fillna("")
