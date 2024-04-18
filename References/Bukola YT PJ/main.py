# Step 1: Log into Youtube
# Step 2: Grab Liked Videos
# Step 3: Create a New Playlist
# Step 4: Search for the Song
# Step 5: Add this son into the new Spotify playlist

from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_USR = os.getenv('SPOTIFY_USER')
print(SPOTIFY_USR)


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
    def create_playlist():
        pass


    # Step 4: Search for the Song
    @staticmethod
    def get_spotify_uri():
        pass

    
    # Step 5: Add the song into the new Spotify playlist
    @staticmethod
    def add_song_to_playlist():
        pass