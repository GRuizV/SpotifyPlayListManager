# Step 1: Log into Youtube
# Step 2: Grab Liked Videos
# Step 3: Create a New Playlist
# Step 4: Search for the Song
# Step 5: Add this son into the new Spotify playlist

import os
import json, requests, base64
import spotify_helper
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_USER = os.getenv('SPOTIFY_USER')
TOKENS_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Bukola YT PJ\tokens.json'







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
            "public" : True
        }
        
        query = f"https://api.spotify.com/v1/users/{SPOTIFY_USER}/playlists"

        with open(TOKENS_JSON_FILE_PATH) as f:
            data = json.load(f)
            token = data['access_token']
            expiration_time = datetime.fromisoformat(data['expiration_time'][:-1])  #The [:-1] is to take out the 'Z' parameter given we are computing this time later


        # Checking if token refreshing is needed
        if expiration_time < datetime.now() + timedelta(minutes=5):
            token, refresh_token = spotify_helper.SpotifyHelper.refresh_token(data['refresh_token'])

        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"
        }

        try:            
            response = requests.post(url=query, data=json.dumps(details), headers=headers)
            response.raise_for_status()
            response_json = response.json()            

            #Returning the ID of the newly created playlist
            return response_json['id']

        except Exception as e:

            print(e)
            return None

      







    # Step 4: Search for the Song
    @staticmethod
    def get_spotify_uri():
        pass

    
    # Step 5: Add the song into the new Spotify playlist
    @staticmethod
    def add_song_to_playlist():
        pass








