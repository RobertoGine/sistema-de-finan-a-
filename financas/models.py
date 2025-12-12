from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Transacao(models.Model):
    TIPO_CHOICES = (
        ('R', 'Receita'),
        ('D', 'Despesa'),
    )
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=50)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    descricao = models.TextField(blank=True, null=True)

    # NOVOS CAMPOS LEMBRETES
    data_vencimento = models.DateField(blank=True, null=True)
    lembrete_enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.valor}"
    
    
class ContaPagar(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    data_vencimento = models.DateField()
    descricao = models.TextField(blank=True, null=True)
    lembrete_enviado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - vence em {self.data_vencimento}"

