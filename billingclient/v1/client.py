# NubeliU Billing SDK
# @autor: Sergio Colinas
from stevedore import extension

from billingclient import client as ckclient
from billingclient.openstack.common.apiclient import client
from billingclient.v1 import chart
from billingclient.v1 import core
from billingclient.v1 import metric
from billingclient.v1.rating.gnocchi import client as rating_client
from billingclient.v1 import report
from billingclient.v1 import widget

SUBMODULES_NAMESPACE = 'billing.client.modules'


class Client(object):
    """Client for the Billing v1 API.

    :param string endpoint: A user-supplied endpoint URL for the billing
                            service.
    :param function token: Provides token for authentication.
    :param integer timeout: Allows customization of the timeout for client
                            http requests. (optional)
    """

    def __init__(self, *args, **kwargs):
        """Initialize a new client for the Billing v1 API."""
        self.auth_plugin = (kwargs.get('auth_plugin')
                            or ckclient.get_auth_plugin(*args, **kwargs))
        self.client = client.HTTPClient(
            auth_plugin=self.auth_plugin,
            region_name=kwargs.get('region_name'),
            endpoint_type=kwargs.get('endpoint_type'),
            original_ip=kwargs.get('original_ip'),
            verify=kwargs.get('verify'),
            cert=kwargs.get('cert'),
            timeout=kwargs.get('timeout'),
            timings=kwargs.get('timings'),
            keyring_saver=kwargs.get('keyring_saver'),
            debug=kwargs.get('debug'),
            user_agent=kwargs.get('user_agent'),
            http=kwargs.get('http')
        )

        self.http_client = client.BaseClient(self.client)
        self.status = core.BillingStatusManager(self.http_client)
        self.charts = chart.ChartManager(self.http_client)
        self.rating = rating_client.Client(self.http_client)
        self.metrics = metric.MetricManager(self.http_client)
        self.reports = report.ReportManager(self.http_client)
        self.widgets = widget.WidgetManager(self.http_client)
        self._expose_submodules()

    def _expose_submodules(self):
        extensions = extension.ExtensionManager(
            SUBMODULES_NAMESPACE,
        )
        for ext in extensions:
            client = ext.plugin.get_client(self.http_client)
            setattr(self, ext.name, client)
