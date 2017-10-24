# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.common import base


class Metric(base.Resource):

    key = 'metric'

    def __repr__(self):
        return "<Metric %s>" % self._info


class Report(base.Resource):

    key = 'reports'

    def __repr__(self):
        return "<Report %s>" % self._info


class Measure(base.Resource):

    key = 'definition'

    def __repr__(self):
        return "<Measure %s>" % self._info


class MetricDefinitionManager(base.CrudManager):
    resource_class = Metric
    base_url = "/v1/metric"
    key = "definition"
    collection_key = "definitions"


class ReportDefinitionManager(base.CrudManager):
    resource_class = Report
    base_url = "/v1/report"
    key = "definition"
    collection_key = "definitions"


class MetricDefinitionMeasuresManager(base.CrudManager):
    resource_class = Measure
    base_url = "/v1/metric"
    key = "definition"
    collection_key = "measures"


class ReportDefinitionMeasuresManager(base.CrudManager):
    resource_class = Measure
    base_url = "/v1/report"
    key = "definition"
    collection_key = "measures"
