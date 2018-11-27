#!/usr/bin/env python

import glob
import json
import logging
import os

import configparser
import keyring
from validate_email import validate_email

import util
from domain import Campaign, Contact, ContactList, List, Message

logger = logging.getLogger(__name__)

APP_NAME = "active_campaign"
APP_ACCOUNT = "token"


def get_contacts(url, api_token):
    logger.debug("url: %s", (url,))
    l = list()
    if url and api_token:
        d = json.loads(util.get(url, api_token))
        for contact in d['contacts']:
            l.append(Contact(id=contact['id'],
                             first_name=contact['firstName'],
                             last_name=contact['lastName'],
                             email=contact['email']))

    return l


def get_contact_list(url, api_token):
    logger.debug("url: %s", (url,))
    l = list()
    if url and api_token:
        d = json.loads(util.get(url, api_token))
        for contact in d['contactLists']:
            l.append(ContactList(id=contact['id'],
                                 list=contact['list'],
                                 contact=contact['contact'],
                                 status=contact['status']))
    return l


def get_campaigns(url, api_token):
    logger.debug("url: %s", (url,))
    l = list()
    if url and api_token:
        d = json.loads(util.get(url, api_token))
        for campaign in d['campaigns']:
            l.append(Campaign(id=campaign['id'],
                              type=campaign['type'],
                              schedule_date=campaign['sdate'],
                              status=campaign['status'],
                              public=campaign['public'],
                              track_links=campaign['tracklinks']))

    return l


def get_messages(url, api_token):
    logger.debug("url: %s", (url,))
    l = list()
    if url and api_token:
        d = json.loads(util.get(url, api_token))
        for message in d['messages']:
            l.append(Message(id=message['id'],
                             from_name=message['fromname'],
                             from_email=message['fromemail'],
                             reply2=message['reply2'],
                             subject=message['subject'],
                             preheader_text=message['preheader_text'],
                             message=message['text']))

    return l


def get_lists(url, api_token):
    logger.debug("url: %s", (url,))
    l = list()
    if url and api_token:
        d = json.loads(util.get(url, api_token))
        for _l in d['lists']:
            l.append(List(id=_l['id'],
                          name=_l['name'],
                          stringid=_l['stringid'],
                          sender_url=_l['sender_url'],
                          sender_reminder=_l['sender_reminder']))
    return l


def to_contact_json(contact):
    logger.debug("contact: %s" % (contact,))
    d = {
        "contact": {
            "first_name": contact.get_first_name(),
            "last_name": contact.get_last_name(),
            "email": contact.get_email()
        }
    }
    return json.dumps(d)


def to_list_json(l):
    logger.debug("list: %s" % (l,))
    d = {
        "list": {
            "name": l.get_name().strip(),
            "stringid": l.get_stringid().strip(),
            "sender_url": l.get_sender_url().strip(),
        }
    }
    return json.dumps(d)


def to_contact_list_json(contact_list):
    d = {
        "contactList": {
            "list": int(contact_list.get_list()),
            "contact": int(contact_list.get_contact()),
            "status": int(contact_list.get_status())
        }
    }
    return json.dumps(d)


def to_message_json(m):
    d = {
        "message": {
            "fromname": m.get_from_name(),
            "fromemail": m.get_from_email(),
            "reply2": m.get_reply2(),
            "subject": m.get_subject(),
            "preheader_text": m.get_preheader_text()
        }
    }
    return json.dumps(d)


def post_list(l, url, api_token):
    logger.debug("list: %s url: %s" % (l, url,))
    if l and url and api_token:
        d = json.loads(util.post(url, to_list_json(l), api_token))
        return List(id=d['list']['id'],
                    name=d['list']['name'],
                    stringid=d['list']['stringid'])
    return dict()


def post_contact_list(cl, url, api_token):
    logger.debug("Contact List: %s url: %s" % (cl, url,))
    if cl and url and api_token:
        d = json.loads(util.post(url,
                                 to_contact_list_json(cl),
                                 api_token))
        return ContactList(id=d['contactList']['id'],
                           list=d['contactList']['list'],
                           contact=d['contactList']['contact'])

    return dict()


def post_contact(contact, url, api_token):
    logger.debug("contact: %s url: %s", (contact, url,))
    if contact and url and api_token:
        d = json.loads(util.post(url,
                                 to_contact_json(validate_contact(contact)),
                                 api_token))
        return Contact(id=d['contact']['id'],
                       first_name=d['contact']['firstName'],
                       last_name=d['contact']['lastName'],
                       email=d['contact']['email'])
    return dict()


def post_message(message, url, api_token):
    logger.debug("message: %s url: %s" % (message, url,))
    if message and url and api_token:
        return util.post(url,
                         to_message_json(validate_message(message)),
                         api_token)
    return dict()


def validate_contact(contact):
    logger.debug("contact: %s" % (contact,))
    if not contact:
        raise ValueError("Contact is null.")
    util.validate_str(contact.get_first_name(), "First name is null or blank.")
    util.validate_str(contact.get_last_name(), "Last name is null or blank.")
    if not contact.get_email() or not validate_email(contact.get_email()):
        raise ValueError("Invalid Email Address.")
    return contact


def validate_list(l):
    logger.debug("List: %s " % (l,))
    if not l:
        raise ValueError("AC List is null.")
    util.validate_str(l.get_name(), "AC List name is null or blank.")
    util.validate_str(l.get_stringid(), "AC List stringid is null or blank.")
    return l


def validate_message(m):
    logger.debug("Message: %s" % (m,))
    if not m:
        raise ValueError("Message null.")
    util.validate_str(m.get_from_email, "Message.from_email")
    return m


def get_api_token():
    logger.debug("get api token for ac")
    active_campaign_token = keyring.get_password(APP_NAME, APP_ACCOUNT)
    if not active_campaign_token:
        raise ValueError("No Active Campaign Token was found.")
    logging.debug("Active Campaign Token: %s" % (active_campaign_token,))
    return active_campaign_token


def get_config():
    base_path = os.path.dirname(__file__)
    file_path = os.path.abspath(os.path.join(base_path, "..", "config.ini"))
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    return config


if __name__ == "__main__":
    print os.path.join(os.path.abspath(__file__), os.pardir)
    config = configparser.ConfigParser()
    config.read(glob.glob(os.path.join('../', 'conf', 'config.ini')))
    for k in config.iterkeys():
        print k
