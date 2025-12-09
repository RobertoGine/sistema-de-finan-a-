from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

class BrevoEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.environ.get("BREVO_API_KEY")

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
            sib_api_v3_sdk.ApiClient(configuration)
        )

        sent_count = 0

        for message in email_messages:
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
                to=[{"email": addr} for addr in message.to],
                subject=message.subject,
                html_content=message.body,
                sender={"email": os.environ.get("DEFAULT_FROM_EMAIL")}
            )

            try:
                api_instance.send_transac_email(send_smtp_email)
                sent_count += 1
            except ApiException as e:
                print("Erro ao enviar email:", e)

        return sent_count
