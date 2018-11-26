#!/usr/bin/env python

import sys
import uuid

sys.path.append("../")

from ac_lib.domain import Contact, List, Message, ContactList, Campaign

rs = lambda: uuid.uuid4()
space = " "
empty = ""


def test_contact():
    id = rs()
    first_name = rs()
    last_name = rs()
    email = "test@test.com"

    c = Contact(id=id,
                first_name=first_name,
                last_name=last_name,
                email="test@test.com")

    assert c.get_id() == id
    assert c.get_first_name() == first_name
    assert c.get_last_name() == last_name
    assert c.get_email() == email


def test_list():
    id = rs()
    name = rs()
    stringid = rs()
    sender_url = rs()
    sender_reminder = rs()

    l = List(id=id,
             name=name,
             stringid=stringid,
             sender_url=sender_url,
             sender_reminder=sender_reminder)

    assert l.get_id() == id
    assert l.get_name() == name
    assert l.get_stringid() == stringid
    assert l.get_sender_url() == sender_url
    assert l.get_sender_reminder() == sender_reminder


def test_message():
    id = rs()
    message = rs()
    from_name = rs()
    from_email = rs()
    reply2 = rs()
    subject = rs()
    preheader_text = rs()

    m = Message(id=id,
                message=message,
                from_name=from_name,
                from_email=from_email,
                reply2=reply2,
                subject=subject,
                preheader_text=preheader_text)

    assert m.get_id() == id
    assert m.get_message() == message
    assert m.get_from_name() == from_name
    assert m.get_from_email() == from_email
    assert m.get_reply2() == reply2
    assert m.get_subject() == subject
    assert m.get_preheader_text() == preheader_text


def test_contact_list():
    id = rs()
    _list = rs()
    contact = rs()
    status = rs()

    cl = ContactList(id=id,
                     list=_list,
                     contact=contact,
                     status=status)

    assert cl.get_id() == id
    assert cl.get_list() == _list
    assert cl.get_contact() == contact
    assert cl.get_status() == status


def test_campaign():
    id = rs()
    type = rs()
    name = rs()
    schedule_date = rs()
    status = rs()
    public = rs()
    track_links = rs()
    p_id = rs()
    message_id = rs()

    c = Campaign(id=id,
                 type=type,
                 name=name,
                 schedule_date=schedule_date,
                 status=status,
                 public=public,
                 track_links=track_links,
                 p_id=p_id,
                 m_id=message_id)

    assert c.get_id() == id
    assert c.get_type() == type
    assert c.get_name() == name
    assert c.get_schedule_date() == schedule_date
    assert c.get_status() == status
    assert c.get_public() == public
    assert c.get_track_links() == track_links
    assert c.get_p_id() == p_id
    assert c.get_m_id() == message_id
