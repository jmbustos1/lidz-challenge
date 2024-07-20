from rest_framework import serializers
from .models import Client, Message, Debt

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'rut', 'salary', 'savings']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'role', 'sent_at']

class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = ['id', 'amount', 'institution', 'due_date']

class ClientDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    debts = DebtSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'rut', 'salary', 'savings', 'messages', 'debts']