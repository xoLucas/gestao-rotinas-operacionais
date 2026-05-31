from rest_framework import serializers
from .models import Evidence

class EvidenceUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evidence
        fields = [
            "execution", "evidence_type", "file", 
            "latitude", "longitude", "accuracy_meters", "is_inside_geofence"
        ]

    def validate(self, data):
        # Regra: Se o tipo de evidência for 'photo', o ficheiro 'file' é obrigatório
        if data.get('evidence_type') == Evidence.EvidenceType.PHOTO and not data.get('file'):
            raise serializers.ValidationError({
                "file": "É obrigatório enviar o ficheiro da imagem quando o tipo de evidência é 'photo'."
            })
        return data