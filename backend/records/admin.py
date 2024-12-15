from django.contrib import admin
from .models import CandidateRecord, UploadedForm

# Register your models here
@admin.register(CandidateRecord)
class CandidateRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'address', 'resume_link', 'created_at')
    search_fields = ('name', 'email')

@admin.register(UploadedForm)
class UploadedFormAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'processed', 'candidate', 'uploaded_at')
    search_fields = ('candidate__name',)
    list_filter = ('processed', 'uploaded_at')
