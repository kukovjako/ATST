# -*- coding: utf-8 -*-

import unittest

from helpers import *

import pytest

@pytest.mark.twitter
@pytest.mark.social
class Twitter3AttachAccount(unittest.TestCase):

    def setUp(self):
        self.server = xmlrpclib.Server(server_https(), transport=SpecialTransport())
        self.method_caller = self.server.__getattr__('Rambler::Id::Twitter::attach_account')
        self.rsid = check_rsid()

    # def test_01_attach_acc_positive(self):
    #     renew_oauths()
    #     oauth_token = from_xml("tw_oauth_token")
    #     oauth_verifier = from_xml("tw_oauth_verifier")
    #     #renew_oauths()
    #     args = {"rsid": self.rsid, "oauth_token": oauth_token, "oauth_verifier": oauth_verifier}
    #     # вызываем метод
    #     response = self.method_caller(args)
    #     assert response['status'] == 'OK','Not OK in status::   %r' % response
    #     #print response
    #     tw_id = response['linked_account']['id']
    #     write_to_xml('id', tw_id)

    def test_02_attach_acc_wrong_tokens_negative(self):
        args = {"rsid": self.rsid, "oauth_token": 123123, "oauth_verifier": 123123}
        # вызываем метод
        response = self.method_caller(args)
        #print response
        assert response['status'] == 'ERROR' and '__foundSchemaViolations' in response.keys(), 'not a correct error message for invalid tokens response::   %r' % response

if __name__ == "__main__":
    unittest.main()


