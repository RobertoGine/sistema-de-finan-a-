from django.contrib import admin
from .models import Transacao
from django.contrib.auth.models import User

admin.site.register(User)

@admin.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('usuario','tipo','categoria','valor','data')
    list_filter = ('tipo','categoria','data')
