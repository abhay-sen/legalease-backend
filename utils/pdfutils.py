from pdf2image import convert_from_path
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import pdfplumber
import os

def extract_text_from_pdf(file_path):
    try:
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

        if not text.strip():
            # Manually specify Poppler path for Windows
            poppler_path = r"C:\poppler\Release-24.08.0-0\poppler-24.08.0\Library\bin"  # <-- update to your actual path

            images = convert_from_path(file_path, poppler_path=poppler_path)
            for img in images:
                text += pytesseract.image_to_string(img)

        return text.strip()

    except Exception as e:
        return f"[ERROR]: {str(e)}"
