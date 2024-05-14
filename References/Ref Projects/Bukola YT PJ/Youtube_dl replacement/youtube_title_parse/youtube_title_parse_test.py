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
import youtube_title_parse


# Loading environmental variables which include clients secrets
load_dotenv()


# CONSTANTS
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_USER = os.getenv('SPOTIFY_USER')
SPOTIFY_TOKENS_JSON_FILE_PATH = spotify_helper.SPOTIFY_TOKENS_JSON_FILE_PATH
YT_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Ref Projects\Bukola YT PJ\youtube_client_secrets.json'
PROJECTS_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Ref Projects\Bukola YT PJ'

YT_TITLE_PARSE_JSON_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Ref Projects\Bukola YT PJ\Youtube_dl replacement\youtube_title_parse\youtube_title_parse_response.json'


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
    

    @staticmethod
    def get_liked_videos(youtube_client:googleapiclient.discovery.build) -> dict:
            
            ''' This function will receive a youtube service comming from the get_youtube_client function and will return a dict with the relevant data of the liked videos '''

            #Building the request
            request = youtube_client.videos().list(part="snippet,contentDetails,statistics", myRating = "like")

            #Sending the request to the Youtube API
            response = request.execute()

            #This dict will store the output
            all_song_info = {}

            #Collecting the relevant data from each video
            for item in response["items"]:

                video_title = item["snippet"]["title"]
                artist, title = youtube_title_parse.get_artist_title(video_title)
                
                if artist and title:
                    all_song_info[video_title] = {'artist': artist, 'title': video_title}


            with open(YT_TITLE_PARSE_JSON_PATH, 'w') as f:
                json.dump(all_song_info,f,indent=2)
    


"Testing the 'get_youtube_client' function"
new_service = CreatePlaylist.get_youtube_client()

songs_data = CreatePlaylist.get_liked_videos(new_service)

# print(songs_data)



'''
Notes:

    It kind of works but to get the track's name is needed a little string handling to have a wayaround not being able to directly extract it,
    and one non-negotiable condition to still makes sense is that the videos in the youtube API response must come from the official artist channel, 
    and the reason is because when the video comes from the official artist channel, both the data["uploader"] and data["channel"] coincide with the actual
    name of the artist, in a different scenario, it'd be impossible to infere which is the artist and which the track's name.

'''