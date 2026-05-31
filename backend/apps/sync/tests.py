from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class SyncAPITests(APITestCase):
    def setUp(self):
        # Criar um utilizador de teste
        self.user = User.objects.create_user(username='operador_teste', password='password123')
        # Obter a URL do endpoint de upload
        self.upload_url = reverse('sync-upload')

    def test_sync_upload_requires_authentication(self):
        """Garante que utilizadores não autenticados recebam erro 401"""
        response = self.client.post(self.upload_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sync_upload_validation_error(self):
        """Garante que a nossa validação (completed sem data) bloqueia o payload"""
        # Autenticar o cliente de teste
        self.client.force_authenticate(user=self.user)
        
        # Payload com erro propositado (status completed, mas sem completed_at)
        payload = {
            "executions": [
                {
                    "id": 1,
                    "status": "completed",
                    "has_abnormality": False
                }
            ]
        }
        
        response = self.client.post(self.upload_url, payload, format='json')
        
        # Esperamos um erro 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # O erro deve estar dentro do array de execuções
        self.assertIn('completed_at', str(response.data))

    def test_sync_upload_empty_payload(self):
        """Garante que enviar um payload vazio retorna erro"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.upload_url, {"executions": []}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)