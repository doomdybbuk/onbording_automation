from PyPDF2 import PdfReader
from pdf2image import convert_from_path
import pytesseract

# Test PDF text extraction
file_path = "../media/JainManan_resumefinal.pdf"  # Replace with a valid PDF file path
reader = PdfReader(file_path)
text = ""
for page in reader.pages:
    text += page.extract_text()

print("Extracted Text from PDF (PyPDF2):")
print(text)

# Test OCR
if not text.strip():
    print("Switching to OCR for image-based PDF...")
    images = convert_from_path(file_path)
    for image in images:
        text += pytesseract.image_to_string(image)

print("Extracted Text with OCR:")
print(text)

# Test structured data extraction
data = extract_data_from_text(text)
print("Parsed Data:")
print(data)