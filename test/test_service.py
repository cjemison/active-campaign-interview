import datetime
import sys
import uuid

import requests

sys.path.append("../")

from ac_lib.domain import Contact, List, ContactList, Message, Campaign
from ac_lib.service import get_config, get_contacts, get_api_token, \
    post_contact, get_lists, post_list, post_contact_list, \
    get_contact_list, get_messages, post_message

from ac_lib.util import post_campaign

rs = lambda: str(uuid.uuid4())


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


def delete_messages():
    config = get_config()
    url = config['http']['message_url']
    token = get_api_token()

    m = get_messages(url, token)
    if m:
        h = {
            'Accept': 'application/json',
            'Api-Token': token
        }
        for _l in m:
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
        assert new_contact.get_id() != ""
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
        assert new_l.get_id() != ""
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
        assert new_contact_list.get_id() != ""
        assert int(new_contact_list.get_list()) == int(l.get_id())
        assert int(new_contact_list.get_contact()) == int(c.get_id())
    finally:
        delete_contact_lists()
        delete_lists()
        delete_contacts()


def test_create_message():
    delete_messages()
    try:
        config = get_config()
        token = get_api_token()
        url = config['http']['message_url']

        m = Message(message=rs(),
                    from_name=rs(),
                    from_email="test@test.com",
                    reply2="test@test.com",
                    subject=rs(),
                    preheader_text=rs())

        new_message = post_message(m, url, token)
        assert new_message
        assert new_message.get_id()
        assert new_message.get_id() != ""
        assert new_message.get_from_email() == m.get_from_email()
        assert new_message.get_from_name() == m.get_from_name()
        assert new_message.get_reply2() == m.get_reply2()
        assert new_message.get_subject() == m.get_subject()
        assert new_message.get_preheader_text() == m.get_preheader_text()

    finally:
        delete_messages()


def test_campaign():
    delete_messages()
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
        assert c

        url = config['http']['list_url']
        l = post_list(List(name="test",
                           stringid="test"),
                      url,
                      token)
        assert l

        url = config['http']['contact_list_url']
        cl = post_contact_list(ContactList(list=l.get_id(),
                                           contact=c.get_id(),
                                           status="1"),
                               url,
                               token)
        assert cl

        url = config['http']['message_url']
        m = post_message(Message(message=rs(),
                                 from_name="Test Test",
                                 from_email="test@test.com",
                                 reply2="test@test.com",
                                 subject="Test Subject",
                                 preheader_text=rs()),
                         url,
                         token)
        assert m

        url = config['http']['campaign_url']
        date_str = (datetime.datetime.today() + datetime.timedelta(minutes=3)) \
            .strftime('%Y-%m-%d %H:%M:%S')

        campaign = Campaign(type="test",
                            name="Test Campaign",
                            schedule_date=date_str,
                            p_id=cl.get_id(),
                            m_id=m.get_id())

        d = campaign.to_dict()
        d['p[' + cl.get_id() + ']'] = cl.get_id()
        d['p[' + m.get_id() + ']'] = m.get_id()

        new_campaign = post_campaign(d, url, token)
        assert new_campaign
    finally:
        pass

    # delete_contact_lists()
    # delete_lists()
    # delete_contacts()
    # delete_messages()
