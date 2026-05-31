from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import EvidenceUploadSerializer

class EvidenceUploadView(APIView):
    """
    Endpoint para envio de arquivos de evidência fotográfica e localização.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] # Permite upload de arquivos

    def post(self, request):
        # Injeta automaticamente o operador que coletou a evidência
        data = request.data.copy()
        
        serializer = EvidenceUploadSerializer(data=data)
        if serializer.is_valid():
            # Salva o vínculo com o operador autenticado
            serializer.save(collected_by=request.user)
            
            return Response({
                "detail": "Evidência enviada com sucesso.",
                "evidence_id": serializer.data["id"]
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)