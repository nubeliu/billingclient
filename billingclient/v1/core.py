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
    key = 'state'

    def is_enabled(self):
        return self.client.get(self.base_url + "/state/is_enabled").json()

    def set_status(self, enabled):
        return self.client.post(self.base_url + "/state/set_status?enabled=" +
                                str(enabled)).json()

    def get_last_processed_timestamp(self):
        return self.client.get(self.base_url +
                               "/state/get_last_processed_timestamp").json()

    def recalculate_since(self, timestamp):
        return self.client.post(self.base_url +
                                "/state/recalculate_since?timestamp=" +
                                timestamp).json()
