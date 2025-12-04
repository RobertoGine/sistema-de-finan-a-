from django.contrib import admin
from .models import Transacao, Acesso


@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'tipo', 'categoria', 'valor', 'data')
    list_filter = ('tipo', 'categoria', 'data')
    search_fields = ('categoria', 'descricao')
    ordering = ('-data',)


@admin.register(Acesso)
class AcessoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'data_hora')
    list_filter = ('usuario', 'data_hora')
    search_fields = ('usuario__username',)
    ordering = ('-data_hora',)
