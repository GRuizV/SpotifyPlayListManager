
'''
CONSTANTS AND ENVIRONMENT VARIABLES SETTING
'''

import os
import requests
import json
from typing import List, Dict
from dataclasses import dataclass
import random


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




    @staticmethod
    async def get_top(type, range, access_token):

        try:
            response = requests.get(
                f"https://api.spotify.com/v1/me/top/{type}?limit=20&time_range={range}",
                headers={
                    "Authorization": f"Bearer {access_token}"
                }
            )
            response.raise_for_status()
            result_json = response.json()
            return [item["id"] for item in result_json["items"]]
        
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return []




    @staticmethod
    async def get_all_top(range, access_token):
        
        try:
            top_tracks = await SpotifyHelper.get_top("tracks", range, access_token)
            top_artists = await SpotifyHelper.get_top("artists", range, access_token)
            return {"topTracks": top_tracks, "topArtists": top_artists}

        except Exception as e: 
            print(f"Error fetching all top tracks and artists: {e}")
            return {"topTracks": [], "topArtists": []}
        
    

    @staticmethod
    def get_seeds(playlist_options, top):

        artists = []
        tracks = []

        for seed in playlist_options['seeds']:

            if seed == 'AT':
                if top['allTime']['tracks']:
                    index = random.randint(0, len(top['allTime']['tracks']) - 1)
                    tracks.append(top['allTime']['tracks'].pop(index))

            elif seed == 'MT':
                if top['mediumTerm']['tracks']:
                    index = random.randint(0, len(top['mediumTerm']['tracks']) - 1)
                    tracks.append(top['mediumTerm']['tracks'].pop(index))

            elif seed == 'ST':
                if top['shortTerm']['tracks']:
                    index = random.randint(0, len(top['shortTerm']['tracks']) - 1)
                    tracks.append(top['shortTerm']['tracks'].pop(index))

            elif seed == 'AA':
                if top['allTime']['artists']:
                    index = random.randint(0, len(top['allTime']['artists']) - 1)
                    artists.append(top['allTime']['artists'].pop(index))

            elif seed == 'MA':
                if top['mediumTerm']['artists']:
                    index = random.randint(0, len(top['mediumTerm']['artists']) - 1)
                    artists.append(top['mediumTerm']['artists'].pop(index))

            elif seed == 'SA':
                if top['shortTerm']['artists']:
                    index = random.randint(0, len(top['shortTerm']['artists']) - 1)
                    artists.append(top['shortTerm']['artists'].pop(index))

            else:
                raise ValueError(f"Unexpected seed value found: {seed}")

        return {'artists': artists, 'tracks': tracks}