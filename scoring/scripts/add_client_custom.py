import requests
import json

url = "http://127.0.0.1:8000/clients/"

"""Funcion para agregar un unico cliente"""
data = {
    "name": "Juan Perez",
    "rut": "11.111.120-1",
    "salary": 1000000,
    "savings": 5000000,
    "age": 30,
    "messages": [
        {
            "text": "Hola, quiero comprar un dpto",
            "sentAt": "2023-12-24T00:00:00.000Z",
            "role": "client"
        },
        {
            "text": "Perfecto, te puedo ayudar con eso",
            "sentAt": "2023-12-24T00:00:00.000Z",
            "role": "agent"
        }
    ],
    "debts": [
        {
            "amount": 1000000,
            "institution": "Banco Estado",
            "dueDate": "2023-12-24T00:00:00.000Z"
        }
    ]
}

response = requests.post(url, headers={"Content-Type": "application/json"}, data=json.dumps(data))

print("Status Code:", response.status_code)
print("Response JSON:", response.json())