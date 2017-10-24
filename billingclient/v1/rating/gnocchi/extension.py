# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.v1.rating.gnocchi import client
from billingclient.v1.rating.gnocchi import shell


class Extension(object):
    """Gnocchi extension.

    """

    @staticmethod
    def get_client(http_client):
        return client.Client(http_client)

    @staticmethod
    def get_shell():
        return shell
