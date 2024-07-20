import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
from .models import Client, Message, Debt
from .serializers import ClientSerializer, ClientDetailSerializer
from django.utils import timezone
from datetime import timedelta

faker = Faker()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def client_list_url():
    return reverse('client-list')

@pytest.fixture
def client_detail_url(client):
    return reverse('client-detail', args=[client.id])

@pytest.fixture
def follow_up_url():
    return reverse('clients-to-do-follow-up')

@pytest.fixture
def create_client_url():
    return reverse('client-create')

@pytest.fixture
def client():
    return Client.objects.create(
        name="Juan Perez",
        rut="11.111.111-1",
        salary=1000000,
        savings=5000000
    )

@pytest.fixture
def message(client):
    return Message.objects.create(
        client=client,
        text="Hola, quiero comprar un dpto",
        role="client",
        sent_at=timezone.now()
    )

@pytest.fixture
def debt(client):
    return Debt.objects.create(
        client=client,
        amount=1000000,
        institution="Banco Estado",
        due_date=timezone.now().date()
    )

@pytest.mark.django_db
@patch('scoring.views.Client.objects.all')
def test_get_clients(mock_all, client_list_url, client, api_client):
    mock_all.return_value = [client]
    response = api_client.get(client_list_url)
    serializer = ClientSerializer([client], many=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data

@pytest.mark.django_db
@patch('scoring.views.Client.objects.get')
def test_get_client_detail(mock_get, client_detail_url, client, api_client):
    mock_get.return_value = client
    response = api_client.get(client_detail_url)
    serializer = ClientDetailSerializer(client)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data

@pytest.mark.django_db
def test_create_client(create_client_url, api_client):
    data = {
        "name": "Maria Lopez",
        "rut": "31.111.111-1",
        "salary": 1200000,
        "savings": 3000000,
        "messages": [
            {
                "text": "Quiero más información",
                "role": "client",
                "sent_at": "2023-12-24T00:00:00.000Z"
            }
        ],
        "debts": [
            {
                "amount": 200000,
                "institution": "Banco Santander",
                "due_date": "2023-12-24"
            }
        ]
    }
    response = api_client.post(create_client_url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Verificar que el cliente y sus relaciones fueron creados correctamente
    client = Client.objects.get(rut="31.111.111-1")
    assert client.name == "Maria Lopez"
    assert client.salary == 1200000
    assert client.savings == 3000000

    messages = Message.objects.filter(client=client)
    assert len(messages) == 1
    assert messages[0].text == "Quiero más información"
    assert messages[0].role == "client"

    debts = Debt.objects.filter(client=client)
    assert len(debts) == 1
    assert debts[0].amount == 200000
    assert debts[0].institution == "Banco Santander"

@pytest.mark.django_db
def test_clients_to_do_follow_up(follow_up_url, client, message, debt, api_client):
    seven_days_ago = timezone.now() - timedelta(days=7)
    response = api_client.get(follow_up_url)
    clients = Client.objects.filter(messages__sent_at__lt=seven_days_ago).distinct()
    serializer = ClientSerializer(clients, many=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data