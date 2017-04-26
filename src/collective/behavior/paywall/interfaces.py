# -*- coding: utf-8 -*-
from collective.behavior.paywall import _
from collective.behavior.paywall.config import DEFAULT_XPATH_EXPRESSION
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import Interface
from zope.interface import provider


class IPaywallLayer(Interface):
    """A layer specific for this add-on product."""


@provider(IFormFieldProvider)
class IPaywall(model.Schema):
    """Paywall behavior."""

    model.fieldset('paywall', label=_(u'Paywall'), fields=['paywall_enabled'])
    paywall_enabled = schema.Bool(
        title=_(u'Enable paywall'),
        description=_(u'Enable the paywall for this item.'),
        required=False,
        default=False,
    )


class IPaywallSettings(model.Schema):
    """Schema for the control panel form."""

    paywall_globally_enabled = schema.Bool(
        title=_(u'Enable paywall globally'),
        description=_(u'Enable the paywall on this site.'),
        required=False,
        default=False,
    )

    button_text = schema.TextLine(
        title=_(u'Button text'),
        description=_(u'Text to be shown in the button used to bypass the paywall.'),
        required=True,
        default=_(u'Continue reading'),
    )

    xpath_expression = schema.ASCIILine(
        title=_(u'XPath expression'),
        description=_(
            u'This expression is used to locate the last element to be shown. '
            u'All elements after this one will be held behind the paywall. '
            u'Default expression selects the second paragraph of the content.',
        ),
        required=True,
        default=DEFAULT_XPATH_EXPRESSION,
    )
