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
# import youtube_dl DEPRECATED!




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
    

    ''' This function at the end is deprecated since youtube_dl is no longer being supported '''
    # Step 2: Grab Liked Videos
    # @staticmethod
    # def get_liked_videos(youtube_client:googleapiclient.discovery.build) -> dict:
        
    #     ''' This function will receive a youtube service comming from the get_youtube_client function and will return a dict with the relevant data of the liked videos '''

    #     #Building the request
    #     request = youtube_client.videos().list(part="snippet,contentDetails,statistics", myRating = "like")

    #     #Sending the request to the Youtube API
    #     response = request.execute()

    #     #This dict will store the output
    #     all_song_info = {}

    #     #Collecting the relevant data from each video
    #     for item in response["items"]:

    #         video_title = item["snippet"]["title"]
    #         youtube_url = f'https://www.youtube.com/watch?v={item["id"]}'

    #         #Use youtube_dl to collect the song name & artist name
    #         video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)

    #         song_name = video["track"]
    #         artist = video["artist"]

    #         #Storing the relevant info in the dict
    #         all_song_info[video_title] = {

    #             "youtube_url" : youtube_url,
    #             "song_name" : song_name,
    #             "artist" : artist,

    #             #addind the Spotify URI, easy to get song to put into a playlist
    #             "spotify_uri" : CreatePlaylist.get_spotify_uri(song_name=song_name, artist=artist)
    #         }

    #     return all_song_info    


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
# new_service = CreatePlaylist.get_youtube_client()
# print(new_service)




"Testing the 'get_youtube_client' function"
# new_service = CreatePlaylist.get_youtube_client()

# song_data =CreatePlaylist.get_liked_videos(new_service)

# print(song_data)

'This test failed due to the support of the youtube_dl library'






