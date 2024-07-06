from price_fetcher import PriceFetcher
from email_service import EmailService
from config import Config
import random
import logging
from time import sleep
from concurrent.futures import ThreadPoolExecutor

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PriceAlert:
    def __init__(self, origin, destination, start_date, end_date):
        self.origin = origin
        self.destination = destination
        self.start_date = start_date
        self.end_date = end_date
        self.price_fetcher = PriceFetcher()
        self.email_service = EmailService()

    def check_prices(self):
        try:
            prices_start, prices_end = self.price_fetcher.fetch_prices(self.origin, self.destination, self.start_date, self.end_date)
            for prices in [prices_start, prices_end]:
                for quote in prices['Quotes']:
                    if quote['MinPrice'] <= Config.PRICE_LIMIT:
                        self.email_service.send_email(quote['MinPrice'], self.destination)
                        logger.info(f'Alerta enviado para {self.destination} com preço {quote["MinPrice"]}')
                        break
        except Exception as e:
            logger.error(f"Erro ao buscar preços: {e}")

def sleep_randomly(min_seconds=3600, max_seconds=10800):
    sleep_time = random.randint(min_seconds, max_seconds)
    logger.info(f'Dormindo por {sleep_time} segundos para evitar detecção')
    sleep(sleep_time)

def lambda_handler(event, context):
    destinations = [
        {"origin": "FOR", "destination": "IGU", "start_date": "2024-09-01", "end_date": "2024-09-15"},
        {"origin": "FOR", "destination": "GRU", "start_date": "2024-09-01", "end_date": "2024-09-15"}
    ]

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = []
        for trip in destinations:
            alert = PriceAlert(trip["origin"], trip["destination"], trip["start_date"], trip["end_date"])
            futures.append(executor.submit(alert.check_prices))

        for future in futures:
            try:
                future.result()
            except Exception as e:
                logger.error(f"Erro ao executar o alerta de preço: {e}")

if __name__ == '__main__':
    lambda_handler(None, None)
