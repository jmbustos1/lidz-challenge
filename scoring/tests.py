import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from faker import Faker
from unittest.mock import patch
from .models import Client, Message, Debt
from .serializers import ClientSerializer, ClientDetailSerializer
from django.utils import timezone
from datetime import timedelta
from scoring.enums import (
    ModelMessage,
    BankChoices,
)
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
        name=faker.name(),
        rut=faker.unique.bothify(text='##.###.###-#'),
        salary=faker.random_int(min=500000, max=2000000),
        savings=faker.random_int(min=1000000, max=10000000)
    )

@pytest.fixture
def message(client):
    return Message.objects.create(
        client=client,
        text=faker.sentence(),
        role=faker.random_element(elements=ModelMessage.values),
        sentAt=timezone.now()
    )

@pytest.fixture
def debt(client):
    return Debt.objects.create(
        client=client,
        amount=faker.random_int(min=50000, max=5000000),
        institution=faker.random_element(elements=BankChoices.values),
        dueDate=faker.date()
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
        "name": faker.name(),
        "rut": faker.unique.bothify(text='##.###.###-#'),
        "salary": faker.random_int(min=500000, max=2000000),
        "savings": faker.random_int(min=1000000, max=10000000),
        "age": faker.random_int(min=15, max=110),
        "messages": [
            {
                "text": faker.sentence(),
                "role": faker.random_element(elements=('client', 'agent')),
                "sentAt": faker.date_time_this_year().isoformat()
            }
        ],
        "debts": [
            {
                "amount": faker.random_int(min=50000, max=5000000),
                "institution": faker.random_element(elements=BankChoices.values),
                "dueDate": faker.date()
            }
        ]
    }
    response = api_client.post(create_client_url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED

    # Verificar que el cliente y sus relaciones fueron creados correctamente
    client = Client.objects.get(rut=data["rut"])
    assert client.name == data["name"]
    assert client.name == data["age"]
    assert client.salary == data["salary"]
    assert client.savings == data["savings"]

    messages = Message.objects.filter(client=client)
    assert len(messages) == 1
    assert messages[0].text == data["messages"][0]["text"]
    assert messages[0].role == data["messages"][0]["role"]

    debts = Debt.objects.filter(client=client)
    assert len(debts) == 1
    assert debts[0].amount == data["debts"][0]["amount"]
    assert debts[0].institution == data["debts"][0]["institution"]

@pytest.mark.django_db
def test_clients_to_do_follow_up(follow_up_url, client, message, debt, api_client):
    seven_days_ago = timezone.now() - timedelta(days=7)
    response = api_client.get(follow_up_url)
    clients = Client.objects.filter(messages__sentAt__lt=seven_days_ago).distinct()
    serializer = ClientSerializer(clients, many=True)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == serializer.data