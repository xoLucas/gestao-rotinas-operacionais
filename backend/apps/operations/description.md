3. operations

Responsável por áreas físicas, locais de execução e geofence.

O escopo exige cadastro de áreas de serviço, geofence por raio ou coordenadas e vínculo entre rotina e área obrigatória.

Soluções desse app:

operations/
- cadastro de áreas de serviço
- coordenadas GPS
- raio permitido
- polígonos/geofences futuramente
- validação de presença na área

Modelos prováveis:

OperationalArea
Geofence
LocationPoint
ou
OperationalArea
OperationalRoute
Asset

Exemplo:

Área: Casa de bombas
Latitude: -18.XXXX
Longitude: -39.XXXX
Raio permitido: 80 metros

Esse app responde à pergunta:

“O operador estava no lugar certo para concluir essa rotina?”