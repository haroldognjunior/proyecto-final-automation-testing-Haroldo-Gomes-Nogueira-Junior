"""
Cliente HTTP chico para las pruebas de API.

Envuelve requests para no repetir la URL base, el timeout
y el logging de cada request/response en todos los tests.
"""
import logging

import requests

JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"

log = logging.getLogger(__name__)


class ApiClient:

    def __init__(self, base_url=JSONPLACEHOLDER_URL, timeout=10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json; charset=UTF-8"})

    def get(self, path, **kwargs):
        return self._send("GET", path, **kwargs)

    def post(self, path, payload, **kwargs):
        return self._send("POST", path, json=payload, **kwargs)

    def delete(self, path, **kwargs):
        return self._send("DELETE", path, **kwargs)

    def _send(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        log.info("%s %s", method, url)
        if "json" in kwargs:
            log.info("Body enviado: %s", kwargs["json"])

        response = self.session.request(method, url, timeout=self.timeout, **kwargs)

        elapsed_ms = response.elapsed.total_seconds() * 1000
        log.info("Respuesta %s en %.0f ms", response.status_code, elapsed_ms)
        return response

    def close(self):
        self.session.close()
