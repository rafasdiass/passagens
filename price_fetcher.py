import requests
from config import Config
import logging
from random import choice

logger = logging.getLogger(__name__)

class PriceFetcher:
    def __init__(self):
        # Lista de proxies obtidos de serviços como ProxyScrape, Free Proxy List, e ProxyNova
        self.proxies = [
            {'http': 'http://191.252.110.90:8080', 'https': 'https://191.252.110.90:8080'},
            {'http': 'http://45.224.151.222:999', 'https': 'https://45.224.151.222:999'},
            {'http': 'http://103.109.57.145:8080', 'https': 'https://103.109.57.145:8080'},
            {'http': 'http://45.77.242.203:3128', 'https': 'https://45.77.242.203:3128'},
            {'http': 'http://103.216.82.146:6666', 'https': 'https://103.216.82.146:6666'},
            {'http': 'http://85.15.153.219:3128', 'https': 'https://85.15.153.219:3128'},
            {'http': 'http://46.8.28.17:8080', 'https': 'https://46.8.28.17:8080'},
            {'http': 'http://103.87.236.46:8080', 'https': 'https://103.87.236.46:8080'},
            {'http': 'http://51.158.68.68:8811', 'https': 'https://51.158.68.68:8811'},
            {'http': 'http://138.68.41.90:3128', 'https': 'https://138.68.41.90:3128'},
            {'http': 'http://103.87.236.46:3128', 'https': 'https://103.87.236.46:3128'},
            {'http': 'http://5.189.188.178:3128', 'https': 'https://5.189.188.178:3128'},
            {'http': 'http://163.172.157.45:3128', 'https': 'https://163.172.157.45:3128'},
            {'http': 'http://51.75.147.41:3128', 'https': 'https://51.75.147.41:3128'},
            {'http': 'http://51.75.147.40:3128', 'https': 'https://51.75.147.40:3128'},
            {'http': 'http://178.62.193.19:3128', 'https': 'https://178.62.193.19:3128'}
            # Adicione mais proxies conforme necessário
        ]
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15'
        ]

    def fetch_prices(self, origin, destination, start_date, end_date):
        headers = {'User-Agent': choice(self.user_agents)}
        proxy = choice(self.proxies)
        url = Config.get_search_url(origin, destination, start_date)
        try:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)  # Timeout aumentado
            response.raise_for_status()
            prices_start = response.json()
            logger.info(f'Sucesso ao buscar preços de {origin} para {destination} para a data {start_date}')

            url = Config.get_search_url(origin, destination, end_date)
            response = requests.get(url, headers=headers, proxies=proxy, timeout=10)  # Timeout aumentado
            response.raise_for_status()
            prices_end = response.json()
            logger.info(f'Sucesso ao buscar preços de {origin} para {destination} para a data {end_date}')

            return prices_start, prices_end
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar preços: {e}")
            raise
