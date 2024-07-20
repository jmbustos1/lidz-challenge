from rest_framework import serializers
from .models import Client, Message, Debt




class MessageSerializer(serializers.ModelSerializer):
    sent_at = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", input_formats=["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"])
    class Meta:
        model = Message
        fields = ['id', 'text', 'role', 'sent_at']

class DebtSerializer(serializers.ModelSerializer):
    due_date = serializers.DateField(format="%Y-%m-%d", input_formats=["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%S"])
    class Meta:
        model = Debt
        fields = ['id', 'amount', 'institution', 'due_date']

class ClientDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    debts = DebtSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'rut', 'salary', 'savings', 'messages', 'debts']
    
class ClientSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, required=False)
    debts = DebtSerializer(many=True, required=False)
    class Meta:
        model = Client
        fields = ['id', 'name', 'rut', 'salary', 'savings', 'messages', 'debts']

    def create(self, validated_data):
        messages_data = validated_data.pop('messages', [])
        debts_data = validated_data.pop('debts', [])
        
        client = Client.objects.create(**validated_data)
        
        for message_data in messages_data:
            print(message_data)
            Message.objects.create(client=client, **message_data)
        
        for debt_data in debts_data:
            print(debt_data)
            Debt.objects.create(client=client, **debt_data)
        
        return client