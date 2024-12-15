from django.db import models

# Create your models here.
class CandidateRecord(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    resume_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class UploadedForm(models.Model):
    file = models.FileField(upload_to="forms/")
    processed = models.BooleanField(default=False)
    candidate = models.ForeignKey(CandidateRecord, on_delete=models.SET_NULL, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)