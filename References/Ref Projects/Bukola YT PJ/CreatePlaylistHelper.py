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
import yt_dlp as youtube_dl
import re




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
    
    
    # This function at the end is deprecated since youtube_dl is no longer being supported
    # Nevertheless a fair substitute
    # Step 2: Grab Liked Videos
    @staticmethod
    def get_liked_videos() -> list:
        
        ''' This function will receive a youtube service comming from the get_youtube_client function and will return a dict with the relevant data of the liked videos '''

        # Create the new youtube service
        youtube_client = CreatePlaylist.get_youtube_client()

        #Building the request
        request = youtube_client.videos().list(part="snippet,contentDetails,statistics", myRating = "like")

        #Sending the request to the Youtube API
        response = request.execute()

        #This dict will store the output
        all_song_info = []

        #Collecting the relevant data from each video
        for item in response["items"]:

            video_title = item["snippet"]["title"]
            youtube_url = f'https://www.youtube.com/watch?v={item["id"]}'

            #Use youtube_dl to collect the song name & artist name
            video = youtube_dl.YoutubeDL({}).extract_info(youtube_url, download=False)

            #Storing the relevant info in the dict
            all_song_info.append((video['uploader'], video_title))


        # PARSING THE VIDEO TITLE TO DEDUCE THE SONG'S NAME

        songs = []

        # Regular expression pattern
        pattern = re.compile(r'^(.+?)\s*-\s*(.+?)\s*[\(|\|].*') # this means "Match anything from the begning to the hyphen, and everything else from the hypen to the next '(' or '|'"

        # Extractng song names
        for artist, title in all_song_info:

            match = pattern.match(title)
            elem1, elem2 = None, None

            if match:
                elem1 = match.group(1)
                elem2 = match.group(2)
        

            if elem1 and elem2:

                art_name = artist.split()[0].casefold() #Sometimes the artist has a composed name

                if art_name in elem1.casefold():
                    songs.append((artist, elem2, CreatePlaylist.get_spotify_uri(song_name=elem2, artist=artist)))
                else:
                    songs.append((artist, elem1, CreatePlaylist.get_spotify_uri(song_name=elem2, artist=artist)))

        return songs


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
    def add_song_to_playlist() -> str:

        ''' This function executes the whole app process: returns the id of the newly created playlist'''
       
        # Collect the song's uris
        uris = [item[2] for item in CreatePlaylist.get_liked_videos()]

        # Create the new playlist
        playlist_id = CreatePlaylist.create_playlist()

        # Add all songs into new playlist
        request_data = json.dumps(uris)
        query = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'

        # Access token requesting
        token = spotify_helper.SpotifyHelper.request_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        # Sending the POST Request
        try:            
            response = requests.post(url=query, data=request_data, headers=headers)
            response.raise_for_status()
            response_json = response.json()

            #Returning the ID of the newly created playlist
            return print('\n\nThe playlist with your liked videos from Youtube was successfully created!\n\n')           

        except Exception as e:

            print(e)
            return None







'===================================================================='

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

# song_data = CreatePlaylist.get_liked_videos(new_service)

# for i in song_data:
#     print(i)

'This test initially failed due to the support of the youtube_dl library / it was replaced with yt_dlp library'




'===================================================================='


if __name__ == '__main__':

    CreatePlaylist.add_song_to_playlist()

