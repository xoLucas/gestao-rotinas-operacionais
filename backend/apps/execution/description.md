6. execution

Responsável pela execução real das rotinas pelo operador.

No escopo, o operador inicia turno, vê agenda, inicia rotina, registra horários, observa status e conclui atividade.

Soluções desse app:

execution/
- início de turno
- registro de presença
- início de execução da rotina
- conclusão da rotina
- status: pendente, em execução, concluída, atrasada, não realizada
- observações do operador
- controle de janela permitida
- bloqueio contra execução duplicada

Modelos prováveis:

WorkSession
RoutineExecution
ExecutionStepResult
Abnormality
ServiceRequestRecord
ShiftReport

Aqui fica o coração operacional.

Exemplo de fluxo:

1. Operador inicia turno
2. Sistema cria WorkSession
3. Operador pega uma rotina
4. Sistema cria RoutineExecution
5. Operador anexa foto, GPS e observação
6. Sistema valida e conclui

Sobre o problema de dois operadores: o escopo recomenda que quem pegar primeiro a solicitação fique com ela, e o outro seja notificado; esse bloqueio depende de internet antes do início da rotina.

Então o app execution teria uma solução chamada algo como:

claim routine

Ou seja:

Operador A clicou em “Iniciar”
→ backend bloqueia aquela execução para A
→ Operador B não consegue iniciar a mesma