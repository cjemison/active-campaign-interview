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
        return "List(id=%s name=%s, stringid=%s. sender_url=%s, sender_reminder=%s" % \
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
        return "ContactList(id=%s, list=%s, contact=%s, status=%s)" % \
               (self._id, self._list, self._contact, self._status)

    def __repr__(self):
        return self.to_str()


if __name__ == "__main__":
    a = Contact(first_name="John",
                last_name="Smith",
                email="john.smith@yahoo.com")
    print "Customer: %s" % (a,)

    a = List(name="testList",
             stringid="This is a string id.",
             sender_url="http://www.google.com",
             sender_reminder="This is a remeinder text")
