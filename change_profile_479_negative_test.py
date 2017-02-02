# -*- coding: utf-8 -*-
import unittest

from helpers import *


class NegativeProfile(unittest.TestCase):

    def setUp(self):
        serverid = xmlrpclib.Server(server_https(), transport=SpecialTransport())
        #file = open('rsid.txt')
        self.rsid = check_rsid()
        self.get_profile = serverid.__getattr__('Rambler::Id::get_profile')
        self.change_profile = serverid.__getattr__('Rambler::Id::change_profile')

    def test_future_birthday(self):
        now = time.time()
        future = now + 100000
        #change_profile = self.change_profile
        checkbd = self.change_profile({'rsid': self.rsid, 'birthday': int(future)})
        assert 'ERROR' in checkbd['status'] and 'Invalid birthday' in checkbd['error']['strerror'], \
                'Future birthday should not be accepted by API::   %r' % checkbd


    def test_gender_empty_negative(self):
        gender = self.change_profile({'rsid': self.rsid, 'gender': 'u'})
        profile = self.get_profile({'rsid': self.rsid})
        # тут проверка на то, что в профайл не должен прийти пол, после того, как мы отправили туда 'u'
        try:
            changed_gender = profile['profile']['gender']
            assert changed_gender == 'govno'
        except KeyError:
            pass
        except AssertionError:
            raise AssertionError('gender not changed to u::   %r' % changed_gender)

    def test_gender_negative(self):
        # негативная проверка на отправку других типов данных вместо пола
        response = self.change_profile({'rsid': self.rsid, 'gender': 1})
        assert 'ERROR' in response['status'] and 'Parameters do not fit contract' in response['error'][
                'strerror'], 'API accepted num as gender instead of string::   %r' %response

    def test_birthday_negative(self):
        # негативная проверка на отправку очень давней даты рождения
        birthday = self.change_profile({'rsid': self.rsid, 'birthday': -2082844801})
        get_birthday = self.get_profile({'rsid': self.rsid})
        assert 'birthday' not in get_birthday['profile'],'Birthday earlier than 01.01.1904 accepted by API::   ' \
                                                             '%r' % get_birthday


    def test_firstname_negative(self):
        # негативная проверка на отправку других типов данных вместо имени
        firstname = self.change_profile({'rsid': self.rsid, 'firstname': 999999999})
        assert 'ERROR' in firstname['status'] and '__foundSchemaViolations' in firstname.keys(), 'Api accepted ' \
                                                                                                     'num as ' \
                                                                                                     'firstname::   ' \
                                                                                                     '%r' % firstname

    def test_lastname_negative(self):
        # негативная проверка на отправку других типов данных вместо фамилии
        lastname = self.change_profile({'rsid': self.rsid, 'lastname': 999999999})
        assert 'ERROR' in lastname['status'] and '__foundSchemaViolations' in lastname.keys(), 'Api accepted num ' \
                                                                                                   'as lastname::   ' \
                                                                                                   '%r' % lastname

    def test_backupemail_negative(self):
        # негативная проверка на отправку других типов данных вместо бэкап имейла
        email = self.change_profile({'rsid': self.rsid, 'backup_email': 999999999})
        assert 'ERROR' in email['status'] and '__foundSchemaViolations' in email.keys(), 'Api accepted num as ' \
                                                                                             'backup_email::   %r' % \
                                                                                             email

    def tearDown(self):
        pass





if __name__ == "__main__":
    unittest.main()
