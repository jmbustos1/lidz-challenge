
from django.db.models import IntegerChoices as _IntegerChoices
from django.db.models import TextChoices as _TextChoices

class ModelMessage(_TextChoices):
    """
    Alternativa de modelo de mensaje
    """

    Client = "client"
    Agent = "agent"