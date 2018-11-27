import sys

import requests

sys.path.append("../")

from ac_lib.domain import Contact, List, ContactList
from ac_lib.service import get_config, get_contacts, get_api_token, \
    post_contact, get_lists, post_list, post_contact_list, \
    get_contact_list


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


def delete_contact_lists():
    config = get_config()
    url = config['http']['contact_list_url']
    token = get_api_token()

    l = get_contact_list(url, token)
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


def test_create_contact_list():
    delete_contact_lists()
    delete_lists()
    delete_contacts()
    try:
        config = get_config()
        token = get_api_token()

        url = config['http']['contact_url']
        c = post_contact(Contact(first_name="Test",
                                 last_name="Test",
                                 email="test@test.com"),
                         url,
                         token)

        url = config['http']['list_url']
        l = post_list(List(name="test",
                           stringid="test"),
                      url,
                      token)

        cl = ContactList(list=l.get_id(),
                         contact=c.get_id(),
                         status="1")

        url = config['http']['contact_list_url']
        new_contact_list = post_contact_list(cl, url, token)
        assert new_contact_list
        assert new_contact_list.get_id()
        assert int(new_contact_list.get_list()) == int(l.get_id())
        assert int(new_contact_list.get_contact()) == int(c.get_id())
    finally:
        delete_contact_lists()
        delete_lists()
        delete_contacts()
