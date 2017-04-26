# -*- coding: utf-8 -*-
from collective.behavior.paywall.testing import INTEGRATION_TESTING
from collective.behavior.paywall.transforms import PaywallTransform
from glob import glob
from plone import api
from plone.app.testing import logout
from repoze.xmliter.utils import getHTMLSerializer

import lxml
import os
import unittest


class TransformerTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def _get_result(self, html):
        with open(html, 'r') as f:
            result = f.read()
        return getHTMLSerializer(result)

    def _walk_files(self):
        current_dir = os.path.abspath(os.path.dirname(__file__))
        html_dir = os.path.join(current_dir, 'html', '*')
        for html in glob(html_dir):
            if 'nopaywall' in html:
                continue
            result = self._get_result(html)
            yield result

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        with api.env.adopt_roles(['Manager']):
            self.n1 = api.content.create(self.portal, 'News Item', 'n1')

        self.n1.paywall_enabled = True
        self.request.response.setHeader('Content-Type', 'text/html')

        self.transformer = PaywallTransform(None, self.request)
        self.transformer.context = self.n1
        logout()

    def test_hide_siblings(self):
        transform = PaywallTransform(None, None)
        html = lxml.html.fromstring('<p>1</p><p>2</p><p>3</p>')
        e = html.xpath('//p[1]')[0]
        transform.hide_siblings(e)
        # '<p>1</p><p class="paywall">2</p><p class="paywall">3</p>'
        self.assertIsNone(html.xpath('//p[1]')[0].attrib.get('class', None))
        self.assertEqual(html.xpath('//p[2]')[0].attrib['class'], 'paywall')
        self.assertEqual(html.xpath('//p[3]')[0].attrib['class'], 'paywall')

    def test_add_paywall_button(self):
        transform = PaywallTransform(None, None)
        html = lxml.html.fromstring('<p>1</p><p>2</p><p>3</p>')
        e = html.xpath('//p[1]')[0]
        transform.add_paywall_button(e)
        # button is added as the last children of the parent
        # '<p>1</p><p>2</p><p>3</p><button id="paywall-button">foo</button>'
        button = html.xpath('//p[last()]')[0].getnext()
        self.assertEqual(button.tag, 'button')
        self.assertEqual(button.attrib['id'], 'paywall-button')
        self.assertEqual(button.text, 'Continue reading')
