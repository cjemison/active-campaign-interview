#!/usr/bin/env python

import json
import logging

from validate_email import validate_email

import util
from domain import Contact, List

logger = logging.getLogger(__name__)


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


def to_contact_list_json(cl):
    d = {
        "contactList": {
            "list": int(cl.get_list()),
            "contact": int(cl.get_contact()),
            "status": int(cl.get_status())
        }
    }
    return json.dumps(d)


def post_list(l, url, api_token):
    logger.debug("list: %s url: %s" % (l, url,))
    if l and url and api_token:
        return util.post(url,
                         l,
                         api_token)
    return dict()


def post_contact_list(cl, url, api_token):
    logger.debug("Contact List: %s url: %s" % (cl, url,))
    if cl and url and api_token:
        return util.post(url,
                         to_contact_list_json(cl),
                         api_token)
    return dict()


def post_contact(contact, url, api_token):
    logger.debug("contact: %s url: %s", (contact, url,))
    if contact and url and api_token:
        return util.post(url,
                         to_contact_json(validate_contact(contact)),
                         api_token)
    return dict()


def validate_contact(contact):
    if not contact:
        raise ValueError("Contact is null.")
    util.validate_str(contact.get_first_name(), "First name is null or blank..")
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
