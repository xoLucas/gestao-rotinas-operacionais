from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone

from apps.execution.models import RoutineExecution
from apps.scheduling.models import ScheduleRule

# Serviços relacionados à geração de execuções de rotinas a partir das regras de agendamento.

def combine_date_and_time(date, time):
    naive_datetime = datetime.combine(date, time)
    return timezone.make_aware(naive_datetime)


def get_shift_start_and_end(work_session):
    shift = work_session.shift
    session_date = timezone.localdate(work_session.started_at)

    shift_start = combine_date_and_time(session_date, shift.start_time)
    shift_end = combine_date_and_time(session_date, shift.end_time)

    # Caso o turno atravesse meia-noite. Ex: 19:00 até 07:00.
    if shift_end <= shift_start:
        shift_end += timedelta(days=1)

    return shift_start, shift_end


def create_execution_if_not_exists(work_session, routine, planned_start_at, planned_end_at):
    execution, created = RoutineExecution.objects.get_or_create(
        work_session=work_session,
        routine=routine,
        planned_start_at=planned_start_at,
        defaults={
            "planned_end_at": planned_end_at,
            "status": RoutineExecution.Status.PENDING,
        },
    )

    return execution, created


@transaction.atomic
def generate_executions_for_work_session(work_session):
    shift = work_session.shift
    shift_start, shift_end = get_shift_start_and_end(work_session)

    schedule_rules = ScheduleRule.objects.filter(
        shift=shift,
        is_active=True,
        routine__is_active=True,
    ).select_related("routine")

    created_executions = []

    for rule in schedule_rules:
        routine = rule.routine

        if rule.frequency_type == ScheduleRule.FrequencyType.ONCE_PER_SHIFT:
            execution, created = create_execution_if_not_exists(
                work_session=work_session,
                routine=routine,
                planned_start_at=shift_start,
                planned_end_at=shift_end,
            )

            if created:
                created_executions.append(execution)

        elif rule.frequency_type == ScheduleRule.FrequencyType.SHIFT_START:
            planned_start = shift_start
            planned_end = planned_start + timedelta(minutes=rule.window_after_minutes)

            execution, created = create_execution_if_not_exists(
                work_session=work_session,
                routine=routine,
                planned_start_at=planned_start,
                planned_end_at=planned_end,
            )

            if created:
                created_executions.append(execution)

        elif rule.frequency_type == ScheduleRule.FrequencyType.SHIFT_END:
            planned_start = shift_end - timedelta(minutes=rule.window_before_minutes)
            planned_end = shift_end

            execution, created = create_execution_if_not_exists(
                work_session=work_session,
                routine=routine,
                planned_start_at=planned_start,
                planned_end_at=planned_end,
            )

            if created:
                created_executions.append(execution)

        elif rule.frequency_type == ScheduleRule.FrequencyType.EVERY_X_HOURS:
            if not rule.interval_hours:
                continue

            current_time = shift_start

            while current_time <= shift_end:
                planned_start = current_time
                planned_end = planned_start + timedelta(minutes=rule.window_after_minutes)

                execution, created = create_execution_if_not_exists(
                    work_session=work_session,
                    routine=routine,
                    planned_start_at=planned_start,
                    planned_end_at=planned_end,
                )

                if created:
                    created_executions.append(execution)

                current_time += timedelta(hours=rule.interval_hours)

        elif rule.frequency_type == ScheduleRule.FrequencyType.FIXED_TIME:
            if not rule.fixed_time:
                continue

            planned_start = combine_date_and_time(
                timezone.localdate(work_session.started_at),
                rule.fixed_time,
            )

            if shift_start <= planned_start <= shift_end:
                planned_end = planned_start + timedelta(minutes=rule.window_after_minutes)

                execution, created = create_execution_if_not_exists(
                    work_session=work_session,
                    routine=routine,
                    planned_start_at=planned_start,
                    planned_end_at=planned_end,
                )

                if created:
                    created_executions.append(execution)

    return created_executions