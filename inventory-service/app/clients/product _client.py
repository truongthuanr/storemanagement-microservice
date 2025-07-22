# app/clients/product_client.py

import requests
from app.servicelogging.servicelogger import logger

class ProductClient:
    def __init__(self, base_url: str = "http://product-service:8000"):
        self.base_url = base_url

    def check_product_exists(self, product_id: int) -> bool:
        try:
            response = requests.get(
                f"{self.base_url}/products/{product_id}",
                timeout=2
            )
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            else:
                logger.error(
                    f"[ProductClient] Unexpected status code {response.status_code} "
                    f"when checking product_id={product_id}"
                )
                return False
        except requests.RequestException as e:
            logger.error(
                f"[ProductClient] Error connecting to product-service for product_id={product_id}: {e}"
            )
            return False