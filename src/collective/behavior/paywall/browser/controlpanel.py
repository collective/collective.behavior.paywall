# -*- coding: utf-8 -*-
from collective.behavior.paywall import _
from collective.behavior.paywall.interfaces import IPaywallSettings
from plone.app.registry.browser import controlpanel


class PaywallSettingsEditForm(controlpanel.RegistryEditForm):
    """Control panel edit form."""

    schema = IPaywallSettings
    label = _(u'Paywall')
    description = _(u'Settings for the paywall.')


class PaywallSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    """Control panel form wrapper."""

    form = PaywallSettingsEditForm
