# -*- test-case-name: knoboo.external.twisted.web2.test.test_cgi,knoboo.external.twisted.web2.test.test_http -*-
# See LICENSE for details.

"""
Various backend channel implementations for web2.
"""
from knoboo.external.twisted.web2.channel.cgi import startCGI
from knoboo.external.twisted.web2.channel.scgi import SCGIFactory
from knoboo.external.twisted.web2.channel.http import HTTPFactory
from knoboo.external.twisted.web2.channel.fastcgi import FastCGIFactory

__all__ = ['startCGI', 'SCGIFactory', 'HTTPFactory', 'FastCGIFactory']
