import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SKYSCANNER_API_KEY = os.getenv('SKYSCANNER_API_KEY')
    TO_EMAILS = os.getenv('TO_EMAILS').split(',')
    AWS_REGION = os.getenv('AWS_REGION')
    ORIGIN = os.getenv('ORIGIN')
    DESTINATION = os.getenv('DESTINATION')
    START_DATE = os.getenv('START_DATE')
    END_DATE = os.getenv('END_DATE')
    PRICE_LIMIT = int(os.getenv('PRICE_LIMIT'))
    SES_VERIFIED_EMAIL = os.getenv('SES_VERIFIED_EMAIL')
    SEARCH_URL_TEMPLATE = 'https://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US/{origin}/{destination}/{date}?apiKey={api_key}'

    @staticmethod
    def get_search_url(origin, destination, date):
        return Config.SEARCH_URL_TEMPLATE.format(
            origin=origin,
            destination=destination,
            date=date,
            api_key=Config.SKYSCANNER_API_KEY
        )
