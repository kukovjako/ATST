# -*- coding: utf-8 -*-

import unittest

from helpers import *

import pytest

@pytest.mark.twitter
@pytest.mark.social
class Twitter5DetachAccount(unittest.TestCase):

    def setUp(self):
        self.server = xmlrpclib.Server(server_https(), transport=SpecialTransport())
        self.method_caller = self.server.__getattr__('Rambler::Id::detach_external_account')
        self.rsid = check_rsid()

    # def test_999_detach_account(self):
    #     tw_id = from_xml("id")
    #     args = {"rsid": self.rsid, "id": tw_id, "provider": "twitter"}
    #     response = self.method_caller(args)
    #     assert response['status'] == 'OK', 'Detach unsuccessful::   %r' % response

    def test_02_detach_acc_noid(self):
        args_noid = {"rsid": self.rsid, "provider": "twitter"}
        response_noid = self.method_caller(args_noid)
        #print response_noid
        assert response_noid['status'] == 'ERROR' and '__foundSchemaViolations' in response_noid.keys(), 'Not a correct error response for request with no id::    %r' % response_noid

    def test_03_detach_account_wrong_id(self):
        args_wrong_id = {"rsid": self.rsid, "id": "123123", "provider": "twitter"}
        response_wrong_id = self.method_caller(args_wrong_id)
        assert response_wrong_id['status'] == 'OK' and 'External profile not found' in response_wrong_id[
                'error']['strerror'], 'SOme external profile returned for request with wrong id::    %r' % response_wrong_id

    def test_04_detach_account_no_provider(self):
        tw_id = from_xml("id")
        args_no_provider = {"rsid": self.rsid, "id": tw_id}
        response_no_provider = self.method_caller(args_no_provider)
        #print response_no_provider
        assert response_no_provider['status'] == 'ERROR' and '__foundSchemaViolations' in response_no_provider.keys(), 'Not a correct error message for request with no provider::   %r' % response_no_provider

    def test_05_detach_account_wrong_provider(self):
        tw_id = from_xml("id")
        args_wrong_provider = {"rsid": self.rsid,  "id": tw_id, "provider": "facebook"}
        response_wrong_provider = self.method_caller(args_wrong_provider)
        #print response_wrong_provider
        assert response_wrong_provider['status'] == 'OK' and 'External profile not found' in response_wrong_provider[
                'error']['strerror'], 'Not a correct error message for request with wrong provider::   %r' % response_wrong_provider



if __name__ == "__main__":
    unittest.main()
