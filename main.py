#!/usr/bin/env python
import logging

import click
import configparser
import keyring

from ac_lib.domain import Contact, ContactList, List
from ac_lib.service import post_contact, get_contacts, \
    post_list, to_list_json, get_lists, post_contact_list

__author__ = "Cornelius Jemison <cornelius.jemison <at> gmail.com>"

fmt_str = '[%(asctime)s] %(filename)s %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(filename="event.log", format=fmt_str, level=logging.DEBUG)
logger = logging.getLogger(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

APP_NAME = "active_campaign"
APP_ACCOUNT = "token"


@click.group()
def main():
    logger.debug("Starting Active Campaign CLI")
    pass


@main.command()
@click.option('--first_name', '-f', prompt='First name', type=str, help='First Name')
@click.option('--last_name', '-l', prompt='Last name', type=str, help='Last Name')
@click.option('--email', '-e', prompt='Email Address', type=str, help='Email Address')
def create_contact(first_name, last_name, email):
    logger.debug("Creating contact")
    api_token = get_api_token()
    contact = Contact(first_name=first_name,
                      last_name=last_name,
                      email=email)
    logger.debug("Attempting to Create: %s", (contact,))
    url = config['http']['contact_url']
    logger.debug("url: %s" % (url,))
    response = post_contact(contact, url, api_token)
    if response:
        logging.info("Created Contact: %s %s" % (first_name, last_name,))


@main.command()
@click.option('--name', '-n', prompt='Name', type=str, help='Name of List')
@click.option('--stringid', '-id', prompt='String Id', type=str, help='String id of List')
@click.option('--sender_url', '-url', prompt='String Id', type=str, help='Sender Url')
@click.option('--sender_reminder', '-r', prompt='String Id', type=str, help='Sender Reminder')
def create_list(name, stringid, sender_url, sender_reminder):
    logger.debug("creating list")
    api_token = get_api_token()
    url = config['http']['create_list_url']
    logger.debug("url: %s" % (url,))
    l = to_list_json(List(name=name,
                          stringid=stringid,
                          sender_url=sender_url,
                          sender_reminder=sender_reminder))
    print post_list(l, url, api_token)


@main.command()
@click.option('--list', '-l', prompt='List Id', type=int, help='List Id')
@click.option('--contact', '-c', prompt='Contact Id', type=int, help='Contact Id')
@click.option('--status', '-s', prompt='Status', default='1', type=click.Choice(['1', '2']), help='Status')
def create_contact_list(list, contact, status):
    logger.debug("list: %s contact=%s status=%s" % (list, contact, status,))
    api_token = get_api_token()
    url = config['http']['create_contact_list_url']
    logger.debug("url: %s" % (url,))
    response = post_contact_list(ContactList(list=list,
                                             contact=contact,
                                             status=status),
                                 url,
                                 api_token)
    if response:
        print response


@main.command()
def show_contacts():
    logger.debug("show contacts")
    api_token = get_api_token()
    url = config['http']['list_contacts_url']
    for contact in get_contacts(url, api_token):
        print "Contact: %s" % (contact,)


@main.command()
def show_lists():
    logger.debug("show lists")
    api_token = get_api_token()
    url = config['http']['get_lists_url']
    for l in get_lists(url, api_token):
        print "List: %s" % (l,)


def get_api_token():
    logger.debug("get api token for ac")
    active_campaign_token = keyring.get_password(APP_NAME, APP_ACCOUNT)
    if not active_campaign_token:
        raise ValueError("No Active Campaign Token was found.")
    logging.debug("Active Campaign Token: %s" % (active_campaign_token,))
    return active_campaign_token


if __name__ == "__main__":
    main()
