from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import EmailMessage
from financas.models import ContaPagar

class Command(BaseCommand):
    help = "Envia lembretes de contas que vencem hoje"

    def handle(self, *args, **kwargs):
        hoje = timezone.now().date()

        contas = ContaPagar.objects.filter(
            data_vencimento=hoje,
            lembrete_enviado=False
        )

        if not contas.exists():
            self.stdout.write("Nenhum lembrete para enviar hoje.")
            return

        for conta in contas:
            assunto = f"Lembrete: Conta '{conta.titulo}' vence hoje"
            mensagem = (
                f"Olá {conta.usuario.first_name or conta.usuario.username},\n\n"
                f"A conta '{conta.titulo}' vence hoje ({hoje}).\n"
                f"Valor: R$ {conta.valor}\n\n"
                f"Descrição: {conta.descricao or 'Nenhuma'}\n\n"
                "Não esqueça de realizar o pagamento!\n\n"
                "— Sistema Financeiro"
            )

            try:
                email = EmailMessage(
                    subject=assunto,
                    body=mensagem,
                    from_email=None,     # usa o DEFAULT_FROM_EMAIL
                    to=[conta.usuario.email],
                )
                email.send()

                conta.lembrete_enviado = True
                conta.save()

                self.stdout.write(f"Lembrete enviado: {conta.titulo}")

            except Exception as e:
                self.stderr.write(f"Erro ao enviar para {conta.usuario.email}: {e}")
