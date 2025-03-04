import os
import cohere
import pandas as pd
import json
import PyPDF2
import docx
import time
import zipfile
import shutil
import tkinter as tk
from tkinter import filedialog

# Configure Cohere API
COHERE_API_KEY = "1reNTPSgdOla2Z2RGyf9UqgiDngIQP5cwie0fTAK"
co = cohere.Client(COHERE_API_KEY)

# Select ZIP File Using Tkinter
def select_zip_file():
    root = tk.Tk()
    root.withdraw()
    zip_file = filedialog.askopenfilename(title="Select ZIP File with Resumes", filetypes=[("ZIP files", "*.zip")])
    return zip_file

zip_file_path = select_zip_file()
print(f"Selected ZIP file: {zip_file_path}")

# Extract ZIP to Temporary Directory
def extract_zip(zip_path, extract_to="./temp_resumes"):
    if not os.path.exists(extract_to):
        os.makedirs(extract_to)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to

folder_name = extract_zip(zip_file_path)

# Function to Extract Text from Different File Types
def extract_text_from_file(file_path):
    text = ""
    file_ext = file_path.lower().split(".")[-1]
    try:
        if file_ext == "pdf":
            with open(file_path, "rb") as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        elif file_ext in ["doc", "docx"]:
            doc = docx.Document(file_path)
            text = "\n".join([para.text for para in doc.paragraphs])
        elif file_ext == "txt":
            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                text = file.read()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
    return text

# Function to Clean Email Address
def clean_email(email):
    if email.startswith("pe"):
        email = email[2:]  # Remove "pe" prefix
    return email

# Function to Extract Resume Data using Cohere
def extract_resume_details(resume_text):
    prompt = f"""
    Extract the following details from the resume and return as JSON:
    - Full Name
    - Email Address
    - Phone Number (Only extract one valid number)
    - Address 
    - Skills
    - Years of Experience
    - Education (Degree, University, CGPA)

    Resume Text:
    {resume_text}

    Return the extracted details in valid JSON format without any extra text.

    Example JSON format:
    {{
        "Full Name": "John Doe",
        "Email Address": "johndoe@example.com",
        "Phone Number": "+1234567890",
        "Address": "123 Main Street , City, Country",
        "Skills": ["Python", "Machine Learning", "Data Science"],
        "Years of Experience": "3 years",
        "Education": [
            {{
                "Degree": "B.Tech in Computer Science",
                "University": "XYZ University",
                "CGPA": "8.5"
            }}
        ]
    }}
    """

    try:
        response = co.chat(
            message=prompt,
            model="command-r-plus",
            temperature=0.2
        )
        print("AI Response:", response.text.strip())
        extracted_data = json.loads(response.text.strip())

        # Clean email if needed
        if "Email Address" in extracted_data:
            extracted_data["Email Address"] = clean_email(extracted_data["Email Address"])

        time.sleep(12)  # To avoid exceeding Cohere's rate limit
        return extracted_data
    except json.JSONDecodeError:
        print(f"JSON decoding failed for response: {response.text.strip()}")
        return {}
    except Exception as e:
        print(f"Error during AI extraction: {e}")
        return {}

# Process Multiple Resumes and Save to CSV
def process_resumes(folder_name, zip_file_path):
    if not os.path.exists(folder_name):
        print("Folder not found. Exiting...")
        return

    all_data = []

    for file_name in os.listdir(folder_name):
        file_path = os.path.join(folder_name, file_name)
        if file_name.lower().endswith(("pdf", "doc", "docx", "txt")):
            print(f"Processing: {file_name}")
            resume_text = extract_text_from_file(file_path)

            if resume_text.strip():
                print("Extracted Text Length:", len(resume_text))
                parsed_data = extract_resume_details(resume_text)

                if parsed_data:
                    parsed_data["File Name"] = file_name
                    print("Parsed Data:", parsed_data)
                    all_data.append(parsed_data)
                else:
                    print(f"Failed to extract valid data from {file_name}")
            else:
                print(f"No text extracted from {file_name}. Skipping...")

    if all_data:
        df = pd.DataFrame(all_data)
        output_folder = os.path.dirname(zip_file_path)
        csv_filename = os.path.join(output_folder, "extracted_resume_data.csv")
        df.to_csv(csv_filename, index=False)
        print(f"All resume data saved to '{csv_filename}'")
    else:
        print("No valid data extracted.")

# Run the Resume Processing
process_resumes(folder_name, zip_file_path)

# Clean up temporary directory
shutil.rmtree(folder_name)
