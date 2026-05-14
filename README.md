# Supply Chain Delay Dashboard

## Overview

This project analyzes shipment data to identify delay patterns and carrier performance using Python and Streamlit.

## Features

* Calculate shipment delay days using ETA vs. ATA
* Track severe delay rate for shipments delayed more than 3 days
* Compare average delay across carriers
* Explore results through an interactive Streamlit dashboard

## ⚠️ Advanced Features

- Context-aware AI insights (selected vs overall performance)
- Anomaly detection using statistical threshold (mean + 2σ)
- AI explanation of operational risks based on anomalies
## Key Insights

* About 18% of shipments fall into the severe delay category
* COSCO shows the highest average delay in the sample analysis
* Delay performance varies by carrier

## 📄 Document Automation Features

- Extract structured data from CBP Form 7501 PDFs
- Parse entry numbers, summary dates, entry dates, and port codes using regex
- Convert unstructured customs documents into structured Python dictionaries
- Automatically append extracted shipment records into Excel tracker
- Support reusable PDF-to-Excel workflow automation

## 🔄 Batch Processing Workflow

- Process multiple CBP Form 7501 PDFs automatically
- Extract structured shipment data from each document
- Append extracted records into centralized Excel tracker
- Support scalable PDF-to-Excel operational workflow

## Tech Stack

* Python
* pandas
* Streamlit
* pdfplumber
* openpyxl
* regex(re)

## Data Note

The original business dataset is not included in this repository for confidentiality reasons. This project is shared as a public portfolio example without proprietary company data.

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

