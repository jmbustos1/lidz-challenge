
from django.db.models import IntegerChoices as _IntegerChoices
from django.db.models import TextChoices as _TextChoices

class ModelMessage(_TextChoices):
    """
    Alternativa de modelo de mensaje
    """

    Client = "client"
    Agent = "agent"

class BankChoices(_TextChoices):
    BANCO_ITAU = "Banco Itau"
    BANCO_BICE = "Banco Bice"
    BANCO_ESTADO = "Banco Estado"
    BANCO_CHILE = "Banco Chile"
    BANCO_SANTANDER = "Banco Santander"
    BANCO_BCI = "Banco BCI"
    BANCO_FALABELLA = "Banco Falabella"
    HITES = "Hites"