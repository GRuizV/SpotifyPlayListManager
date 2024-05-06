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
TOKENS_JSON_FILE_PATH = spotify_helper.TOKENS_JSON_FILE_PATH





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

        # Access token requesting
        token = spotify_helper.SpotifyHelper.request_token()

        headers = {
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"
        }

        # Sending the POST Request
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
    def get_spotify_uri(song_name:str, artist:str) -> str:

        '''This function retrieves the ID of a track'''

        # Input treatment
        song_name = song_name.replace(' ','%2520')
        artist = artist.replace(' ','%2520')

        # Example query: (Cicuta - Noiseferatu) 'https://api.spotify.com/v1/search?q=remaster%2520track%3Acicuta%2520artist%3Anoisefaratu&type=track&market=CO&offset=0'
        query = f'https://api.spotify.com/v1/search?q=remaster%2520track%3A{song_name}%2520artist%3A{artist}&type=track&market=CO&offset=0' # The response I need is - response['tracks']['items'][0]['uri'] -.
        
        # Access token requesting
        token = spotify_helper.SpotifyHelper.request_token()

        # Building the 'headers'
        headers = { 
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {token}"
        } 


        # Sending the GET Request
        try:            
            response = requests.get(url=query, headers=headers)
            response.raise_for_status()
            response_json = response.json()            

            #this are the songs that match the search above
            songs = response_json["tracks"]["items"]

            print(query)
            #this project only cared for the firs match ***(but mine could make a function to get the closest match)
            uri = songs[0]["uri"]

            return uri

        except Exception as e:

            print(e)
            return None
    

        




        
    
    # Step 5: Add the song into the new Spotify playlist
    @staticmethod
    def add_song_to_playlist():
        pass 





# # 'get_spotify_uri' functions testing
# art = 'Granuja'
# song = 'Días de Perros'

# print(f'\n{song.replace(' ', '%20')+'%20'}\n')

# test = CreatePlaylist.get_spotify_uri(artist=art, song_name=song)
# print(test)





