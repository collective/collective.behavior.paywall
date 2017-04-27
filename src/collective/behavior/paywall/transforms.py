# -*- coding: utf-8 -*-
from collective.behavior.paywall.interfaces import IPaywallLayer
from collective.behavior.paywall.interfaces import IPaywallSettings
from collective.behavior.paywall.logger import logger
from collective.behavior.paywall.utils import paywall_enabled
from plone.registry.interfaces import IRegistry
from plone.transformchain.interfaces import ITransform
from repoze.xmliter.utils import getHTMLSerializer
from zope.component import adapter
from zope.component import getUtility
from zope.interface import implementer
from zope.interface import Interface

import lxml


# static resources
CSS = lxml.etree.fromstring('<style>.paywall { display: none; }</style>')
# custom parser to deal with the "&&" operator inside the JS code
js_parser = lxml.etree.XMLParser(resolve_entities=False, strip_cdata=False)
JS = lxml.etree.fromstring("""<script>
//<![CDATA[
function bypassPaywall() {
  var els = document.getElementsByClassName("paywall");
  while (els && els.length) {
    els[0].classList.remove("paywall");
  }
  document.getElementById("paywall-button").style.display = 'none';
}
window.onload = function() { document.getElementById("paywall-button").addEventListener("click", bypassPaywall); };
//]]>
</script>""", js_parser)

# TODO: make this configurable via configlet
BUTTON = '<button id="paywall-button">{label}</button>'


# XXX: can we register the transform in the context of Dexterity-based
#      context types only?
@implementer(ITransform)
@adapter(Interface, IPaywallLayer)
class PaywallTransform(object):
    """Paywall for Dexterity-based content types with behavior applied.

    Right now the paywall just hide the content via CSS and adds a
    button to show it again. In the future we could implement the
    actual removal of the content below the element specified.
    """

    order = 6666

    def __init__(self, published, request):
        self.published = published
        self.request = request
        self.context = getattr(published, 'context', None)
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(IPaywallSettings)

    def hide_siblings(self, element):
        """Hide all sibling elements after the last to be shown."""
        for e in element.itersiblings():
            classes = e.attrib.get('class', '').split(' ')
            classes.append('paywall')
            e.attrib['class'] = ' '.join(classes).strip()

    def add_paywall_button(self, element):
        """Add paywall button after the element."""
        button = lxml.html.fromstring(BUTTON.format(label=self.settings.button_text))
        element.getparent().append(button)

    def add_static_resources(self, result):
        """Add paywall CSS code on the head of the document."""
        head = result.tree.xpath('//head')[0]
        head.append(CSS)
        head.append(JS)

    @property
    def response_is_html(self):
        content_type = self.request.response.getHeader('Content-Type')
        if content_type:
            return content_type.startswith('text/html')

    def transformIterable(self, result, encoding):
        if not self.response_is_html:
            return

        if not paywall_enabled(self.context):
            return
        logger.debug('Paywall enabled in context')

        try:
            result = getHTMLSerializer(result)
        except (AttributeError, TypeError, lxml.etree.ParseError):
            logger.warn('Paywall transform failed')
            return

        element = result.tree.xpath(self.settings.xpath_expression)

        if not element:
            return
        element = element[0]

        # TODO: make this configurable via configlet: hide or remove
        self.hide_siblings(element)
        self.add_paywall_button(element)
        self.add_static_resources(result)

        return result
