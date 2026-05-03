10. audit

Responsável por histórico de alterações e rastreabilidade administrativa.

O escopo exige que toda alteração relevante gere trilha: quem criou, quem alterou, quando alterou, valor anterior e valor novo.

Soluções desse app:

audit/
- log de criação
- log de alteração
- log de exclusão
- valor anterior
- valor novo
- usuário responsável
- data e hora

Modelos prováveis:

AuditLog
ChangeRecord

Esse app é essencial porque o sistema tem valor de auditoria operacional.

Exemplo:

Usuário: Gerente Carlos
Ação: alterou periodicidade da rotina X
Antes: a cada 4 horas
Depois: a cada 2 horas
Data: 03/05/2026 14:32