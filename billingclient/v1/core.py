# NubeliU Billing SDK
# @autor: Sergio Colinas

from billingclient.common import base


class BillingStatus(base.Resource):

    key = 'status'

    def __repr__(self):
        return "<BillingStatus %s>" % self._info

    def enable(self):
        self.enabled = True
        self.update()

    def disable(self):
        self.enabled = False
        self.update()


class BillingStatusManager(base.CrudManager):
    resource_class = BillingStatus
    base_url = "/v1/rating"
    key = 'status'

    def is_enabled(self):
        return self.client.get(self.base_url + "/status/is_enabled").json()

    def set_status(self, enabled):
        return self.client.post(self.base_url + "/status/set_status?enabled=" +
                                ("true" if enabled else ""))

    def get_last_processed_timestamp(self):
        return self.client.get(self.base_url +
                               "/status/get_last_processed_timestamp").json()

    def recalculate_since(self, timestamp):
        return self.client.post(self.base_url +
                                "/status/recalculate_since?timestamp=" +
                                timestamp).json()
