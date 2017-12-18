import fixtures
import testtools


class BaseTestCase(testtools.TestCase):

    def setUp(self):
        super(BaseTestCase, self).setUp()
        self.useFixture(fixtures.FakeLogger())
