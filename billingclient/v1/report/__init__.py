# NubeliU Billing SDK
# @autor: Sergio Colinas
import urllib

from billingclient.common import base

class ReportResult(base.Resource):

    key = 'report'

    def __repr__(self):
        return "<Report %s>" % self._info


class ReportManager(base.Manager):

    base_url = "/v1/report"

    def list_tenants(self):
        return self.client.get(self.base_url + "/tenants").json()

    def get_total(self, tenant_id, begin=None, end=None, service=None):
        url = self.base_url + "/total"
        filters = list()
        if tenant_id:
            filters.append("tenant_id=%s" % tenant_id)
        if begin:
            filters.append("begin=%s" % begin.isoformat())
        if end:
            filters.append("end=%s" % end.isoformat())
        if service:
            filters.append("service=%s" % service)
        if filters:
            url += "?%s" % ('&'.join(filters))
        return self.client.get(url).json()

    def get_aws_ri_coverage(self, account_id=None, secret_access_key=None, u_domain_id=None):
        url = self.base_url + "/aws_ri_coverage"
        params = list()
        if account_id:
            params.append("account_id=%s" % account_id)
        if secret_access_key:
            params.append("secret_access_key=%s" % urllib.quote(secret_access_key, safe=''))
        if u_domain_id:
            params.append("u_domain_id=%s" % u_domain_id)
            url += "?%s" % ('&'.join(params))
        return self.client.get(url).json()