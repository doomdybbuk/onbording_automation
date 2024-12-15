from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract
import re
import spacy

# Load spaCy model (use a pre-trained English model)
nlp = spacy.load("en_core_web_sm")

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    Handles both text-based and image-based PDFs.
    """
    text = ""

    try:
        # Try extracting text from text-based PDF
        pdf_reader = PdfReader(file_path)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text()
    except Exception as e:
        print(f"Error reading text-based PDF: {e}")

    if not text.strip():  # If no text extracted, use OCR
        print("Switching to OCR for image-based PDF...")
        try:
            images = convert_from_path(file_path)
            for image in images:
                text += pytesseract.image_to_string(image)
        except Exception as e:
            print(f"Error during OCR: {e}")

    return text.strip()

def extract_data_from_text(text):
    """
    Extract structured data (e.g., name, email, phone) from text using NLP.
    """
    data = {}

    # Use spaCy for named entity recognition
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "PERSON" and "name" not in data:
            data["name"] = ent.text
        elif ent.label_ == "GPE" and "address" not in data:
            data["address"] = ent.text

    # Extract email using regex
    email_match = re.search(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", text)
    data["email"] = email_match.group(0) if email_match else None

    # Extract phone number using regex
    phone_match = re.search(r"\b\d{10}\b", text)
    data["phone"] = phone_match.group(0) if phone_match else None

    return data
