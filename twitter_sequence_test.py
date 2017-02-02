# -*- coding: utf-8 -*-

import unittest
from helpers import *
import xmlrpclib
import pytest

@pytest.mark.twitter
@pytest.mark.social
class Twitter_Full(unittest.TestCase):

    def setUp(self):
        self.server = xmlrpclib.Server(server_https(), transport=SpecialTransport())
        self.method_callers = self.server.__getattr__('Rambler::Id::Twitter::get_oauth_token')
        self.rsid = check_rsid()


    def test_01_twitter_get_oauth_token_positive_https(self):
        args_https = {"scheme": "https", "uri": "string"}
        # вызываем метод
        method_callers = self.server.__getattr__('Rambler::Id::Twitter::get_oauth_token')
        response_https = method_callers(args_https)
        assert response_https['status'] == 'OK' and bool(response_https.get('oauth_token')) is True, 'No token in ' \
                                                                                                     'https ' \
                                                                                                     'response::   ' \
                                                                                                     '%r' % response_https
        token = response_https['oauth_token']
        write_to_xml('tw_oauth_token', token)



    def test_03_create_twitter_web_session_positive(self):
        renew_oauths('webview_login_twitter.py')
        tw_oauth_verifier = from_xml("tw_oauth_verifier")
        tw_oauth_token = from_xml("tw_oauth_token")
        args = {"oauth_token": tw_oauth_token, 'oauth_verifier': tw_oauth_verifier}
        method_caller = self.server.__getattr__('Rambler::Id::create_twitter_web_session')
        response = method_caller(args)
        # print response
        assert response['status'] == 'OK', 'Session not created::   %r' % response



    def test_02_attach_acc_positive(self):
        renew_oauths('webview_login_twitter.py')
        method_caller = self.server.__getattr__('Rambler::Id::Twitter::attach_account')
        oauth_token = from_xml("tw_oauth_token")
        oauth_verifier = from_xml("tw_oauth_verifier")
        #renew_oauths()
        args = {"rsid": self.rsid, "oauth_token": oauth_token, "oauth_verifier": oauth_verifier}
        # вызываем метод
        response = method_caller(args)
        assert response['status'] == 'OK','Not OK in status::   %r' % response
        #print response
        tw_id = response['linked_account']['id']
        write_to_xml('id', tw_id)



    def test_04_load_profile_positive(self):
        method_caller = self.server.__getattr__('Rambler::Id::load_profile')
        args = {"rsid": self.rsid, "get_external_profiles": 1}
        response = method_caller(args)
        exist = False
        for list in response['profile']['external_profiles']:
            for dict in list:
                if dict['provider'] == 'twitter':
                    exist = True
        assert exist, 'No Twitter profile attached::   %r' % response
        # try:
        #     mdict = response['profile']['external_profiles'][0]
        #     assert 'id' in mdict['properties'].keys()
        # except KeyError:
        #     raise AssertionError, 'No external profiles when requested::   %r' % response



    def test_05_detach_account(self):
        method_caller = self.server.__getattr__('Rambler::Id::detach_external_account')
        tw_id = from_xml("id")
        args = {"rsid": self.rsid, "id": tw_id, "provider": "twitter"}
        response = method_caller(args)
        assert response['status'] == 'OK', 'Detach unsuccessful::   %r' % response