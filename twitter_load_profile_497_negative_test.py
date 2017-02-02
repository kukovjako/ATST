# -*- coding: utf-8 -*-

import unittest

from helpers import *

import pytest

@pytest.mark.twitter
@pytest.mark.social
class Twitter4LoadProfile(unittest.TestCase):

    def setUp(self):
        self.server = xmlrpclib.Server(server_https(), transport=SpecialTransport())
        self.method_caller = self.server.__getattr__('Rambler::Id::load_profile')
        self.rsid = check_rsid()

    # def test_1_load_profile_positive(self):
    #     args = {"rsid": self.rsid, "get_external_profiles": 1}
    #     response = self.method_caller(args)
    #     try:
    #         mdict = response['profile']['external_profiles'][0]
    #         assert 'id' in mdict['properties'].keys()
    #     except KeyError:
    #         raise AssertionError, 'No external profiles when requested::   %r' %response

    def test_load_profile_negative(self):
        args = {"rsid": self.rsid}
        # вызываем метод
        response = self.method_caller(args)
        #print response
        assert 'external_profiles' not in response['profile'].keys(), 'external profiles are in response, ' \
                                                                          'must be NOT::    %r' % response

    def test_load_profile_negative_norsid(self):
        response = self.method_caller()
        assert 'ERROR' in response['status'] and 'Need session' in response['error']['strerror'], 'Not a need session response::   %r' % response


if __name__ == "__main__":
    unittest.main()