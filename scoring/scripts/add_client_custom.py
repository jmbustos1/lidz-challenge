import requests
import json

# URL de la API
url = "http://127.0.0.1:8000/client/"

# Datos del cliente
data = {
    "name": "Juan Perez",
    "rut": "11.111.111-1",
    "salary": 1000000,
    "savings": 5000000,
    "messages": [
        {
            "text": "Hola, quiero comprar un dpto",
            "sent_at": "2023-12-24T00:00:00.000Z",
            "role": "client"
        },
        {
            "text": "Perfecto, te puedo ayudar con eso",
            "sent_at": "2023-12-24T00:00:00.000Z",
            "role": "agent"
        }
    ],
    "debts": [
        {
            "amount": 1000000,
            "institution": "Banco Estado",
            "due_date": "2023-12-24T00:00:00.000Z"
        }
    ]
}

# Realizar la solicitud POST
response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

# Imprimir la respuesta
print("Status Code:", response.status_code)
print("Response JSON:", response.json())