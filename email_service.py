import boto3
from config import Config
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.ses_client = boto3.client('ses')

    def send_email(self, price, destination):
        try:
            response = self.ses_client.send_email(
                Source='your_verified_email@example.com',
                Destination={'ToAddresses': Config.TO_EMAILS},
                Message={
                    'Subject': {'Data': f'Alerta de Preço de Passagem Aérea para {destination}'},
                    'Body': {
                        'Text': {'Data': f'Preço encontrado: ${price}'},
                    },
                },
            )
            logger.info(f'Email enviado com sucesso: {response}')
        except Exception as e:
            logger.error(f"Erro ao enviar email: {e}")