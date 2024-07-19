from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    salary = models.IntegerField()
    savings = models.IntegerField()
    email = models.EmailField(max_length=254, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name