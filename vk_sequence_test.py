import xmlrpclib
import unittest
import pytest
from helpers import *


@pytest.mark.vk
@pytest.mark.social
class LoginVKSequence(unittest.TestCase):
    def setUp(self):
        self.serverid = xmlrpclib.Server(server_https(), transport=SpecialTransport())


    def test_1_vk_create_session(self):
        renew_oauths('webview_login_vk.py')
        method_caller = self.serverid.__getattr__('Rambler::Id::create_oauth2_web_session')
        code = from_xml('vk_code')
        #code = '1e7956303af0b71a72'
        provider = 'vkontakte'
        args = {'code': code, 'provider': provider, 'redirect_uri': 'https%3A%2F%2Fid.rambler.ru%2Foauth-20%2F%3Fprovider%3Dvkontakte'}
        response = method_caller(args)
        print response
        assert 'OK' in response['status'] and len(response['rsid']) > 4, 'No session created for VK::    %r' % response


    def test_2_vk_attach(self):
        #renew_oauths('webview_login_vk.py')
        code = from_xml('vk_code')
        method_caller = self.serverid.__getattr__('Rambler::Id::attach_external_account')
        rsid = check_rsid()
        args = {'rsid': rsid, 'code': code, 'redirect_uri': 'https%3A%2F%2Fid.rambler.ru%2Foauth-20%2F%3Fprovider%3Dvkontakte', 'provider': 'vkontakte', 'credentials_name': 'Vkontakte'}
        #args = {'code': '533dac2b68088d576e', 'redirect_uri': 'https://id.rambler.ru', 'provider': 'vkontakte'}
        response = method_caller(args)
        #print response
        assert response['status'] == 'OK' and len(str(response["linked_account"])) > 10, 'VK account has not been attached::    %r' % response
        vk_id = response["linked_account"]["id"]
        write_to_xml('vk_id', vk_id)


    def test_3_load_profile_positive(self):
        rsid = check_rsid()
        method_caller = self.serverid.__getattr__('Rambler::Id::load_profile')
        args = {"rsid": rsid, "get_external_profiles": 1}
        response = method_caller(args)
        #print response
        exist = False
        for dict in response['profile']['external_profiles']:
            if dict['provider'] == 'vkontakte':
                exist = True
        assert exist, 'No attached VK profile found::   %r' % response


    def test_4_vk_detach(self):
        method_caller = self.serverid.__getattr__('Rambler::Id::detach_external_account')
        vk_id = from_xml("vk_id")
        rsid = check_rsid()
        args = {"rsid": rsid, "id": vk_id, "provider": "vkontakte"}
        response = method_caller(args)
        #print response
        assert response['status'] == 'OK' and response['profile']['result'] == 'deleted', 'Detach unsuccessful::   %r' % response


'''
https://oauth.vk.com/authorize?client_id=3210582&display=page&redirect_uri=https%3A%2F%2Fid.rambler.ru%2Foauth-20%2F%3Fprovider%3Dvkontakte&response_type=code&v=5.62&state=123456
'''
'''408195346'''
