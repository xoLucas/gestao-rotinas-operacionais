1. accounts

Responsável por usuários, login e permissões.

No seu escopo, o operador precisa se identificar no início do turno, e o sistema também precisa diferenciar operador, gerente e administrador.

Soluções desse app:

accounts/
- cadastro de usuários
- login/autenticação
- operador
- gerente
- administrador
- permissões de acesso
- vínculo entre usuário e perfil operacional

Modelos prováveis:

User
OperatorProfile
Role
Permission

Exemplo de responsabilidade:

“Lucas é operador da equipe A, pode executar rotinas, mas não pode editar periodicidade.”