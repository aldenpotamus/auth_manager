#!/usr/bin/python

import http.client
import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import configparser

class AuthManager:
    CONFIG = None
    httplib2.RETRIES = 1

    # Maximum number of times to retry before giving up.
    MAX_RETRIES = 10

    # Explicitly tell the underlying HTTP transport library not to retry, since
    # we are handling retry logic ourselves.


    # Always retry when these exceptions are raised.
    RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
    http.client.IncompleteRead, http.client.ImproperConnectionState,
    http.client.CannotSendRequest, http.client.CannotSendHeader,
    http.client.ResponseNotReady, http.client.BadStatusLine)

    # Always retry when an apiclient.errors.HttpError with one of these status
    # codes is raised.
    RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

    # This OAuth 2.0 access scope allows an application to upload files to the
    # authenticated user's YouTube channel, but doesn't allow other types of access.
    YOUTUBE_UPLOAD_SCOPE = None
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    # This variable defines a message to display if the CLIENT_SECRETS_FILE is
    # missing.
    MISSING_CLIENT_SECRETS_MESSAGE = """
    WARNING: Please configure OAuth 2.0

    To make this sample run you will need to populate the client_secrets.json file
    found at:

    with information from the API Console
    https://console.developers.google.com/

    For more information about the client_secrets.json file format, please visit:
    https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    """

    VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")

    @staticmethod
    def get_authenticated_service(authID, clientSecretFile=None, config=None, scopes=[]):       
        args = argparser.parse_args()
        
        tokenPath = './'
        if 'AUTH_MANAGER' in config and 'authTokenDir' in config['AUTH_MANAGER']:
            tokenPath = config['AUTH_MANAGER']['authTokenDir'] 
        
        flow = flow_from_clientsecrets(os.path.join(tokenPath, clientSecretFile),
            scope=scopes,
            message=AuthManager.MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage(os.path.join(tokenPath, f'{authID}-oauth2.json'))
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            print(f'*********************CURRENT AUTH FOR {authID}*********************')
            credentials = run_flow(flow, storage, args)

        return build(AuthManager.YOUTUBE_API_SERVICE_NAME, AuthManager.YOUTUBE_API_VERSION,
                     http=credentials.authorize(httplib2.Http()))
