
import httplib2
import os
import sys
import pandas as pd
import json
import requests
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow


def get_comment_threads(video_id):
    comments = []
    MISSING_CLIENT_SECRETS_MESSAGE = "WARNING: Please configure OAuth 2.0"
    YOUTUBE_READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"

    CLIENT_SECRETS_FILE = '\\client_secret.json'


    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE, scope=YOUTUBE_READONLY_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = Storage("\\Users\\User\\dev\\YTAnalysis\\channel\\lib\\retrieve.py-oauth2.json")

    credentials = storage.get()

    if credentials is None or credentials.invalid:
        flags = argparser.parse_args()
        credentials = run_flow(flow, storage, flags)

    # Trusted testers can download this discovery document from the developers page
    # and it should be in the same directory with the code.


    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    http=credentials.authorize(httplib2.Http()))

    i = 0
    x = 0
    status = True

    while status == True:

        results = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId=" + video_id + "&key=AIzaSyC2XkC45k19rk6YpZLoLYY5hH-r7jKi_mc&maxResults=100")
        results = results.json()

        if 'nextPageToken' not in results:
            pageToken = ''
            status = False

        else:
            pageToken = results['nextPageToken']
            results = requests.get("https://www.googleapis.com/youtube/v3/commentThreads?part=snippet%2Creplies&videoId=" + video_id + "&key=AIzaSyC2XkC45k19rk6YpZLoLYY5hH-r7jKi_mc&maxResults=100&pageToken" + pageToken)
            results = results.json()

        for elem in results['items']:
            comments.append(elem['snippet']['topLevelComment']['snippet']['textOriginal'])
            i+=1
            x+=1
            #load next page of comments
            if i == 99:
                print(x)
                i = 0
                break

        if x >=400:
            status = False

    df = pd.DataFrame({'comment':comments})
    return df
