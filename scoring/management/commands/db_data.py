import random
from django.core.management.base import BaseCommand
from faker import Faker
from scoring.models import Client, Message, Debt
from scoring.enums import ModelMessage, BankChoices
from scoring.serializers import ClientSerializer
from datetime import timedelta

class Command(BaseCommand):
    "datos de prueba"
    
    def handle(self, *args, **kwargs):
        faker = Faker()
        message_count = 4
        client_count = 4
        debt_count = 3
        for _ in range(client_count):
            client_data = {
                "name": faker.name(),
                "rut": faker.unique.bothify(text='##.###.###-#'),
                "salary": faker.random_int(min=500000, max=2000000),
                "savings": faker.random_int(min=1000000, max=10000000),
                "messages": self.generate_intercalated_messages(faker, message_count),
                "debts": [
                    {
                        "amount": faker.random_int(min=50000, max=5000000),
                        "institution": random.choice([choice.value for choice in BankChoices]),
                        "due_date": faker.date()
                    } for _ in range(random.randint(1, debt_count))
                ]
            }

            serializer = ClientSerializer(data=client_data)
            if serializer.is_valid():
                serializer.save()
                self.stdout.write(self.style.SUCCESS(f'Cliente agregado exitosamente {client_data["name"]}'))
            else:
                self.stdout.write(self.style.ERROR(f'Error agregando cliente {client_data["name"]}'))
                self.stdout.write(self.style.ERROR(f'Errores: {serializer.errors}'))

    def generate_intercalated_messages(self, faker, num_messages):
        messages = []
        base_time = faker.date_time_this_year()

        for i in range(num_messages):
            role = ModelMessage.CLIENT if i % 2 == 0 else ModelMessage.AGENT
            sent_at = base_time + timedelta(minutes=i * 10)  # Aumentar 10 minutos entre cada mensaje
            message_data = {
                "text": faker.sentence(),
                "role": role,
                "sent_at": sent_at.isoformat()
            }
            messages.append(message_data)

        return messages