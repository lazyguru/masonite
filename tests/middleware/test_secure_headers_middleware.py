""" Test Secure Headers Midddleware """
import unittest

from masonite.middleware import SecureHeadersMiddleware
from masonite.request import Request
from masonite.testsuite import TestSuite, generate_wsgi


class TestSecureHeadersMiddleware(unittest.TestCase):

    def setUp(self):
        self.request = Request(generate_wsgi())
        self.middleware = SecureHeadersMiddleware(self.request)
        self.app = TestSuite().create_container().container
        self.app.bind('Request', self.request.load_app(self.app))
        self.request = self.app.make('Request')

    def test_secure_headers_middleware(self):
        self.middleware.after()
        self.assertEqual(self.request.header('Strict-Transport-Security'), 'max-age=63072000; includeSubdomains')
        self.assertEqual(self.request.header('X-Frame-Options'), 'SAMEORIGIN')

    def test_secure_headers_gets_middleware_from_the_config(self):
        self.request = self.app.make('Request')
        self.middleware.after()
        self.assertEqual(self.request.header('X-Content-Type-Options'), 'sniff-test')
