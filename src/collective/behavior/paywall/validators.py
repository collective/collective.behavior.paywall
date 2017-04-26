# -*- coding: utf-8 -*-
from lxml import etree
from zope.interface import Invalid


def is_xpath_expression(value):
    """Checks if value contains a valid XPath expression."""
    if value == u'':
        return True

    try:
        etree.XPath(value)
        return True
    except etree.XPathSyntaxError as e:
        raise Invalid(e.message)
