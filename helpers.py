# -*- coding: utf-8 -*-

import os
import time
import random
from random import randint
import imaplib
#import email
import xmlrpclib
import subprocess
#import xml.etree.ElementTree as ET
#from xml.dom.minidom import *
from xml.dom.minidom import parse as parsse
from xml.etree.ElementTree import parse
import string
try:
    from bs4 import BeautifulSoup
except ImportError:
    import BeautifulSoup

from xmlrpclib import ServerProxy, Transport, Error





def get_payload(method, args):
    methodname = '<methodName>'+method+'</methodName>'
    m = xmlrpclib.Marshaller()
    payload = m.dumps([args])
    xmlv = "<?xml version='1.0'?>"
    payload = xmlv + '<methodCall>' + methodname + payload + '</methodCall>'
    return payload

def get_data(req, text):
    soup = BeautifulSoup(req.text, 'xml')
    element = soup.find(text=str(text))
    elpar = element.find_parent().find_parent()
    token = elpar.find('string').text
    return token

def get_headers():
    return {'Host':'id.rambler.ru', 'Content-Type': 'text/xml'}


def from_xml(key):
    xml = parsse('vars.xml')
    item_to_get = xml.getElementsByTagName(str(key))[0].firstChild.nodeValue
    return item_to_get


def randomstring(n):
    rand = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))
    return str(rand)

def randomint():
    rand = randint(1, 1474268321)
    return rand


def check_rsid():
    server = xmlrpclib.Server(server_https(), transport=SpecialTransport())
    caller = server.__getattr__('Rambler::Id::get_profile_info')
    file = open('rsid.txt')
    init_rsid = file.read()
    resp = caller({"rsid": init_rsid})
    #print resp
    # print resp
    if resp['status'] == 'OK':
        #print 'rsid is fresh and clean, proceeding'
        return init_rsid
    elif resp['status'] == 'ERROR' and resp['requiredAction'] == 'NeedSession':
        rsid_caller = server.__getattr__('Rambler::Id::create_web_session')
        args = { 'login': 'lobanov_autotest', 'password': 'qweasd'}
        rsid_response = rsid_caller(args)
        new_rsid = rsid_response.get('rsid')
        rsid_file = open('rsid.txt', 'w')
        rsid_file.write(new_rsid)
        #print 'rsid appears to be rotten, updating'
        #print 'old rsid = ', init_rsid, 'updated to new = ', new_rsid
        return new_rsid
    else:
        print "some other error occured"



def create_tw_token():
    server = xmlrpclib.Server(server_https(), transport=SpecialTransport())
    method_caller = server.__getattr__('Rambler::Id::Twitter::get_oauth_token')
    args_nouri = {"scheme": "https"}
    response_nouri = method_caller(args_nouri)
    token = response_nouri['oauth_token']
    return token

def write_to_xml(tag, subj):
    xml = parse('vars.xml')
    tw = xml.findall(tag)
    tw[0].text = subj
    xml.write('vars.xml', xml_declaration=True)

def renew_oauths(file):
    init_stamp = os.stat('vars.xml').st_mtime
    p = subprocess.Popen(['xvfb-run --server-num=66 python ' + str(file)], shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print '** please wait for a while **'
    a = p.stdout.readlines()
    for line in a:
        print line
        assert 'xvfb-run: command not found' not in line, 'No XVFB installed. Please install first.'
    while init_stamp == os.stat('vars.xml').st_mtime:
        time.sleep(2)
        print 'waiting for changes to apply'


def send_mail(method):
    email = 'ramblerautotest' + '+' + str(random.randrange(1,100000)) + '@gmail.com'
    server = xmlrpclib.Server(server_https(), transport=SpecialTransport())
    #method = 'Rambler::Common::send_email_validation'
    method_caller = server.__getattr__(method)
    args = {'method': 'Rambler::Id::X::register_by_external_email', 'email': email, 'template':'mail-confirm-id'}
    response = method_caller(args)
    print response

def get_mail():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('ramblerautotest@gmail.com', 'Qweasd12')
    mail.list()
    mail.select("inbox")  # connect to inbox.
    result, data = mail.search(None, "ALL")
    ids = data[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    latest_email_id = id_list[-1]  # get the latest
    result, data = mail.uid('search', None, "ALL")  # search and return uids instead
    latest_email_uid = data[0].split()[-1]
    result, data = mail.uid('fetch', latest_email_uid, '(RFC822)')
    print 'fetching mail'
    message = data[0][1]
    # start parsing
    start_e_val = '&value='
    end_e_val = '#confirmemail'
    start_e_val_index = message.find(start_e_val) + len(start_e_val)
    end_e_val_index = message.find(end_e_val)
    e_value = message[start_e_val_index:end_e_val_index]
    # email id
    start_id_val = 'account/?id='
    end_id_val = '&value='
    start_id_val_index = message.find(start_id_val) + len(start_id_val)
    end_id_val_index = message.find(end_id_val)
    id_value = message[start_id_val_index:end_id_val_index]
    return id_value, e_value
    # write_to_xml('email_value', e_value)
    # write_to_xml('email_id', id_value)

def server_http():
    return 'http://' + from_xml('server') + '/rpc'

def server_https():
    return 'https://' + from_xml('server') + '/rpc'

class SpecialTransport(Transport):

    def send_request(self, connection, handler, request_body):
        try:
            import gzip
        except ImportError:
            gzip = None #python can be built without zlib/gzip support
        if self.accept_gzip_encoding and gzip:
            connection.putrequest("POST", handler, skip_host=True, skip_accept_encoding=True)
            connection.putheader("Accept-Encoding", "gzip")
            connection.putheader("Host", "id.rambler.ru")
        else:
            connection.putrequest("POST", handler, skip_host=True)
            connection.putheader("Host", "id.rambler.ru")