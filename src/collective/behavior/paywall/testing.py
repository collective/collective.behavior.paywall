# -*- coding: utf-8 -*-
"""Setup testing fixture."""
from collective.behavior.paywall.tests.utils import enable_paywall_behavior
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import collective.behavior.paywall
        self.loadZCML(package=collective.behavior.paywall)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'collective.behavior.paywall:default')
        enable_paywall_behavior('News Item')
        portal.portal_workflow.setDefaultChain('simple_publication_workflow')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name='collective.behavior.paywall:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name='collective.behavior.paywall:Functional')

ROBOT_TESTING = FunctionalTesting(
    bases=(FIXTURE, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name='collective.behavior.paywall:Robot',
)
