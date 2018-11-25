#!/usr/bin/env python
import logging

fmt_str = '[%(asctime)s] %(filename)s %(levelname)s @ line %(lineno)d: %(message)s'
logging.basicConfig(filename="event.log", format=fmt_str, level=logging.DEBUG)
logger = logging.getLogger(__name__)

import click
from ac_lib.domain import ContactList
from ac_lib.service import *
from ac_lib.util import post_campaign

__author__ = "Cornelius Jemison <cornelius.jemison <at> gmail <dot> com>"

config = get_config()


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
    url = config['http']['list_url']
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
    url = config['http']['contact_list_url']
    logger.debug("url: %s" % (url,))
    response = post_contact_list(ContactList(list=list,
                                             contact=contact,
                                             status=status),
                                 url,
                                 api_token)
    if response:
        print response


@main.command()
@click.option('--type', '-t',
              prompt='Campaign Type',
              default='text',
              type=click.Choice(['single',
                                 'recurring',
                                 'split',
                                 'responder',
                                 'reminder',
                                 'special',
                                 'activerss',
                                 'text']),
              help='Campaign Type')
@click.option('--name', '-n',
              prompt='Campaign Name',
              type=str,
              help='Campaign Name')
@click.option('--schedule_date', '-sd',
              prompt='Campaign Schedule Date',
              type=str,
              help='Campaign Schedule Date - i.e 2018-11-24 15:56:00')
@click.option('--status', '-s',
              prompt='Campaign Status',
              type=click.Choice(['1', '2']),
              help='Campaign Status')
@click.option('--list_id', '-l',
              prompt='Campaign List Id',
              type=int,
              help='Campaign List Id')
@click.option('--message_id', '-m',
              prompt='Campaign Message Id',
              type=int,
              help='Campaign Message Id')
def create_campaign(type,
                    name,
                    schedule_date,
                    status,
                    list_id,
                    message_id):
    api_token = get_api_token()
    url = config['http']['campaign_url']
    c = Campaign(type=type,
                 name=name,
                 schedule_date=schedule_date,
                 status=status,
                 p_id=list_id,
                 message_id=message_id)
    d = c.to_dict()
    logger.debug("Campaign: %s" % (d,))
    print post_campaign(d, url, api_token)


@main.command()
@click.option('--fromname', '-fn',
              prompt='Message From Name',
              type=str,
              help='Message From Name')
@click.option('--fromemail', '-fe',
              prompt='Message From Email',
              type=str,
              help='Message From Email')
@click.option('--reply', '-r',
              prompt='Message Reply',
              type=str,
              help='Message Reply')
@click.option('--subject', '-s',
              prompt='Message Subject',
              type=str,
              help='Message Subject')
@click.option('--preheader_text', '-p',
              prompt='Message Pre Header',
              type=str,
              help='Message Pre Header')
@click.option('--message', '-m',
              prompt='Message',
              type=str,
              help='Message')
def create_message(fromname,
                   fromemail,
                   reply,
                   subject,
                   preheader_text,
                   message):
    api_token = get_api_token()
    url = config['http']['message_url']
    m = Message(from_name=fromname,
                from_email=fromemail,
                reply2=reply,
                subject=subject,
                preheader_text=preheader_text,
                message=message)
    print post_message(m, url, api_token)


@main.command()
def show_contacts():
    logger.debug("show contacts")
    api_token = get_api_token()
    url = config['http']['contact_url']
    for contact in get_contacts(url, api_token):
        print "Contact: %s" % (contact,)


@main.command()
def show_lists():
    logger.debug("show lists")
    api_token = get_api_token()
    url = config['http']['list_url']
    for l in get_lists(url, api_token):
        print "List: %s" % (l,)


@main.command()
def show_messages():
    logger.debug("show messages")
    api_token = get_api_token()
    url = config['http']['message_url']
    for l in get_messages(url, api_token):
        print "Message: %s" % (l,)


@main.command()
def show_campaigns():
    logger.debug("show messages")
    api_token = get_api_token()
    url = config['http']['campaign_url']
    for l in get_campaigns(url, api_token):
        print "Message: %s" % (l,)


if __name__ == "__main__":
    main()
