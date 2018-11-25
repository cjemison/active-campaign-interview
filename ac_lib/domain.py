#!/usr/bin/env python

# Objects are immutable.


class List:
    def __init__(self, id="",
                 name="",
                 stringid="",
                 sender_url="",
                 sender_reminder=""):
        self._id = id
        self._name = name
        self._stringid = stringid
        self._sender_url = sender_url
        self._sender_reminder = sender_reminder

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_stringid(self):
        return self._stringid

    def get_sender_url(self):
        return self._sender_url

    def get_sender_reminder(self):
        return self._sender_reminder

    def to_str(self):
        return "List(id=%s name=%s, stringid=%s. sender_url=%s," \
               " sender_reminder=%s" % \
               (self._id, self._name, self._stringid,
                self._sender_url, self._sender_reminder)

    def __repr__(self):
        return self.to_str()


class Contact:
    def __init__(self, id="",
                 first_name="",
                 last_name="",
                 email=""):
        self._id = id
        self._first_name = first_name
        self._last_name = last_name
        self._email = email

    def get_id(self):
        return self._id

    def get_first_name(self):
        return self._first_name

    def get_last_name(self):
        return self._last_name

    def get_email(self):
        return self._email

    def to_str(self):
        return "Customer(id=%s, first_name=%s, last_name=%s, email=%s)" % \
               (self._id, self._first_name, self._last_name, self._email,)

    def __repr__(self):
        return self.to_str()


class ContactList:
    def __init__(self, id="",
                 list="",
                 contact="",
                 status=""):
        self._id = id
        self._list = list
        self._contact = contact
        self._status = status

    def get_id(self):
        return self._id

    def get_list(self):
        return self._list

    def get_contact(self):
        return self._contact

    def get_status(self):
        return self._status

    def to_str(self):
        return "ContactList(id=%s, list=%s, contact=%s, " \
               "status=%s)" % \
               (self._id, self._list, self._contact, self._status)

    def __repr__(self):
        return self.to_str()


class Message:
    def __init__(self, id="",
                 message="",
                 from_name="",
                 from_email="",
                 reply2="",
                 subject="",
                 preheader_text=""):
        self._id = id
        self._message = message
        self._from_name = from_name
        self._from_email = from_email
        self._reply2 = reply2
        self._subject = subject
        self._preheader_text = preheader_text

    def get_id(self):
        return self._id

    def get_message(self):
        return self._message

    def get_from_name(self):
        return self._from_name

    def get_from_email(self):
        return self._from_email

    def get_reply2(self):
        return self._reply2

    def get_subject(self):
        return self._subject

    def get_preheader_text(self):
        return self._preheader_text

    def to_str(self):
        return "Message(id=%s, message=%s," \
               " from_name=%s, from_email=%s, subject=%s, reply=%s," \
               " preheader_text=%s)" % \
               (self._id,
                self._message,
                self._from_name,
                self._from_email,
                self._subject,
                self._reply2,
                self._preheader_text)

    def __repr__(self):
        return self.to_str()


class Campaign:
    def __init__(self, id="",
                 type="",
                 name="",
                 schedule_date="",
                 status="1",
                 public="1",
                 track_links="None",
                 p_id="",
                 message_id=""):
        self._id = id
        self._type = type
        self._name = name
        self._schedule_date = schedule_date
        self._status = status
        self._public = public
        self._track_links = track_links
        self._p_id = p_id
        self._message_id = message_id

    def get_id(self):
        return self._id

    def get_type(self):
        return self._type

    def get_name(self):
        return self._name

    def get_schedule_date(self):
        return self._schedule_date

    def get_public(self):
        return self._public

    def get_track_links(self):
        return self._track_links

    def get_p_id(self):
        return self._p_id

    def get_m_id(self):
        return self._m_id

    def to_dict(self):
        d = dict()
        d['name'] = self._name
        d['type'] = self._type
        d['sdate'] = self._schedule_date
        d['status'] = self._status
        d['public'] = self._public
        d['tracklinks'] = self._track_links
        d['p[1]'] = self._p_id
        d['m[1]'] = self._message_id
        return d

    def to_str(self):
        return "Campaign(id=%s, type=%s," \
               " name=%s, schedule_date=%s, public=%s, track_links=%s," \
               " list_id=%s, message_id=%s)" % \
               (self._id,
                self._type,
                self._name,
                self._schedule_date,
                self._public,
                self._track_links,
                self._p_id,
                self._message_id)

    def __repr__(self):
        return self.to_str()
