from .models import UploadedForm, CandidateRecord
from .utils import extract_text_from_pdf, extract_data_from_text

def process_uploaded_form(form_id):
    """
    Process the uploaded form:
    - Extract text from the uploaded PDF.
    - Parse structured data and save it to the database.
    """
    try:
        form = UploadedForm.objects.get(id=form_id)
        file_path = form.file.path
        print(f"Processing Form ID {form_id}, File Path: {file_path}")

        # Extract text from the PDF
        text = extract_text_from_pdf(file_path)
        print("Extracted Text:", text)

        # Extract structured data
        data = extract_data_from_text(text)
        print("Parsed Data:", data)

        # Validate and create CandidateRecord
        if data:
            data.setdefault("name", "Unknown")
            data.setdefault("email", "unknown@example.com")
            data.setdefault("phone", "N/A")
            data.setdefault("address", "N/A")
            data.setdefault("resume_link", file_path)

            candidate = CandidateRecord.objects.create(**data)
            print(f"Candidate Created: {candidate}")

            # Update UploadedForm
            form.candidate = candidate
            form.processed = True
            form.save()
            print(f"Form ID {form_id} processed successfully.")
        else:
            print(f"No data extracted from Form ID {form_id}")

    except UploadedForm.DoesNotExist:
        print(f"Error: UploadedForm with ID {form_id} not found.")
    except Exception as e:
        print(f"Error processing form ID {form_id}: {str(e)}")
