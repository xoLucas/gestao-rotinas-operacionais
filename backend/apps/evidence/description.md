7. evidence

Responsável por fotos, localização e comprovações.

O escopo exige foto obrigatória, geolocalização, armazenamento das evidências em object storage e metadados no banco.

Soluções desse app:

evidence/
- upload de fotos
- metadados da foto
- vínculo da foto com execução
- localização coletada
- validação de geofence
- armazenamento do link da evidência

Modelos prováveis:

PhotoEvidence
LocationEvidence
EvidenceValidation

Exemplo:

Foto: rotina_123.jpg
Execução: Verificação do tanque
Operador: João
Horário: 10:42
Latitude/longitude: ...
Status: validada

Importante: a foto não deve ficar diretamente no PostgreSQL. O escopo recomenda Azure Blob Storage, deixando no banco apenas metadados e links.