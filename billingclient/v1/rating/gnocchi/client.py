# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.v1.rating import gnocchi


class Client(object):
    """Client for the Gnocchi v1 API.

    :param http_client: A http client.
    """

    def __init__(self, http_client):
        """Initialize a new client for the Gnocchi v1 API."""
        self.http_client = http_client
        self.metric_rule_sets = gnocchi.MetricRuleSetManager(self.http_client)
        self.metadata_rule_sets = gnocchi.MetadataRuleSetManager(
            self.http_client)
        self.metric_rules = gnocchi.MetricRuleManager(self.http_client)
        self.metadata_rules = gnocchi.MetadataRuleManager(self.http_client)
        self.threshold_rules = gnocchi.ThresholdRuleManager(self.http_client)
