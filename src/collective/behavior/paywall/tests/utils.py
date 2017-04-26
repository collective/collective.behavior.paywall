# -*- coding: utf-8 -*-
from collective.behavior.paywall.interfaces import IPaywall
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.schema import SchemaInvalidatedEvent
from zope.component import queryUtility
from zope.event import notify


def enable_paywall_behavior(portal_type):
    """Enable Paywall behavior on the specified portal type."""
    fti = queryUtility(IDexterityFTI, name=portal_type)
    behavior = IPaywall.__identifier__
    if behavior in fti.behaviors:
        return
    behaviors = list(fti.behaviors)
    behaviors.append(behavior)
    fti.behaviors = tuple(behaviors)
    notify(SchemaInvalidatedEvent(portal_type))


def disable_paywall_behavior(portal_type):
    """Enable Paywall behavior on the specified portal type."""
    fti = queryUtility(IDexterityFTI, name=portal_type)
    behavior = IPaywall.__identifier__
    if behavior not in fti.behaviors:
        return
    behaviors = list(fti.behaviors)
    behaviors.remove(behavior)
    fti.behaviors = tuple(behaviors)
    notify(SchemaInvalidatedEvent(portal_type))
