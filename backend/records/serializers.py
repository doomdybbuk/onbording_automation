from rest_framework import serializers
from .models import CandidateRecord, UploadedForm

class CandidateRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateRecord
        fields = "__all__"

class UploadedFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedForm
        fields = ["id", "file", "processed", "candidate", "uploaded_at"]
        read_only_fields = ["processed", "candidate"]
