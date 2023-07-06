# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2 import service_account
from dotenv import load_dotenv

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl", 
          "https://www.googleapis.com/auth/youtubepartner"]
#SERVICE_ACCOUNT_FILE = 'splendid-alpha-340001-cb68705c6230.json'
SERVICE_ACCOUNT_FILE = 'splendid-alpha-340001-8081732b89b2.json'

CHANNEL_ID=os.getenv('CHANNEL_ID')

credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.channels().list(
        part="id,snippet,contentDetails,statistics",
        #mine=True,
        id=CHANNEL_ID
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()