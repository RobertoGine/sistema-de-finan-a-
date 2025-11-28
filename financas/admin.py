from django.contrib import admin
from .models import Transacao

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario','tipo','categoria','valor','data')
    list_filter = ('tipo','categoria','data')
