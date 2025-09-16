from dependency_injector import containers, providers

from bases import base_http_client
from integration import http_client


class IntegrationContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["services"])

    http_client: base_http_client.BaseHTTPClient = providers.Factory(http_client.HTTPClient)
