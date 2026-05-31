from rest_framework import serializers
from .models import Evidence

class EvidenceUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = [
            "execution", "evidence_type", "file", 
            "latitude", "longitude", "accuracy_meters", "is_inside_geofence"
        ]