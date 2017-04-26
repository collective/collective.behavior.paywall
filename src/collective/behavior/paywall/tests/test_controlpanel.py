# -*- coding: utf-8 -*-
from collective.behavior.paywall.config import DEFAULT_XPATH_EXPRESSION
from collective.behavior.paywall.config import PROJECTNAME
from collective.behavior.paywall.interfaces import IPaywallSettings
from collective.behavior.paywall.testing import INTEGRATION_TESTING
from plone import api
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

import unittest


class ControlPanelTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.controlpanel = self.portal['portal_controlpanel']

    def test_controlpanel_has_view(self):
        view = api.content.get_view(u'paywall-settings', self.portal, self.request)
        view = view.__of__(self.portal)
        self.assertTrue(view())

    def test_controlpanel_view_is_protected(self):
        from AccessControl import Unauthorized
        from plone.app.testing import logout
        logout()
        with self.assertRaises(Unauthorized):
            self.portal.restrictedTraverse('@@paywall-settings')

    def test_controlpanel_installed(self):
        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertIn('paywall', actions)

    def test_controlpanel_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']

        with api.env.adopt_roles(['Manager']):
            qi.uninstallProducts(products=[PROJECTNAME])

        actions = [
            a.getAction(self)['id'] for a in self.controlpanel.listActions()]
        self.assertNotIn('paywall', actions)


class RegistryTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.registry = getUtility(IRegistry)
        self.settings = self.registry.forInterface(IPaywallSettings)

    def test_paywall_globally_enabled_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'paywall_globally_enabled'))
        self.assertFalse(self.settings.paywall_globally_enabled)

    def test_button_text_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'button_text'))
        self.assertEqual(self.settings.button_text, u'Continue reading')

    def test_xpath_expression_record_in_registry(self):
        self.assertTrue(hasattr(self.settings, 'xpath_expression'))
        self.assertEqual(
            self.settings.xpath_expression, DEFAULT_XPATH_EXPRESSION)

    def test_records_removed_on_uninstall(self):
        qi = self.portal['portal_quickinstaller']
        qi.uninstallProducts(products=[PROJECTNAME])

        records = [
            IPaywallSettings.__identifier__ + '.paywall_globally_enabled',
            IPaywallSettings.__identifier__ + '.button_text',
            IPaywallSettings.__identifier__ + '.xpath_expression',
        ]

        for r in records:
            self.assertNotIn(r, self.registry)
