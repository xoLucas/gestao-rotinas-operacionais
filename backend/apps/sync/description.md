8. sync

Responsável pela sincronização offline-first entre mobile e backend.

O escopo deixa claro que o app deve armazenar rotinas, fotos, registros, horários e localização localmente, e sincronizar quando houver conectividade.

Soluções desse app:

sync/
- envio de dados pendentes
- recebimento da agenda do turno
- controle de fila de sincronização
- controle de conflitos
- reprocessamento em caso de falha
- status de sincronização
- endpoints específicos para o app mobile

Modelos prováveis:

SyncBatch
SyncItem
Device
SyncLog
ConflictLog

Fluxo:

Antes do turno:
mobile baixa operadores, turnos, rotinas, áreas e regras

Durante o turno:
mobile salva tudo em SQLite

Depois:
mobile envia pacote de sincronização para o backend

Esse app não é só “API normal”. Ele existe porque offline-first exige lógica própria.