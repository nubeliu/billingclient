# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.common import base


class Chart(base.Resource):

    key = 'charts'

    def __repr__(self):
        return "<Chart %s>" % self._info


class Dashboard(base.Resource):

    key = 'dashboards'

    def __repr__(self):
        return "<Dashboard %s>" % self._info


class Measure(base.Resource):

    key = 'definition'

    def __repr__(self):
        return "<Measure %s>" % self._info


class ChartDefinitionManager(base.CrudManager):
    resource_class = Chart
    base_url = "/v1/chart"
    key = "definition"
    collection_key = "definitions"


class DashboardDefinitionManager(base.CrudManager):
    resource_class = Dashboard
    base_url = "/v1/dashboard"
    key = "definition"
    collection_key = "definitions"

    def get_default(self):
        return self.client.get(self.base_url + "/default").json()


class ChartDefinitionMeasuresManager(base.CrudManager):
    resource_class = Measure
    base_url = "/v1/chart"
    key = "definition"
    collection_key = "measures"


class DashboardDefinitionMeasuresManager(base.CrudManager):
    resource_class = Measure
    base_url = "/v1/dashboard"
    key = "definition"
    collection_key = "measures"
