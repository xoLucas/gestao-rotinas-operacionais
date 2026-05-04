4. routines

Responsável pelo cadastro das rotinas e tarefas operacionais.

O escopo exige cadastro de rotinas com nome, descrição, instrução, área de execução, obrigatoriedade de foto e obrigatoriedade de geolocalização.

O Routine deve saber:
- de qual procedimento ela veio;
- qual item do procedimento;
- se é rotina normal ou tarefa crítica;
- se exige foto;
- se exige geolocalização;
- se exige observação;
- se pode gerar SS;
- qual área/rota/equipamento está relacionado;
- qual nível de criticidade.

Soluções desse app:

routines/
- cadastro de rotina
- instrução operacional
- tarefas/checklist da rotina
- obrigatoriedade de foto
- obrigatoriedade de localização
- prioridade da rotina
- vínculo com área operacional

Modelos prováveis:

Routine
RoutineStep
RoutineRequirement

Exemplos:

Routine:
- procedure_item: 8.1.5
- name: Rota de monitoramento da planta
- category: Rotina da operação
- frequency: a cada 4 horas
- criticality: alta
- requires_geolocation: true
- requires_photo: talvez true

Routine:
- procedure_item: 8.2.3
- name: Verificar nível da caixa API no início e fim do turno
- category: Tarefa crítica
- criticality: crítica

Esse app define o que deve ser feito.