
'''
CONSTANTS AND ENVIRONMENT VARIABLES SETTING
'''

import os
import requests
import json
from typing import List, Dict
from dataclasses import dataclass


# Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

# Constants
CLIENT_ID = os.getenv('SPOTIFY_API_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_API_CLIENT_SECRET')

PLAYLIST_NAME = 'Discover Daily'
PLAYLIST_DESCRIPTION = (
    "If you would like to support Discoverify, consider visiting patreon.com/discoverify (COMPLETELY OPTIONAL). "
    "Daily music, curated for you based on your listening history. "
    "If you don't want to get this daily playlist anymore, you can unsubscribe at https://discoverifymusic.com"
)

@dataclass
class SpotifyAPIException(Exception):
    delete_user: bool






'''
MAIN CLASS
'''

class SpotifyHelper:


    @staticmethod
    async def get_new_access_token(refresh_token: str) -> str:

        details = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        result = requests.post('https://accounts.spotify.com/api/token', data=details)
        result_json = result.json()

        if 'error' in result_json and result_json['error'] == 'invalid_grant':
            raise SpotifyAPIException(True)

        return result_json['access_token']
    




    @staticmethod
    async def get_refresh_token(code: str, redirect_uri: str) -> str:
        
        details = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }

        result = requests.post('https://accounts.spotify.com/api/token', data=details)
        result_json = result.json()

        if 'error' in result_json and result_json['error'] == 'invalid_grant':
            raise SpotifyAPIException(True)

        return result_json['refresh_token']
