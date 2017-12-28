# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.common import base
from billingclient.v1.metric import definition


class MetricManager(base.Manager):

    base_url = "/v1/metric"

    def __init__(self, http_client):
        self.mappings = definition.MetricDefinitionManager(http_client)
        self.measures = definition.MetricDefinitionMeasuresManager(http_client)
        self.reports = definition.ReportDefinitionManager(http_client)
        self.report_measures = definition.ReportDefinitionMeasuresManager(
            http_client)
        self.widgets = definition.WidgetDefinitionManager(http_client)
        self.widget_measures = definition.WidgetDefinitionMeasuresManager(
            http_client)
        super(MetricManager, self).__init__(http_client)

    def list_available_metrics(self, gnocchi_metric=None, refresh=False):
        url = self.base_url + "/available?"
        if gnocchi_metric:
            url += "gnocchi_metric=" + gnocchi_metric + "&"
        if refresh and (refresh.lower() == "true" or refresh == "1"):
            url += "refresh=True"
        return self.client.get(url).json()
