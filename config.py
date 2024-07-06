import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SKYSCANNER_API_KEY = os.getenv('SKYSCANNER_API_KEY')
    TO_EMAILS = os.getenv('TO_EMAILS').split(',')
    PRICE_LIMIT = 500
    SEARCH_URL_TEMPLATE = 'https://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/US/USD/en-US/{origin}/{destination}/{date}?apiKey={api_key}'

    @staticmethod
    def get_search_url(origin, destination, date):
        return Config.SEARCH_URL_TEMPLATE.format(
            origin=origin,
            destination=destination,
            date=date,
            api_key=Config.SKYSCANNER_API_KEY
        )
