# Step 1: Log into Youtube
# Step 2: Grab Liked Videos
# Step 3: Create a New Playlist
# Step 4: Search for the Song
# Step 5: Add this son into the new Spotify playlist

import os
import json, requests
import spotify_helper
from dotenv import load_dotenv
import googleapiclient.errors
import google_auth_oauthlib.flow
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request




# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_USER = os.getenv('SPOTIFY_USER')
SPOTIFY_TOKENS_JSON_FILE_PATH = spotify_helper.SPOTIFY_TOKENS_JSON_FILE_PATH
YT_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Ref Projects\Bukola YT PJ\youtube_client_secrets.json'
PROJECTS_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Ref Projects\Bukola YT PJ'




class CreatePlaylist:
    
    # Step 1: Log into Youtube
    @staticmethod
    def get_youtube_client() -> googleapiclient.discovery.build:

        '''This function authenticates the user using OAuth 2.0 and returns a service object for the YouTube API.'''
            
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"
        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = YT_JSON_FILE_PATH
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]


        # Load credentials from file if available
        tokens_file_path = os.path.join(PROJECTS_PATH, 'youtube_tokens.json')
        creds = None

        if os.path.exists(tokens_file_path):
            creds = Credentials.from_authorized_user_file(tokens_file_path)


        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                
            else:
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(tokens_file_path, 'w') as token:
                token.write(creds.to_json())


        # Build the service
        youtube_client = googleapiclient.discovery.build(api_service_name, api_version, credentials=creds)

        return youtube_client
    

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








'*** Mini Testing Suite ***'


"'get_spotify_uri' functions testing"
# art = 'Granuja'
# song = 'Días de Perros'

# print(f'\n{song.replace(' ', '%20')+'%20'}\n')

# test = CreatePlaylist.get_spotify_uri(artist=art, song_name=song)
# print(test)





'Accessing to the YT client secrets'
# with open(YT_JSON_FILE_PATH) as f:
    
#     data = json.load(f)

#     client_id = data['installed']['client_id']
#     client_secret = data['installed']['client_secret']

#     print(client_id)
#     print(client_secret)




"Testing the 'get_youtube_client' function"
new_service = CreatePlaylist.get_youtube_client()
print(new_service)






