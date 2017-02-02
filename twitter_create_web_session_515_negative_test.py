# -*- coding: utf-8 -*-

import unittest
from helpers import *


import pytest

@pytest.mark.twitter
@pytest.mark.social
class Twitter2CreateWebSession(unittest.TestCase):

    def setUp(self):
        self.server = xmlrpclib.Server(server_https(), transport=SpecialTransport())
        self.method_caller = self.server.__getattr__('Rambler::Id::create_twitter_web_session')
        # self.tw_oauth_token = from_xml("tw_oauth_token")
        # self.tw_oauth_verifier = from_xml("tw_oauth_verifier")

    # def test_01_create_twitter_web_session_positive(self):
    #     renew_oauths()
    #     tw_oauth_verifier = from_xml("tw_oauth_verifier")
    #     tw_oauth_token = from_xml("tw_oauth_token")
    #     args = {"oauth_token": tw_oauth_token, 'oauth_verifier': tw_oauth_verifier}
    #     response = self.method_caller(args)
    #     # print response
    #     assert response['status'] == 'OK', 'Session not created::   %r' % response

    def test_02_create_twitter_web_session_negative(self):
        tw_oauth_token = from_xml("tw_oauth_token")
        tw_oauth_verifier = from_xml("tw_oauth_verifier")
        args = { "oauth_token": tw_oauth_token, 'oauth_verifier': tw_oauth_verifier}
        # вызываем метод
        response = self.method_caller(args)
        #print response
        # print response
        assert response['status'] == 'ERROR', 'Status is not ERROR::   %r' % response

    def test_03_create_bad_scheme_negative(self):
        tw_oauth_verifier = from_xml("tw_oauth_verifier")
        rsid = check_rsid()
        args = {'rsid': rsid, 'oauth_verifier': tw_oauth_verifier}

        # вызываем метод
        response = self.method_caller(args)
        # print response
        assert response['status'] == 'ERROR' and '__foundSchemaViolations' in response.keys(), 'Not a correct response, ' \
                                                                                            'when ' \
                                                                                            '__foundSchemaViolations ' \
                                                                                            'needed::   %r' % response


if __name__ == "__main__":
    unittest.main()
