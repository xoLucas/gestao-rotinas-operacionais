from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# Importamos a Company também
from apps.organizations.models import Company, Station
from apps.operations.models import OperationalArea
from apps.routines.models import Routine
from apps.scheduling.models import Shift
from apps.execution.models import WorkSession, RoutineExecution

User = get_user_model()

class EvidenceAPITests(APITestCase):
    def setUp(self):
        # 1. Cria o usuário autenticado
        self.user = User.objects.create_user(username='operador_foto', password='password123')
        self.upload_url = reverse('evidence-upload')

        # 2. Prepara o banco de dados temporário com os cadastros básicos
        # Criamos a Company primeiro para satisfazer a restrição do banco
        self.company = Company.objects.create(name="Seacrest Teste")
        
        # Agora passamos a company na criação da Station
        self.station = Station.objects.create(code="TST", name="Estação Teste", company=self.company)
        
        self.area = OperationalArea.objects.create(name="Área Teste", station=self.station)
        
        self.shift = Shift.objects.create(
            name="Turno Teste", 
            start_time="07:00:00", 
            end_time="19:00:00", 
            station=self.station
        )
        
        self.routine = Routine.objects.create(
            name="Rotina Teste", 
            category="operational_routine", 
            criticality="low",
            station=self.station,
            area=self.area
        )
        
        self.session = WorkSession.objects.create(operator=self.user, shift=self.shift)
        
        # 3. Cria a execução que utilizaremos no teste
        self.execution = RoutineExecution.objects.create(
            work_session=self.session, 
            routine=self.routine, 
            status="pending"
        )

    def test_evidence_upload_missing_file_for_photo(self):
        """Garante que enviar uma evidência tipo 'photo' sem ficheiro falha devido à nossa validação."""
        self.client.force_authenticate(user=self.user)
        
        # Passamos o ID real da execução que acabamos de criar dinamicamente
        payload = {
            "execution": self.execution.id,
            "evidence_type": "photo",
            "is_inside_geofence": True
        }
        
        response = self.client.post(self.upload_url, payload, format='multipart')
        
        # Agora a validação de Chave Estrangeira vai passar, e o sistema vai bater 
        # exatamente na nossa regra de ausência de imagem (file)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file', response.data)