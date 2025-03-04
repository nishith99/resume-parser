Resume Parser using Cohere API

Project Overview
A Python-based resume parser that extracts key information (Name, Email, Phone Number, Address, Skills, Experience, and Education) from resumes in PDF, DOCX, DOC, and TXT formats. It leverages the Cohere command-r-plus model for accurate information extraction and outputs the results in a structured CSV file.

Features
- Supports resume extraction from PDF, DOC, DOCX, and TXT files.
- Extracts:
  - Full Name
  - Email Address
  - Phone Number
  - Address
  - Skills
  - Years of Experience
  - Education (Degree, University, CGPA)
- Bulk processing from ZIP archives.
- Outputs extracted data in CSV format.
- Automatically cleans up temporary directories after processing.

Project Structure
resume-parser/
├── main.py              # Main script for resume parsing
├── README.md            # Project documentation
├── requirements.txt     # Python dependencies
└── temp_resumes/        # Temporary directory for extracted files (auto-cleaned)

Installation

1. Clone the repository:

   git clone https://github.com/nishith99/resume-parser.git
   cd resume-parser

2. Create and activate a virtual environment (optional but recommended):

   # On Linux/macOS
   python -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   venv\Scripts\activate

3. Install required packages:

   pip install -r requirements.txt

4. Set your Cohere API key:

   Replace the placeholder API key in the script:

   COHERE_API_KEY = "your-cohere-api-key"

Usage

1. Run the script and select a ZIP file containing resumes:

   python main.py

2. The extracted data will be saved as a CSV file in the same directory as the ZIP file.

Example Output
extracted_resume_data.csv

Output CSV Format
The output CSV will contain the following columns:

- Full Name
- Email Address
- Phone Number
- Address
- Skills (as a list)
- Years of Experience
- Education (Degree, University, CGPA)
- File Name

How It Works

1. File Selection: Opens a Tkinter dialog to select a ZIP file.
2. Extract ZIP: Unzips the contents to a temporary directory.
3. Text Extraction: Extracts text from PDF, DOC, DOCX, or TXT.
4. AI Extraction: Sends resume content to Cohere API (command-r-plus model) for structured data extraction.
5. Save to CSV: Outputs extracted details to a CSV file.
6. Clean Up: Deletes temporary files after processing.

Troubleshooting

1. Empty CSV: Ensure the resumes contain readable text (OCR not supported for image PDFs).
2. API Errors: Verify the Cohere API key is valid and ensure the rate limit is not exceeded.

Customization

- Modify fields to extract in the extract_resume_details function.
- Adjust the Cohere model or temperature settings for better performance.

Future Improvements

- Support for OCR (image-based PDF parsing).
- Enhanced error handling and logging.
- Multi-threading for faster resume processing.

License

This project is licensed under the MIT License.

Acknowledgments

- Cohere for their powerful language models.s
