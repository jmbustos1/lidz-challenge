from django.db import models
from scoring.enums import (
    ModelMessage,
    BankChoices,
)

class Client(models.Model):
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    salary = models.IntegerField()
    savings = models.IntegerField()
    age = models.IntegerField(null=True, blank=True)  # Nuevo campo de edad
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Message(models.Model):
    
    client = models.ForeignKey(Client, related_name='messages', on_delete=models.CASCADE)
    text = models.TextField()
    role = models.CharField(max_length=10, choices=ModelMessage.choices)
    sentAt = models.DateTimeField()

    def __str__(self):
        return f"{self.role} - {self.sentAt}: {self.text[:20]}"
    

class Debt(models.Model):
    client = models.ForeignKey(Client, related_name='debts', on_delete=models.CASCADE)
    institution = models.CharField(max_length=100, choices=BankChoices.choices)
    amount = models.IntegerField()
    dueDate = models.DateField()

    def __str__(self):
        return f"{self.institution} - {self.amount} - {self.dueDate}"