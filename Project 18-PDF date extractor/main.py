
import os
import re
from tkinter import filedialog, Tk
from pypdf import PdfReader
import openpyxl
from pathlib import Path
from datetime import datetime
import calendar

# -----------------------------
# Helpers
# -----------------------------
MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4,
    "may": 5, "jun": 6, "jul": 7, "aug": 8,
    "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

def normalise_date(raw):
    if not raw or raw == "Not found":
        return "Not found"

    raw = raw.strip()

    # MM/YYYY
    if re.fullmatch(r"\d{1,2}/\d{4}", raw):
        m, y = raw.split("/")
        return f"{y}-{int(m):02d}"

    # Month YYYY
    match = re.fullmatch(r"([A-Za-z]+)\s(\d{4})", raw)
    if match:
        month = MONTHS.get(match.group(1).lower()[:3])
        return f"{match.group(2)}-{month:02d}" if month else raw

    return raw


def expiry_status(expiry_ym):
    if expiry_ym in ("Not found", "", None):
        return "No expiry stated"

    y, m = map(int, expiry_ym.split("-"))
    last_day = calendar.monthrange(y, m)[1]
    expiry_date = datetime(y, m, last_day)

    today = datetime.today()

    if expiry_date < today:
        return "Expired"
    if (expiry_date - today).days <= 90:
        return "Expires soon"
    return "Valid"


# -----------------------------
# Detection logic
# -----------------------------
def detect_manufacturer(text, filename):
    text_u = (text + filename).upper()
    for brand in ["LAMINEX", "FORMICA", "HIMACS", "HI-MACS"]:
        if brand in text_u:
            return brand.replace("HI-MACS", "HIMACS")
    return "Unknown"


def detect_doc_type(text, filename):
    blob = (text + filename).upper()

    rules = {
        "Technical Data Sheet (TDS)": ["TECHNICAL DATA", "TDS"],
        "Safety Data Sheet (SDS)": ["SAFETY DATA", "SDS", "MSDS"],
        "Warranty": ["WARRANTY"],
        "Installation Guide": ["INSTALLATION", "FABRICATION"],
        "Test / Report / Certificate": ["TEST REPORT", "FIRE", "CERTIFICATE", "REPORT"],
        "Brochure / Flyer": ["BROCHURE", "FLYER"]
    }

    for doc_type, keys in rules.items():
        if any(k in blob for k in keys):
            return doc_type

    return "Other"


def extract_product_family(text):
    # Very lightweight heuristic — safe but useful
    match = re.search(r"Laminex\s+([A-Z][A-Za-z0-9\+\- ]{3,40})", text)
    return match.group(1).strip() if match else "Not identified"


def extract_version(text, filename):
    patterns = [
        r"Version\s*([A-Z0-9\.]+)",
        r"\bV([0-9]+)\b",
        r"Rev(?:ision)?\s*([A-Z0-9\.]+)"
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            return m.group(1)

    fm = re.search(r"V([0-9]+)", filename, re.IGNORECASE)
    return fm.group(1) if fm else "Not found"


def extract_issue(text):
    m = re.search(r"Issued\s*:?\s*([A-Za-z]+\s\d{4}|\d{1,2}/\d{4})", text, re.IGNORECASE)
    return normalise_date(m.group(1)) if m else "Not found"


def extract_expiry(text):
    m = re.search(r"Expiry\s*:?\s*([A-Za-z]+\s\d{4}|\d{1,2}/\d{4})", text, re.IGNORECASE)
    return normalise_date(m.group(1)) if m else "Not found"


# -----------------------------
# Folder picker
# -----------------------------
root = Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="Select PDF Folder")

# -----------------------------
# Excel setup
# -----------------------------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Laminex Document Register"
ws.append([
    "Filename",
    "Manufacturer",
    "Product Family",
    "Document Type",
    "Version",
    "Issue Date (YYYY-MM)",
    "Expiry Date (YYYY-MM)",
    "Expiry Status",
])

# -----------------------------
# Process PDFs
# -----------------------------
for filename in sorted(f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")):
    filepath = Path(folder_path) / filename
    print(f"Processing {filename}")

    try:
        reader = PdfReader(filepath)
        text = "".join(page.extract_text() or "" for page in reader.pages[:2])

        manufacturer = detect_manufacturer(text, filename)
        doc_type = detect_doc_type(text, filename)
        product = extract_product_family(text)
        version = extract_version(text, filename)
        issue = extract_issue(text)
        expiry = extract_expiry(text)
        status = expiry_status(expiry)

        ws.append([
            filename,
            manufacturer,
            product,
            doc_type,
            version,
            issue,
            expiry,
            status
        ])

        print("  ✅ Done")

    except Exception as e:
        ws.append([filename, "Error", "Error", "Error", "Error", "Error", "Error", "Error"])
        print(f"  ❌ {e}")

# -----------------------------
# Save
# -----------------------------
output = Path(folder_path) / "laminex_document_register.xlsx"
wb.save(output)
print(f"\n✅ Saved to {output}")
