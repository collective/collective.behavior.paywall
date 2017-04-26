# -*- coding: utf-8 -*-
from collective.behavior.paywall.interfaces import IPaywallSettings
from collective.behavior.paywall.testing import INTEGRATION_TESTING
from collective.behavior.paywall.utils import paywall_enabled
from plone import api
from plone.app.testing import logout
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class UtilsTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IPaywallSettings)

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(self.portal, 'News Item', 'n1')

        self.settings.paywall_globally_enabled = True
        self.n1.paywall_enabled = True
        logout()
        assert paywall_enabled(self.n1)

    def test_paywall_disabled_for_authenticated_user(self):
        from plone.app.testing import login
        from plone.app.testing import TEST_USER_NAME
        login(self.portal, TEST_USER_NAME)
        self.assertFalse(paywall_enabled(self.n1))

    def test_paywall_behavior_not_applied(self):
        from collective.behavior.paywall.tests.utils import disable_paywall_behavior
        disable_paywall_behavior('News Item')
        self.assertFalse(paywall_enabled(self.n1))

    def test_paywall_globally_disabled(self):
        self.settings.paywall_globally_enabled = False
        self.assertFalse(paywall_enabled(self.n1))

    def test_paywall_locally_disabled(self):
        self.n1.paywall_enabled = False
        self.assertFalse(paywall_enabled(self.n1))
