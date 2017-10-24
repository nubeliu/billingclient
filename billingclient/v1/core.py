# NubeliU Billing SDK
# @autor: Sergio Colinas

from billingclient.common import base


class BillingModule(base.Resource):

    key = 'module'

    def __repr__(self):
        return "<BillingModule %s>" % self._info

    def enable(self):
        self.enabled = True
        self.update()

    def disable(self):
        self.enabled = False
        self.update()


class BillingModuleManager(base.CrudManager):
    resource_class = BillingModule
    base_url = "/v1/rating"
    key = 'module'
    collection_key = "modules"


class Collector(base.Resource):

    key = 'collector'

    def __repr__(self):
        return "<Collector %s>" % self._info


class CollectorManager(base.Manager):
    resource_class = Collector
    base_url = "/v1/rating"
    key = "collector"
    collection_key = "collectors"


class QuotationManager(base.Manager):
    base_url = "/v1/rating/quote"

    def quote(self, resources):
        out = self.api.post(self.base_url,
                            json={'resources': resources}).json()
        return out
