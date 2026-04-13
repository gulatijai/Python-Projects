import os
import re
from tkinter import filedialog, Tk
from pypdf import PdfReader
import openpyxl

# folder picker
root = Tk()
root.withdraw()
folder_path = filedialog.askdirectory(title="Select PDF Folder")

# setup Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.append(['Filename', 'Document Name', 'Test Number', 'Version', 'Issue Date', 'Expiry Date'])

# regex patterns for dates and versions
date_patterns = [
    r'\d{1,2}\s(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}',  # 01 Sep 2023
    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s\d{4}',            # Sep 2023
    r'\d{1,2}/\d{4}',                                                          # 03/2021
    r'\d{1,2}/\d{1,2}/\d{4}',                                                 # 01/09/2023
    r'\d{4}-\d{2}-\d{2}',                                                     # 2023-09-01
]

version_pattern = r'[Vv]ersion\s*[\d\.]+|[Vv]\s*[\d\.]+'

issue_keywords = ['issued', 'issue date', 'date issued', 'published']
expiry_keywords = ['expiry', 'expires', 'expiration', 'valid until']

def find_dates(text):
    found_dates = []
    for pattern in date_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        found_dates.extend(matches)
    return found_dates

def find_issue_date(text):
    lines = text.lower().split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in issue_keywords):
            # search this line and next line for dates
            search_text = line + ' ' + (lines[i+1] if i+1 < len(lines) else '')
            dates = find_dates(search_text)
            if dates:
                return dates[0]
    return 'Not found'

def find_expiry_date(text):
    lines = text.lower().split('\n')
    for i, line in enumerate(lines):
        if any(keyword in line for keyword in expiry_keywords):
            search_text = line + ' ' + (lines[i+1] if i+1 < len(lines) else '')
            dates = find_dates(search_text)
            if dates:
                return dates[0]
    return 'Not found'

def find_version(text):
    match = re.search(version_pattern, text, re.IGNORECASE)
    return match.group(0) if match else 'Not found'

def find_doc_name(text):
    # look for common document title patterns
    title_keywords = ['TEST REPORT', 'TECHNICAL DATA', 'INSTALLATION GUIDE',
                      'WARRANTY', 'CARE AND MAINTENANCE', 'MATERIAL SAFETY']
    text_upper = text.upper()
    for keyword in title_keywords:
        if keyword in text_upper:
            return keyword
    # fallback to first non-empty line
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return lines[0] if lines else 'Not found'

def find_test_number(text):
    match = re.search(r'Test(?:ing)?\s*Number\s*:?\s*(\S+)', text, re.IGNORECASE)
    return match.group(1) if match else 'Not found'

# process all PDFs
pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
print(f"Found {len(pdf_files)} PDF files")

for filename in pdf_files:
    print(f"Processing: {filename}")
    try:
        filepath = os.path.join(folder_path, filename)
        reader = PdfReader(filepath)

        # extract text from first 2 pages only
        text = ""
        for page in reader.pages[:2]:
            text += page.extract_text() or ""

        # extract data
        doc_name = find_doc_name(text)
        version = find_version(text)
        issue_date = find_issue_date(text)
        expiry_date = find_expiry_date(text)

        test_number = find_test_number(text)
        ws.append([filename, doc_name, test_number, version, issue_date, expiry_date])
        print(f"  ✅ Done")

    except Exception as e:
        print(f"  ❌ Error: {e}")
        ws.append([filename, 'Error', 'Error', 'Error', 'Error'])

# save Excel
output_path = os.path.join(folder_path, 'pdf_dates.xlsx')
wb.save(output_path)
print(f"Saved to {output_path}")