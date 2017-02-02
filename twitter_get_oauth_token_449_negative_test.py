# -*- coding: utf-8 -*-

import unittest
# import sys
#
# sys.path.append("../")
# sys.path.append("../vars.xml")
from helpers import *
import xmlrpclib

import pytest

@pytest.mark.twitter
@pytest.mark.social
class Twitter1GetOauthToken_negative(unittest.TestCase):

    def setUp(self):
        self.server = xmlrpclib.Server(server_http(), transport=SpecialTransport())
        self.servers = xmlrpclib.Server(server_https(), transport=SpecialTransport())
        self.method_caller = self.server.__getattr__('Rambler::Id::Twitter::get_oauth_token')
        self.method_callers = self.servers.__getattr__('Rambler::Id::Twitter::get_oauth_token')


    def test_01_twitter_get_oauth_token_positive_http(self):
        args_http = {"scheme": "http", "uri": "string"}
        #args_nouri = {"scheme": "https"}
        # вызываем метод
        response_http = self.method_caller(args_http)
        assert response_http['status'] == 'OK' and bool(response_http.get('oauth_token')) is True, 'No token in http response::  %r' % response_http

    def test_01_twitter_get_oauth_token_positive_nouri(self):
        args_nouri = {"scheme": "https"}
        # вызываем метод
        response_nouri = self.method_caller(args_nouri)
        assert response_nouri['status'] == 'OK' and bool(response_nouri.get('oauth_token')) is True, 'No token in nouri response::  %r' % response_nouri

    def test_02_twitter_get_oauth_token_negative_http(self):
        args_http = {"scheme": "http", "uri": 123}
        # вызываем метод
        response_http_n = self.method_caller(args_http)
        assert response_http_n['status'] == 'ERROR', 'not ERROR in incorrect http response::  %r' % response_http_n

    def test_02_twitter_get_oauth_token_negative_https(self):
        args_https = {"scheme": "https", "uri": 123}
        response_https_n = self.method_callers(args_https)
        assert response_https_n['status'] == 'ERROR', 'not ERROR in negative https response:: %r' % response_https_n

    def test_02_twitter_get_oauth_token_negative_scheme(self):
        args_invalid_scheme = {"scheme": "random", "uri": "string"}
        response_invalid_scheme = self.method_caller(args_invalid_scheme)
        assert response_invalid_scheme['status'] == 'ERROR', 'not ERROR in negative scheme response::  %r' % response_invalid_scheme


if __name__ == "__main__":
    unittest.main()
