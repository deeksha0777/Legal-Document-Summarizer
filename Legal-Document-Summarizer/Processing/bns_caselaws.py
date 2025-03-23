import pdfplumber
import json
import os
import re

def extract_case_summary(pdf_path):
    """Extracts case title, date, court, and summary from a single PDF."""
    case_data = {
        "case_title": "",
        "date_of_decision": "",
        "court": "",
        "summary": ""
    }

    with pdfplumber.open(pdf_path) as pdf:
        text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])

    lines = text.split("\n")

    for i, line in enumerate(lines):
        # Extract case title
        if "vs" in line and "State" in line:
            case_data["case_title"] = line.strip()

        # Extract date of decision using regex
        date_match = re.search(r"(\d{1,2} \w+ \d{4})", line)
        if "Date of decision:" in line or date_match:
            case_data["date_of_decision"] = date_match.group(1) if date_match else line.split(":")[1].strip()

        # Extract court name
        if "HIGH COURT" in line or "COURT" in line:
            case_data["court"] = line.strip()

        # Extract summary based on keywords
        if any(keyword in line.lower() for keyword in ["summary", "facts", "court decision", "held that"]):
            case_data["summary"] = lines[i+1].strip() if i+1 < len(lines) else ""

    return case_data

def process_multiple_pdfs(pdf_folder, output_json):
    """Processes all PDFs in a folder and saves results in a JSON file."""
    all_cases = []
    
    for file in os.listdir(pdf_folder):
        if file.upper().endswith(".PDF"):
            pdf_path = os.path.join(pdf_folder, file)
            print(f"📄 Processing: {file}")
            case_data = extract_case_summary(pdf_path)
            
            all_cases.append(case_data)

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(all_cases, f, ensure_ascii=False, indent=4)

    print(f"\n✅ Processed {len(all_cases)} PDFs. Data saved in {output_json}")

# 🔹 Example Usage
pdf_folder_path = r"C:\Users\hp\Documents\BNS PDF"  # Folder where PDFs are stored
output_json_file = "cases_summary.json"

process_multiple_pdfs(pdf_folder_path, output_json_file)
