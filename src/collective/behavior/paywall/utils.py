# -*- coding: utf-8 -*-
from collective.behavior.paywall.interfaces import IPaywall
from collective.behavior.paywall.interfaces import IPaywallSettings
from plone import api


def paywall_enabled(context):
    """Checks if the paywall is enabled in the context, that is:

    - user is anonymous
    - paywall behavior is applied in the context
    - paywall is enabled globally
    - paywall is enabled in the context
    """
    if not api.user.is_anonymous():
        return False

    if not IPaywall.providedBy(context):
        return False

    globally_enabled = api.portal.get_registry_record(
        interface=IPaywallSettings, name='paywall_globally_enabled')
    if not globally_enabled:
        return False

    return context.paywall_enabled
