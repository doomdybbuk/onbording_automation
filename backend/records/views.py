from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .models import CandidateRecord, UploadedForm
from .tasks import process_uploaded_form


# View to handle file upload and render upload form page
class UploadFormView(View):
    def get(self, request):
        return render(request, "uploadform.html")

    def post(self, request):
        try:
            uploaded_files = request.FILES.getlist('files')
            if not uploaded_files:
                return render(request, "uploadform.html", {"error": "No files were uploaded."})
            
            uploaded_forms = []  # To store UploadedForm instances

            # Save files and trigger processing
            for file in uploaded_files:
                uploaded_form = UploadedForm.objects.create(file=file)
                uploaded_forms.append(uploaded_form)  # Append to list
                process_uploaded_form(uploaded_form.id)  # Direct processing (sync)

            # Prepare links for uploaded files
            uploaded_files_links = [
                {"file_name": form.file.name, "file_url": form.file.url}
                for form in uploaded_forms
            ]

            # URL for candidate list
            candidate_list_url = reverse_lazy("candidate-list")

            # Debugging
            print("Uploaded Files Links:", uploaded_files_links)
            print("Candidate List URL:", candidate_list_url)

            # Context for rendering the page
            context = {
                "message": "Files uploaded successfully.",
                "uploaded_files_links": uploaded_files_links,
                "candidate_list_url": candidate_list_url,
            }
            return render(request, "uploadform.html", context)

        except Exception as e:
            print("Error:", str(e))  # Debugging
            return render(request, "uploadform.html", {"error": str(e)})


# View to render the candidate list with pagination and filtering
class CandidateListView(View):
    def get(self, request):
        name = request.GET.get("name")
        email = request.GET.get("email")
        page = request.GET.get("page", 1)

        candidates = CandidateRecord.objects.all()
        if name:
            candidates = candidates.filter(name__icontains=name)
        if email:
            candidates = candidates.filter(email__icontains=email)

        # Pagination setup (10 records per page)
        paginator = Paginator(candidates, 10)
        paginated_candidates = paginator.get_page(page)

        return render(request, "record_list.html", {
            "candidates": paginated_candidates,
            "name": name,
            "email": email
        })


# View to render candidate details
class CandidateDetailView(View):
    def get(self, request, id):
        candidate = get_object_or_404(CandidateRecord, id=id)
        return render(request, "record_detail.html", {"candidate": candidate})
