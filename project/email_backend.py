import os
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException


class BrevoEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        api_key = os.environ.get("BREVO_API_KEY")
        sender_email = os.environ.get("DEFAULT_FROM_EMAIL")

        if not api_key or not sender_email:
            print("Faltando BREVO_API_KEY ou DEFAULT_FROM_EMAIL")
            return 0

        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = api_key

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        sent = 0

        for message in email_messages:

            html_body = message.body

            # Se o Django enviou alternativas, usa a versão HTML correta
            if hasattr(message, "alternatives") and message.alternatives:
                html_body = message.alternatives[0][0]

            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                sender={"email": sender_email},
                to=[{"email": addr} for addr in message.to],
                subject=message.subject,
                html_content=html_body
            )

            try:
                api_instance.send_transac_email(send_smtp_email)
                sent += 1
            except ApiException as e:
                print("Erro ao enviar email:", e)

        return sent
