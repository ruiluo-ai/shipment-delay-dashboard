import pdfplumber
import re

def extract_7501_data(pdf_path):
    text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    #print(text)
    text = text.upper().replace("\n"," ")

    data = {}

    entry_match = re.search(r"\b[A-Z0-9]{3}-\d{7}-\d\b",text)

    if entry_match:
        data["Entry Number"] = entry_match.group()
    else:
        data["Entry Number"] = None

    summary_data_match = re.search(r"3\. SUMMARY DATE.*?(\d{2}/\d{2}/\d{2})",text)
    if summary_data_match:
        data["Summary Date"] = summary_data_match.group(1)
    else:
        data["Summary Date"] = None

    entry_date_match = re.search(r"7\. ENTRY DATE.*?(\d{2}/\d{2}/\d{2})", text)
    if entry_date_match:
        data["Entry Date"] = entry_date_match.group(1)
    else:
        data["Entry Date"] = None

    port_match = re.search(r"6\. PORT CODE.*?(\d{4})",text)
    if port_match:
        data["Port Code"] = port_match.group(1)
    else:
        data["Port Code"] = None

    return data

result = extract_7501_data("8SP-0066153-9-Corrected(Air-Shipment).pdf")
print(result)
