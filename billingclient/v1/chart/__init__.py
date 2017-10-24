# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.common import base
from billingclient.v1.chart import definition


class ChartManager(base.Manager):

    base_url = "/v1/chart"

    def __init__(self, http_client):
        self.mappings = definition.ChartDefinitionManager(http_client)
        self.measures = definition.ChartDefinitionMeasuresManager(http_client)
        self.dashboards = definition.DashboardDefinitionManager(http_client)
        self.dashboard_measures = definition.DashboardDefinitionMeasuresManager(http_client)
        super(ChartManager, self).__init__(http_client)
