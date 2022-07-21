from coinmetrics.api_client import CoinMetricsClient
import requests

SSL_CERT_LOCATION = requests.certs.where()
print(f"SSL Certs Location: {SSL_CERT_LOCATION}")

client = CoinMetricsClient(verify_ssl_certs=SSL_CERT_LOCATION)

if __name__ == "__main__":
    print(client.catalog_markets())