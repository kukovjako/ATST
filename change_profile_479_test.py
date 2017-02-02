# -*- coding: utf-8 -*-
import unittest
import datetime

from helpers import *


class ChangeProfile(unittest.TestCase):

    def test_change_profile(self):
        serverid = xmlrpclib.Server(server_https(), transport=SpecialTransport())
        #file = open('rsid.txt')
        rsid = check_rsid()

        # Генерим пол 100% отличный от того, что сейчас в аккаунте
        method_caller = serverid.__getattr__('Rambler::Id::get_profile')
        response = method_caller({'rsid': rsid})
        genderlist = 'mf'
        try:
            initialgender = str(response['profile']['gender'])
            if initialgender == 'm':
                gender = 'f'
            elif initialgender == 'f':
                gender = 'm'
        except KeyError:
            gender = random.choice(genderlist)

        # Словарь рандомных значений:
        random_dict = {'rsid': rsid,  'firstname' : randomstring(7),  'backup_email' : randomstring(4) + '@' + randomstring(4)+'.ru',
            'gender' : str(gender), 'birthday' : randomint(), 'lastname' : randomstring(10),
                       'geoid': randomint()}

        # Сгенеренную рандомную юникс-дату приводим к человеческому формату для дальнейшего сравнения полученной
        # человеческой даты с этим говном:
        date = datetime.datetime.fromtimestamp(random_dict['birthday'])
        date = str(date.strftime('%Y-%m-%d'))

        # Меняем инфу об аккаунте:
        method_caller = serverid.__getattr__('Rambler::Id::change_profile')
        change = method_caller(random_dict)

        # Удаляем рсид и меняем дату рождения на человеческую.
        random_dict['birthday'] = date
        del random_dict['rsid']

        # Получаем измененную инфу
        method_caller = serverid.__getattr__('Rambler::Id::get_profile')
        response = method_caller({'rsid': rsid})
        changed_profile = response['profile']

        # Тут происходит сравнение полученных значений от апишки с той инфой, что мы отсылали:
        for key in random_dict:
            try:
                assert random_dict[key] == changed_profile[key]
            except AssertionError:
                raise AssertionError(str(key) + ' is not changed')



if __name__ == "__main__":
    unittest.main()