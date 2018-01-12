# NubeliU Billing SDK
# @autor: Sergio Colinas
from billingclient.common import base


class WidgetResult(base.Resource):

    key = 'widget'

    def __repr__(self):
        return "<Widget %s>" % self._info


class WidgetManager(base.Manager):

    base_url = "/v1/widget"
