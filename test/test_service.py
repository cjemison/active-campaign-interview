import sys

import requests

sys.path.append("../")

from ac_lib.domain import Contact, List
from ac_lib.service import get_config, get_contacts, get_api_token, \
    post_contact, get_lists, post_list


def delete_contacts():
    config = get_config()
    url = config['http']['contact_url']
    token = get_api_token()

    l = get_contacts(url, token)
    if l:
        h = {
            'Accept': 'application/json',
            'Api-Token': token
        }
        for c in l:
            del_url = "%s/%s" % (url, c.get_id(),)
            r = requests.delete(del_url, headers=h)
            assert r.status_code == 200


def delete_lists():
    config = get_config()
    url = config['http']['list_url']
    token = get_api_token()

    l = get_lists(url, token)
    if l:
        h = {
            'Accept': 'application/json',
            'Api-Token': token
        }
        for _l in l:
            del_url = "%s/%s" % (url, _l.get_id(),)
            r = requests.delete(del_url, headers=h)
            assert r.status_code == 200


def test_create_contact():
    delete_contacts()
    try:
        config = get_config()
        url = config['http']['contact_url']
        token = get_api_token()
        c = Contact(first_name="Test",
                    last_name="Test",
                    email="test@test.com")
        new_contact = post_contact(c, url, token)
        assert new_contact
        assert new_contact.get_id()
        assert new_contact.get_first_name() == "Test"
        assert new_contact.get_last_name() == "Test"
        assert new_contact.get_email() == "test@test.com"
    finally:
        delete_contacts()


def test_create_list():
    delete_lists()
    try:
        config = get_config()
        url = config['http']['list_url']
        token = get_api_token()
        l = List(name="test",
                 stringid="test")
        new_l = post_list(l, url, token)
        assert new_l
        assert new_l.get_name() == "test"
        assert new_l.get_stringid() == "test"
    finally:
        delete_lists()
