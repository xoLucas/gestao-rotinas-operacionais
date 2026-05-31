from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.db import transaction

from apps.operations.models import OperationalArea, Asset
from apps.routines.models import Routine
from apps.scheduling.models import Shift, ScheduleRule
from apps.execution.models import RoutineExecution, ExecutionStepResult

from .serializers import (
    OperationalAreaSerializer,
    AssetSerializer,
    RoutineSerializer,
    ShiftSerializer,
    ScheduleRuleSerializer,
    SyncExecutionSerializer,
)

class SyncInitialView(APIView):
    """
    Endpoint responsável por enviar a carga inicial de dados (offline-first)
    para o aplicativo mobile, filtrando pela Estação do operador.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        # 1. Identificar a estação do operador logado
        try:
            # Navegação pelas FKs: User -> OperatorProfile -> Team -> Sector -> Station
            station = user.operator_profile.team.sector.station
        except AttributeError:
            return Response(
                {"detail": "Operador não possui um perfil, equipe ou estação vinculada."},
                status=400
            )

        # 2. Buscar os dados ativos vinculados àquela estação
        areas = OperationalArea.objects.filter(station=station, is_active=True)
        assets = Asset.objects.filter(area__station=station, is_active=True)
        
        # Usamos prefetch_related para otimizar a query, já que os steps estão aninhados no serializer
        routines = Routine.objects.filter(station=station, is_active=True).prefetch_related("steps")
        
        shifts = Shift.objects.filter(station=station, is_active=True)
        rules = ScheduleRule.objects.filter(routine__station=station, is_active=True)

        # 3. Serializar tudo em um único payload de resposta
        data = {
            "station": {
                "id": station.id,
                "code": station.code,
                "name": station.name,
            },
            "areas": OperationalAreaSerializer(areas, many=True).data,
            "assets": AssetSerializer(assets, many=True).data,
            "routines": RoutineSerializer(routines, many=True).data,
            "shifts": ShiftSerializer(shifts, many=True).data,
            "schedule_rules": ScheduleRuleSerializer(rules, many=True).data,
        }

        return Response(data)
    
class SyncUploadView(APIView):
    """
    Recebe os dados executados offline pelo mobile e atualiza o banco central.
    """
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user
        
        # O mobile deve enviar {"executions": [{...}, {...}]}
        executions_data = request.data.get("executions", [])
        
        if not executions_data:
            return Response({"detail": "Nenhum dado de execução enviado."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SyncExecutionSerializer(data=executions_data, many=True)
        serializer.is_valid(raise_exception=True)

        updated_count = 0

        for exec_data in serializer.validated_data:
            try:
                # Busca a execução agendada anteriormente para o operador
                execution = RoutineExecution.objects.select_for_update().get(
                    id=exec_data["id"], 
                    work_session__operator=user
                )
                
                # Atualiza os dados da execução principal
                execution.status = exec_data["status"]
                execution.started_at = exec_data.get("started_at")
                execution.completed_at = exec_data.get("completed_at")
                execution.observation = exec_data.get("observation", "")
                execution.outside_geofence_justification = exec_data.get("outside_geofence_justification", "")
                execution.has_abnormality = exec_data.get("has_abnormality", False)
                execution.save()

                # Processa os resultados de cada etapa (checklist)
                steps_data = exec_data.get("steps", [])
                for step_data in steps_data:
                    ExecutionStepResult.objects.update_or_create(
                        execution=execution,
                        step_id=step_data["step_id"],
                        defaults={
                            "is_completed": step_data["is_completed"],
                            "observation": step_data.get("observation", ""),
                            "value": step_data.get("value", ""),
                            "completed_at": execution.completed_at # Sincroniza com o fim da rotina
                        }
                    )
                
                updated_count += 1

            except RoutineExecution.DoesNotExist:
                # Opcional: Você pode logar as execuções não encontradas ou ignorar
                continue

        return Response({
            "detail": "Sincronização concluída com sucesso.",
            "updated_executions": updated_count
        }, status=status.HTTP_200_OK)