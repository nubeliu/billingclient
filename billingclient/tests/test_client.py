import types

import mock

from billingclient import client
from billingclient.tests import fakes
from billingclient.tests import utils
from billingclient.v1 import client as v1client

FAKE_ENV = {
    'username': 'username',
    'password': 'password',
    'tenant_name': 'tenant_name',
    'auth_url': 'http://no.where',
    'os_endpoint': 'http://no.where',
    'auth_plugin': 'fake_auth',
    'token': '1234',
    'user_domain_name': 'default',
    'project_domain_name': 'default',
}


class ClientTest(utils.BaseTestCase):

    @staticmethod
    def create_client(env, api_version=1, endpoint=None, exclude=[]):
        env = dict((k, v) for k, v in env.items()
                   if k not in exclude)

        return client.get_client(api_version, **env)

    def setUp(self):
        super(ClientTest, self).setUp()

    def test_client_version(self):
        c1 = self.create_client(env=FAKE_ENV, api_version=1)
        self.assertIsInstance(c1, v1client.Client)

    def test_client_auth_lambda(self):
        env = FAKE_ENV.copy()
        env['token'] = lambda: env['token']
        self.assertIsInstance(env['token'],
                              types.FunctionType)
        c1 = self.create_client(env)
        self.assertIsInstance(c1, v1client.Client)

    def test_client_auth_non_lambda(self):
        env = FAKE_ENV.copy()
        env['token'] = "1234"
        self.assertIsInstance(env['token'], str)
        c1 = self.create_client(env)
        self.assertIsInstance(c1, v1client.Client)

    @mock.patch('keystoneclient.v2_0.client', fakes.FakeKeystone)
    def test_client_without_auth_plugin(self):
        env = FAKE_ENV.copy()
        del env['auth_plugin']
        c = self.create_client(env, api_version=1, endpoint='fake_endpoint')
        self.assertIsInstance(c.auth_plugin, client.AuthPlugin)

    def test_client_without_auth_plugin_keystone_v3(self):
        env = FAKE_ENV.copy()
        del env['auth_plugin']
        expected = {
            'username': 'username',
            'endpoint': 'http://no.where',
            'tenant_name': 'tenant_name',
            'service_type': None,
            'token': '1234',
            'endpoint_type': None,
            'auth_url': 'http://no.where',
            'tenant_id': None,
            'cacert': None,
            'password': 'password',
            'domain_id': None,
            'domain_name': None,
            'user_domain_name': 'default',
            'user_domain_id': None,
            'project_domain_name': 'default',
            'project_domain_id': None,
        }
        with mock.patch('billingclient.client.AuthPlugin') as auth_plugin:
            self.create_client(env, api_version=1)
            auth_plugin.assert_called_with(**expected)

    def test_client_with_auth_plugin(self):
        c = self.create_client(FAKE_ENV, api_version=1)
        self.assertIsInstance(c.auth_plugin, str)

    def test_v1_client_timeout_invalid_value(self):
        env = FAKE_ENV.copy()
        env['timeout'] = 'abc'
        self.assertRaises(ValueError, self.create_client, env)
        env['timeout'] = '1.5'
        self.assertRaises(ValueError, self.create_client, env)

    def _test_v1_client_timeout_integer(self, timeout, expected_value):
        env = FAKE_ENV.copy()
        env['timeout'] = timeout
        expected = {
            'auth_plugin': 'fake_auth',
            'timeout': expected_value,
            'original_ip': None,
            'http': None,
            'region_name': None,
            'verify': True,
            'timings': None,
            'keyring_saver': None,
            'cert': None,
            'endpoint_type': None,
            'user_agent': None,
            'debug': None,
        }
        cls = 'billingclient.openstack.common.apiclient.client.HTTPClient'
        with mock.patch(cls) as mocked:
            self.create_client(env)
            mocked.assert_called_with(**expected)

    def test_v1_client_timeout_zero(self):
        self._test_v1_client_timeout_integer(0, None)

    def test_v1_client_timeout_valid_value(self):
        self._test_v1_client_timeout_integer(30, 30)

    def test_v1_client_cacert_in_verify(self):
        env = FAKE_ENV.copy()
        env['cacert'] = '/path/to/cacert'
        client = self.create_client(env)
        self.assertEqual('/path/to/cacert',
                         client.http_client.http_client.verify)

    def test_v1_client_certfile_and_keyfile(self):
        env = FAKE_ENV.copy()
        env['cert_file'] = '/path/to/cert'
        env['key_file'] = '/path/to/keycert'
        client = self.create_client(env)
        self.assertEqual(('/path/to/cert', '/path/to/keycert'),
                         client.http_client.http_client.cert)
