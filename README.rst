*************************
Paywall support for Plone
*************************

.. contents:: Table of Contents

Life, the Universe, and Everything
==================================

This package implements a behavior for Dexterity-based content types to add a paywall in your content.

Mostly Harmless
===============

.. image:: http://img.shields.io/pypi/v/collective.behavior.paywall.svg
   :target: https://pypi.python.org/pypi/collective.behavior.paywall

.. image:: https://img.shields.io/travis/collective/collective.behavior.paywall/master.svg
    :target: http://travis-ci.org/collective/collective.behavior.paywall

.. image:: https://img.shields.io/coveralls/collective/collective.behavior.paywall/master.svg
    :target: https://coveralls.io/r/collective/collective.behavior.paywall

Got an idea? Found a bug? Let us know by `opening a support ticket <https://github.com/collective/collective.behavior.paywall/issues>`_.

Don't Panic
===========

Installation
------------

To enable this package in a buildout-based installation:

#. Edit your buildout.cfg and add add the following to it:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        collective.behavior.paywall

After updating the configuration you need to run ''bin/buildout'', which will take care of updating your system.

Go to the 'Site Setup' page in a Plone site and click on the 'Add-ons' link.

Check the box next to ``Paywall Support`` and click the 'Activate' button.

Usage
-----

Go to 'Site Setup' and select 'Paywall'.

.. figure:: https://raw.githubusercontent.com/collective/collective.behavior.paywall/master/docs/controlpanel.png
    :align: center
    :height: 768px
    :width: 1024px

    The Paywall control panel configlet.

Go to 'Site Setup' and select 'Dexterity Content Types' and enable the 'Paywall' behavior in your content types.

Create a new item of the selected type and enable the paywall on it.

When an anonymous user access this specific item she will see only the first two paragraphs of the content (according to the default XPath selector) and a button labeled "Continue reading".

.. figure:: https://raw.githubusercontent.com/collective/collective.behavior.paywall/master/docs/paywall.png
    :align: center
    :height: 768px
    :width: 1024px

    The paywall in action.

When the user selects the button, the rest of the content will be shown.

Go to 'Site Setup' and select 'Dexterity Content Types' and enable the 'Paywall' behavior in your content types.

How does it work
----------------

The paywall is applied in a transform that modifies the response before publishing it.
The XPath expression in the configlet is used to select the last element of the HTML DOM to be shown.
By default, the second paragraph of the body text is the last element selected,
and all its siblings will be hidden by applying a class to them.

A button is inserted as the last element of the body text.
This button fires a JavaScript event that removed the class and hides the button itself.

The paywall is only applied to anonimous users.

Small CSS and JavaScript snippets are also inserted on each item behind the firewall.

The use of an XPath expression means that the final result could be affected by the markup.
We need to find out a way to validate this as part of a quality assurance process.

TODO
----

- Implement a preview option for logged in users to let them see if the result is what is expected
- Change the button for an arbitrary HTML configured in the configlet
- Implement a real paywall that removes the content instead of just hiding it
- Check accessibility
