import os
from openpyxl import Workbook, load_workbook
from pdf_extract import extract_7501_data

pdf_folder = "pdfs"
excel_file = "7501_tracker.xlsx"

if os.path.exists(excel_file):
    wb = load_workbook(excel_file)
    ws = wb.active
else:
    wb = Workbook()
    ws = wb.active
    ws.title = "7501 Tracker"
    ws.append(["File Name","Entry Number", "Summary Date","Entry Date","Port Code"])

for file_name in os.listdir(pdf_folder):
    if file_name.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder,file_name)

        data = extract_7501_data(pdf_path)

        ws.append(
            [
                file_name,
                data["Entry Number"],
                data["Summary Date"],
                data["Entry Date"],
                data["Port Code"]
            ]
        )
wb.save(excel_file)

print("Batch processing complete.")