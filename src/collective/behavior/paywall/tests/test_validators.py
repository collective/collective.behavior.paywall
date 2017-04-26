# -*- coding: utf-8 -*-
from collective.behavior.paywall.config import DEFAULT_XPATH_EXPRESSION
from collective.behavior.paywall.validators import is_xpath_expression
from zope.interface import Invalid

import unittest


class ValidatorsTestCase(unittest.TestCase):

    def test_is_xpath_expression_empty_value(self):
        self.assertTrue(is_xpath_expression(''))

    def test_is_xpath_expression_valid_value(self):
        self.assertTrue(is_xpath_expression(DEFAULT_XPATH_EXPRESSION))

    def test_is_xpath_expression_invalid_value(self):
        with self.assertRaises(Invalid) as e:
            is_xpath_expression('//')
        self.assertEqual(e.exception.message, u'Invalid expression')
