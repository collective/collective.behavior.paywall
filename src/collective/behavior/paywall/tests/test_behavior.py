# -*- coding: utf-8 -*-
from collective.behavior.paywall.interfaces import IPaywall
from collective.behavior.paywall.testing import INTEGRATION_TESTING
from collective.behavior.paywall.tests.utils import disable_paywall_behavior
from plone import api
from plone.behavior.interfaces import IBehavior
from zope.component import queryUtility

import unittest


class PaywallBehaviorTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(self.portal, 'News Item', 'n1')

    def test_behavior_registration(self):
        registration = queryUtility(IBehavior, name=IPaywall.__identifier__)
        self.assertIsNotNone(registration)

    def test_paywall_behavior(self):
        self.assertTrue(IPaywall.providedBy(self.n1))
        disable_paywall_behavior('News Item')
        self.assertFalse(IPaywall.providedBy(self.n1))

    def test_fields(self):
        self.assertFalse(self.n1.paywall_enabled)
        self.n1.paywall_enabled = True
        self.assertTrue(self.n1.paywall_enabled)
