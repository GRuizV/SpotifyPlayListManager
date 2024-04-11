
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
    


    @staticmethod
    async def get_liked(track_ids, access_token):

        response = requests.get(
            f"https://api.spotify.com/v1/me/tracks/contains?ids={','.join(track_ids)}",
            headers={"Authorization": f"Bearer {access_token}"}
        )
        return response.json()
    



    @staticmethod
    async def get_recommendation_urls(user, seeds):

        base_url = 'https://api.spotify.com/v1/recommendations?limit=50'

        if seeds['artists']:
            base_url += f'&seed_artists={",".join(seeds["artists"])}'

        if seeds['tracks']:
            base_url += f'&seed_tracks={",".join(seeds["tracks"])}'

        min_max_url = base_url + f'&min_acousticness={user["playlistOptions"]["acousticness"][0]/100}&max_acousticness={user["playlistOptions"]["acousticness"][1]/100}'
        min_max_url += f'&min_danceability={user["playlistOptions"]["danceability"][0]/100}&max_danceability={user["playlistOptions"]["danceability"][1]/100}'
        min_max_url += f'&min_energy={user["playlistOptions"]["energy"][0]/100}&max_energy={user["playlistOptions"]["energy"][1]/100}'
        min_max_url += f'&min_instrumentalness={user["playlistOptions"]["instrumentalness"][0]/100}&max_instrumentalness={user["playlistOptions"]["instrumentalness"][1]/100}'
        min_max_url += f'&min_popularity={user["playlistOptions"]["popularity"][0]}&max_popularity={user["playlistOptions"]["popularity"][1]}'
        min_max_url += f'&min_valence={user["playlistOptions"]["valence"][0]/100}&max_valence={user["playlistOptions"]["valence"][1]/100}'

        target_url = base_url + f'&target_acousticness={(user["playlistOptions"]["acousticness"][0]+user["playlistOptions"]["acousticness"][1])/200}'
        target_url += f'&target_danceability={(user["playlistOptions"]["danceability"][0]+user["playlistOptions"]["danceability"][1])/200}'
        target_url += f'&target_energy={(user["playlistOptions"]["energy"][0]+user["playlistOptions"]["energy"][1])/200}'
        target_url += f'&target_instrumentalness={(user["playlistOptions"]["instrumentalness"][0]+user["playlistOptions"]["instrumentalness"][1])/200}'
        target_url += f'&target_popularity={round((user["playlistOptions"]["popularity"][0]+user["playlistOptions"]["popularity"][1])/2)}'
        target_url += f'&target_valence={(user["playlistOptions"]["valence"][0]+user["playlistOptions"]["valence"][1])/200}'

        return {'minMaxUrl': min_max_url, 'targetUrl': target_url}
    
    


    '-'










