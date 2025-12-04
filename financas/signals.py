from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Acesso

@receiver(user_logged_in)
def registra_acesso(sender, user, request, **kwargs):
    Acesso.objects.create(usuario=user)
