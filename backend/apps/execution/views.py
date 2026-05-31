from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.utils import timezone

from .models import WorkSession
from .serializers import WorkSessionSerializer, RoutineExecutionSerializer
from apps.scheduling.models import Shift
from apps.scheduling.services import generate_executions_for_work_session

class StartWorkSessionView(APIView):
    """
    Endpoint para iniciar o turno. Cria a sessão de trabalho e gera 
    as execuções de rotinas baseadas nas regras de agendamento do turno.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        
        # 1. Obter dados do payload (turno, aparelho, gps)
        shift_id = request.data.get("shift")
        device_id = request.data.get("device_id", "")
        start_latitude = request.data.get("start_latitude")
        start_longitude = request.data.get("start_longitude")

        if not shift_id:
            return Response({"detail": "O campo 'shift' (turno) é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            shift = Shift.objects.get(id=shift_id, is_active=True)
        except Shift.DoesNotExist:
            return Response({"detail": "Turno não encontrado ou inativo."}, status=status.HTTP_404_NOT_FOUND)

        # Opcional: Impedir que inicie um turno se já existir um aberto
        active_session = WorkSession.objects.filter(operator=user, ended_at__isnull=True).first()
        if active_session:
            return Response({
                "detail": "Você já possui um turno em andamento.",
                "work_session": WorkSessionSerializer(active_session).data
            }, status=status.HTTP_400_BAD_REQUEST)

        # 2. Criar a sessão de trabalho (WorkSession)
        work_session = WorkSession.objects.create(
            operator=user,
            shift=shift,
            device_id=device_id,
            start_latitude=start_latitude,
            start_longitude=start_longitude,
        )

        # 3. Gerar a agenda de execuções usando o seu serviço
        created_executions = generate_executions_for_work_session(work_session)

        # 4. Retornar os dados
        return Response({
            "detail": "Turno iniciado com sucesso.",
            "work_session": WorkSessionSerializer(work_session).data,
            "agenda": RoutineExecutionSerializer(created_executions, many=True).data
        }, status=status.HTTP_201_CREATED)