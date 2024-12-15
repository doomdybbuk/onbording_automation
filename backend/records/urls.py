from django.urls import path
from .views import UploadFormView, CandidateListView, CandidateDetailView

urlpatterns = [
    path("upload-form/", UploadFormView.as_view(), name="upload-form"),  # Class-based view
    path("candidates/", CandidateListView.as_view(), name="candidate-list"),
    path("candidates/<int:id>/", CandidateDetailView.as_view(), name="candidate-detail"),
]
