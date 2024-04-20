# Step 1: Log into Youtube
# Step 2: Grab Liked Videos
# Step 3: Create a New Playlist
# Step 4: Search for the Song
# Step 5: Add this son into the new Spotify playlist

from dotenv import load_dotenv
import os
import json
import requests
import base64

# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_USR = os.getenv('SPOTIFY_USER')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')



class CreatePlaylist:
    
    # Step 1: Log into Youtube
    @staticmethod
    def get_youtube_client():
        pass
        

    # Step 2: Grab Liked Videos
    @staticmethod
    def get_liked_videos():
        pass
    

    # Step 3: Create a New Playlist
    @staticmethod
    def create_playlist() -> str:
        
        '''This function creates a new playlist and returns the new Playlist ID'''

        details = {
            "name" : "Youtube Liked Vids",
            "description" : "All Youtube Liked Videos Songs",
            "public" : False
        }
        
        query = f"https://api.spotify.com/v1/users/{SPOTIFY_USR}/playlists"

        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer"

        }


        response = requests.post(query, details)


    # Step 3.1: Get Token -> This is going to be a next step with working with a new and refreshed token case
    @staticmethod
    def get_access_token():
        pass










    # Step 4: Search for the Song
    @staticmethod
    def get_spotify_uri():
        pass

    
    # Step 5: Add the song into the new Spotify playlist
    @staticmethod
    def add_song_to_playlist():
        pass











auth_string = f'{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}'
auth_bytes = auth_string.encode('utf-8')
auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

url = 'https://accounts.spotify.com/api/token'

headers = {
    'Authorization' : f'Basic {auth_base64}',
    'Content-Type' : 'application/x-www-form-urlencoded'
}

data = {'grant_type' : "client_credentials"}

response = requests.post(url, headers=headers, data=data)

json_response = json.loads(response.content)

token = json_response['access_token']

print(token)