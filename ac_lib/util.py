#!/usr/bin/env python
import json
import logging
import urllib
import urllib2

import requests

logger = logging.getLogger(__name__)


def list_errors(response):
    logger.warning(response.status_code)
    logger.warning(response.text)
    d = json.loads(response.text)
    for error in d['errors']:
        logger.warning("Error: %s" % (error['title']))


def get(url, token):
    logger.debug("url: %s token: %s" % (url, token,))
    if url and token:
        headers = {
            'Accept': 'application/json',
            'Api-Token': token
        }
        logger.info("GET: %s" % (url,))
        response = requests.get(url, headers=headers)
        if response and response.status_code == 200:
            return response.text
        else:
            list_errors(response)

    return dict()


def post(url, body="", token=""):
    logger.debug("url: %s token: %s body: %s" % (url, token, body,))
    if body and token:
        headers = {
            'Accept': 'application/json',
            'ContentType': 'application/json',
            'Api-Token': token
        }
        logger.info("POST: %s  %s" % (url, body,))
        response = requests.post(url, data=body, headers=headers)
        if response and (response.status_code == 201 or response.status_code == 200):
            return response.text
        else:
            list_errors(response)


def validate_str(val="", message=""):
    if not val or val.strip() == "":
        raise ValueError(message)


def post_campaign(post_data, url, token=""):
    request_url = '%s/admin/api.php?&api_action=campaign_create&api_output=%s&api_key=%s' % (url,
                                                                                             "json",
                                                                                             token,)
    logger.debug("request_url: %s" % (request_url,))
    post_data = urllib.urlencode(post_data)
    req = urllib2.Request(request_url, post_data)
    response = json.loads(urllib2.urlopen(req).read())
    logger.debug("Response: %s" % (response,))
    return response


def post_contact_list(post_data, url, token=""):
    request_url = '%s/admin/api.php?&api_action=campaign_create&api_output=%s&api_key=%s' % (url,
                                                                                             "json",
                                                                                             token,)
    logger.debug("request_url: %s" % (request_url,))
    post_data = urllib.urlencode(post_data)
    req = urllib2.Request(request_url, post_data)
    response = json.loads(urllib2.urlopen(req).read())
    logger.debug("Response: %s" % (response,))
    return response
