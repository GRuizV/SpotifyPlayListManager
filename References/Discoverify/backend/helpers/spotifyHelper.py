
'''
CONSTANTS AND ENVIRONMENT VARIABLES SETTING
'''

# import os
# import requests
# from requests.adapters import HTTPAdapter
# from requests.packages.urllib3.util.retry import Retry
# import json
# from typing import List, Dict
# from dataclasses import dataclass
# import random
# import base64
# from Crypto.Cipher import AES
# import datetime


# Load environment variables
# from dotenv import load_dotenv
# load_dotenv()

# # Constants
# CLIENT_ID = os.getenv('SPOTIFY_API_CLIENT_ID')
# CLIENT_SECRET = os.getenv('SPOTIFY_API_CLIENT_SECRET')

# PLAYLIST_NAME = 'Discover Daily'
# PLAYLIST_DESCRIPTION = (
#     "If you would like to support Discoverify, consider visiting patreon.com/discoverify (COMPLETELY OPTIONAL). "
#     "Daily music, curated for you based on your listening history. "
#     "If you don't want to get this daily playlist anymore, you can unsubscribe at https://discoverifymusic.com"
# )

# @dataclass
# class SpotifyAPIException(Exception):
#     delete_user: bool






'''
MAIN CLASS
'''

# class SpotifyHelper:


#     @staticmethod
#     def get_new_access_token(refresh_token: str) -> str:

#         details = {
#             'grant_type': 'refresh_token',
#             'refresh_token': refresh_token,
#             'client_id': CLIENT_ID,
#             'client_secret': CLIENT_SECRET
#         }

#         result = requests.post('https://accounts.spotify.com/api/token', data=details)
#         result_json = result.json()

#         if 'error' in result_json and result_json['error'] == 'invalid_grant':
#             raise SpotifyAPIException(True)

#         return result_json['access_token']
    

#     @staticmethod
#     def get_refresh_token(code: str, redirect_uri: str) -> str:

#         details = {
#             'grant_type': 'authorization_code',
#             'code': code,
#             'redirect_uri': redirect_uri,
#             'client_id': CLIENT_ID,
#             'client_secret': CLIENT_SECRET
#         }

#         result = requests.post('https://accounts.spotify.com/api/token', data=details)
#         result_json = result.json()

#         if 'error' in result_json and result_json['error'] == 'invalid_grant':
#             raise SpotifyAPIException(True)

#         return result_json['refresh_token']


#     @staticmethod
#     def get_top(type, range, access_token):

#         try:
#             response = requests.get(
#                 f"https://api.spotify.com/v1/me/top/{type}?limit=20&time_range={range}",
#                 headers={
#                     "Authorization": f"Bearer {access_token}"
#                 }
#             )
#             response.raise_for_status()
#             result_json = response.json()
#             return [item["id"] for item in result_json["items"]]
        
#         except requests.exceptions.RequestException as e:
#             print(f"Error: {e}")
#             return []


#     @staticmethod
#     async def get_all_top(range, access_token):
        
#         try:
#             top_tracks = await SpotifyHelper.get_top("tracks", range, access_token)
#             top_artists = await SpotifyHelper.get_top("artists", range, access_token)
#             return {"topTracks": top_tracks, "topArtists": top_artists}

#         except Exception as e: 
#             print(f"Error fetching all top tracks and artists: {e}")
#             return {"topTracks": [], "topArtists": []}


#     @staticmethod
#     def get_seeds(playlist_options, top):

#         artists = []
#         tracks = []

#         for seed in playlist_options['seeds']:

#             if seed == 'AT':
#                 if top['allTime']['tracks']:
#                     index = random.randint(0, len(top['allTime']['tracks']) - 1)
#                     tracks.append(top['allTime']['tracks'].pop(index))

#             elif seed == 'MT':
#                 if top['mediumTerm']['tracks']:
#                     index = random.randint(0, len(top['mediumTerm']['tracks']) - 1)
#                     tracks.append(top['mediumTerm']['tracks'].pop(index))

#             elif seed == 'ST':
#                 if top['shortTerm']['tracks']:
#                     index = random.randint(0, len(top['shortTerm']['tracks']) - 1)
#                     tracks.append(top['shortTerm']['tracks'].pop(index))

#             elif seed == 'AA':
#                 if top['allTime']['artists']:
#                     index = random.randint(0, len(top['allTime']['artists']) - 1)
#                     artists.append(top['allTime']['artists'].pop(index))

#             elif seed == 'MA':
#                 if top['mediumTerm']['artists']:
#                     index = random.randint(0, len(top['mediumTerm']['artists']) - 1)
#                     artists.append(top['mediumTerm']['artists'].pop(index))

#             elif seed == 'SA':
#                 if top['shortTerm']['artists']:
#                     index = random.randint(0, len(top['shortTerm']['artists']) - 1)
#                     artists.append(top['shortTerm']['artists'].pop(index))

#             else:
#                 raise ValueError(f"Unexpected seed value found: {seed}")

#         return {'artists': artists, 'tracks': tracks}
    

#     @staticmethod
#     def get_liked(track_ids, access_token):

#         response = requests.get(
#             f"https://api.spotify.com/v1/me/tracks/contains?ids={','.join(track_ids)}",
#             headers={"Authorization": f"Bearer {access_token}"}
#         )
#         return response.json()
    

#     @staticmethod
#     def get_recommendation_urls(user, seeds):

#         base_url = 'https://api.spotify.com/v1/recommendations?limit=50'

#         if seeds['artists']:
#             base_url += f'&seed_artists={",".join(seeds["artists"])}'

#         if seeds['tracks']:
#             base_url += f'&seed_tracks={",".join(seeds["tracks"])}'

#         min_max_url = base_url + f'&min_acousticness={user["playlistOptions"]["acousticness"][0]/100}&max_acousticness={user["playlistOptions"]["acousticness"][1]/100}'
#         min_max_url += f'&min_danceability={user["playlistOptions"]["danceability"][0]/100}&max_danceability={user["playlistOptions"]["danceability"][1]/100}'
#         min_max_url += f'&min_energy={user["playlistOptions"]["energy"][0]/100}&max_energy={user["playlistOptions"]["energy"][1]/100}'
#         min_max_url += f'&min_instrumentalness={user["playlistOptions"]["instrumentalness"][0]/100}&max_instrumentalness={user["playlistOptions"]["instrumentalness"][1]/100}'
#         min_max_url += f'&min_popularity={user["playlistOptions"]["popularity"][0]}&max_popularity={user["playlistOptions"]["popularity"][1]}'
#         min_max_url += f'&min_valence={user["playlistOptions"]["valence"][0]/100}&max_valence={user["playlistOptions"]["valence"][1]/100}'

#         target_url = base_url + f'&target_acousticness={(user["playlistOptions"]["acousticness"][0]+user["playlistOptions"]["acousticness"][1])/200}'
#         target_url += f'&target_danceability={(user["playlistOptions"]["danceability"][0]+user["playlistOptions"]["danceability"][1])/200}'
#         target_url += f'&target_energy={(user["playlistOptions"]["energy"][0]+user["playlistOptions"]["energy"][1])/200}'
#         target_url += f'&target_instrumentalness={(user["playlistOptions"]["instrumentalness"][0]+user["playlistOptions"]["instrumentalness"][1])/200}'
#         target_url += f'&target_popularity={round((user["playlistOptions"]["popularity"][0]+user["playlistOptions"]["popularity"][1])/2)}'
#         target_url += f'&target_valence={(user["playlistOptions"]["valence"][0]+user["playlistOptions"]["valence"][1])/200}'

#         return {'minMaxUrl': min_max_url, 'targetUrl': target_url}
    
    
#     @staticmethod
#     async def get_tracks(user, user_id, tracks_in_playlist, seeds, access_token):
#         PLAYLIST_SIZE = 30
#         usr = user

#         # if not user.get('playlistOptions'):
#             # usr = await UserController.restore_playlist_options(user_id)

#         min_max_url, target_url = SpotifyHelper.get_recommendation_urls(usr, seeds)

#         recommendations = await requests.fetch(min_max_url, {
#             'Accepts': 'application/json',
#             'method': 'GET',
#             'headers': {
#                 'Authorization': f'Bearer {access_token}'
#             }
#         })

#         response_json = await recommendations.json()

#         tracks = response_json.get('tracks', [])

#         track_ids = []
#         uris = []

#         for track in tracks:
#             track_ids.append(track['id'])
#             uris.append(track['uri'])


#         liked_tracks = set()
#         already_in_playlist = set()
#         playlist_uris = set()


#         for i, liked in enumerate(await SpotifyHelper.get_liked(track_ids, access_token)):

#             if not liked:
#                 playlist_uris.add(uris[i])

#             else:
#                 liked_tracks.add(uris[i])

#             if track_ids[i] in tracks_in_playlist:
#                 already_in_playlist.add(uris[i])

#             if len(playlist_uris) >= PLAYLIST_SIZE:
#                 break


#         if len(playlist_uris) < PLAYLIST_SIZE:

#             target_recommendations = await requests.fetch(target_url, {
#                 'Accepts': 'application/json',
#                 'method': 'GET',
#                 'headers': {
#                     'Authorization': f'Bearer {access_token}'
#                 }
#             })

#             target_response_json = await target_recommendations.json()
#             target_tracks = target_response_json.get('tracks', [])


#             if not target_tracks:
#                 return []
            

#             target_track_ids = []
#             target_uris = []


#             for target_track in target_tracks:
#                 target_track_ids.append(target_track['id'])
#                 target_uris.append(target_track['uri'])


#             for i, target_liked in enumerate(await SpotifyHelper.get_liked(target_track_ids, access_token)):

#                 if not target_liked:
#                     playlist_uris.add(target_uris[i])

#                 else:
#                     liked_tracks.add(target_uris[i])

#                 if target_track_ids[i] in tracks_in_playlist:
#                     already_in_playlist.add(target_uris[i])

#                 if len(playlist_uris) >= PLAYLIST_SIZE:
#                     break


#         for track in already_in_playlist:

#             if len(playlist_uris) >= PLAYLIST_SIZE:
#                 break

#             if track not in liked_tracks:
#                 playlist_uris.add(track)


#         for track in liked_tracks:

#             if len(playlist_uris) >= PLAYLIST_SIZE:
#                 break

#             playlist_uris.add(track)


#         return list(playlist_uris)
    

#     @staticmethod
#     def update_playlist_tracks(playlist_id, uris, access_token):

#         url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
#         headers = {
#             'Authorization': f'Bearer {access_token}',
#             'Content-Type': 'application/json'
#         }

#         data = {
#             'uris': uris
#         }

#         response = requests.post(url, headers=headers, json=data)
#         response.raise_for_status()

#         return response.json()
    

#     @staticmethod
#     def get_playlist(user_id, playlist_id, access_token):

#         if not playlist_id:
#             return None

#         url = f'https://api.spotify.com/v1/playlists/{playlist_id}'
#         headers = {'Authorization': f'Bearer {access_token}'}

#         try:
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             result_json = response.json()

#             return result_json if result_json['owner']['id'] == user_id else None

#         except requests.exceptions.RequestException as e:
#             print(result_json)
#             print(e)

#             response = requests.get(url, headers=headers)
#             result_json = response.json()

#             return result_json if result_json['owner']['id'] == user_id else None
    

#     @staticmethod
#     def create_playlist(user, user_id, access_token):
#         url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
#         headers = {
#             'Content-Type': 'application/json',
#             'Authorization': f'Bearer {access_token}'
#         }
#         data = {
#             'name': 'Discover Daily',
#             'public': False,
#             'description': "If you would like to support Discoverify, consider visiting patreon.com/discoverify (COMPLETELY OPTIONAL). Daily music, curated for you based on your listening history. If you don't want to get this daily playlist anymore, you can unsubscribe at https://discoverifymusic.com"
#         }

#         try:
#             response = requests.post(url, headers=headers, data=json.dumps(data))
#             response.raise_for_status()
#             response_json = response.json()

#             user.playlist_id = response_json['id']

#             return response_json

#         except requests.exceptions.RequestException as e:
#             print(e)
#             return None


#     @staticmethod
#     def get_me(accessToken):
        
#         response = requests.get('https://api.spotify.com/v1/me', headers={'Authorization': f'Bearer {accessToken}'})
#         return response.json()


#     @staticmethod
#     def get_user_playlists(access_token):
#         url = 'https://api.spotify.com/v1/me/playlists?limit=50'
#         headers = {
#             'Accept': 'application/json',
#             'Authorization': f'Bearer {access_token}'
#         }
#         response = requests.get(url, headers=headers)
#         return response.json()
    

#     @staticmethod
#     def get_generic_fetch(uri, access_token):

#         headers = {
#             'Accept': 'application/json',
#             'Authorization': f'Bearer {access_token}'            
#         }
#         response = requests.get(uri, headers=headers)
#         return response.json()
    

#     @staticmethod
#     async def does_my_playlist_exist(playlist_id, access_token):

#         playlists = await SpotifyHelper.get_user_playlists(access_token)

#         if not playlists or 'items' not in playlists:
#             return False

#         next_url = playlists.get('next')

#         while True:

#             for item in playlists['items']:

#                 if item['id'] == playlist_id:
#                     return True

#             if not next_url:
#                 break

#             playlists = await SpotifyHelper.get_generic_fetch(next_url, access_token)
#             next_url = playlists.get('next')

#         return False


#     @staticmethod
#     def add_playlist_cover(playlist_id, image_path, access_token):

#         url = f"https://api.spotify.com/v1/playlists/{playlist_id}/images"
#         headers = {
#             "Authorization": f"Bearer {access_token}",
#         }
#         files = {
#             "file": open(image_path, "rb")
#         }
#         response = requests.put(url, headers=headers, files=files)
#         response.raise_for_status()
    

#     @staticmethod
#     def updatePlaylist(user, playlistCover=None):

#         print(f"Starting job for user: {user['userId']}")

#         userId = AES.new(
#             base64.b64decode(os.environ['CLIENT_SECRET']),
#             AES.MODE_ECB
#         ).decrypt(base64.b64decode(user['userId'])).decode('utf-8')

#         try:
#             accessToken = SpotifyHelper.getNewAccessToken(user['refreshToken'])

#             seeds = SpotifyHelper.getAllTop(user['playlistOptions'], accessToken)
#             seeds = SpotifyHelper.getSeeds(user['playlistOptions'], seeds)

#             playlist = SpotifyHelper.getPlaylist(userId, user['playlistId'], accessToken)
#             doesMyPlaylistExist = SpotifyHelper.doesMyPlaylistExists(user['playlistId'], accessToken)

#             if not playlist or not doesMyPlaylistExist:
#                 playlist = SpotifyHelper.createPlaylist(user, userId, accessToken)
#                 print('Had to create new playlist')

#             playlistId = playlist['id']
#             tracksAlreadyInPlaylist = set(
#                 [x['track']['id'] for x in playlist['tracks']['items']]
#             )

#             tracks = SpotifyHelper.getTracks(user, userId, tracksAlreadyInPlaylist, seeds, accessToken)
#             print(f"{len(tracks)} tracks found")

#             SpotifyHelper.updatePlaylistTracks(playlistId, tracks, accessToken)

#             user['lastUpdated'] = datetime.now()
#             # user.save() # Assuming user is a MongoDB document

#             if playlistCover:
#                 SpotifyHelper.addPlaylistCover(playlistId, playlistCover, accessToken)

#             print(f"Playlist updated for user: {user['userId']}")

#         except Exception as e:

#             print(e)

#             if e.deleteUser:

#                 print(f"Deleting User: {userId}")
#                 # UserController.deleteUser(userId) # Delete user function
#                 return

#         print(' ')


#     @staticmethod
#     async def update_playlists(users):

#         print(f"running {len(users)} jobs | {datetime.now()}")
#         # playlist_cover = 'images/playlistCover.jpeg'
#         # await asyncio.gather(*[update_playlist(user, None) for user in users])

#         failures = []

#         for i, user in enumerate(users):
#             try:
#                 print(f"{i + 1}/{len(users)}")
#                 await SpotifyHelper.update_playlist(user, None)

#             except Exception as e:
#                 print(e)
#                 failures.append(user)

#         print()
#         print(f"running {len(failures)} failure jobs | {datetime.now()}")

#         for i, user in enumerate(failures):
#             try:
#                 print(f"{i + 1}/{len(failures)}")
#                 await SpotifyHelper.update_playlist(user, None)

#             except Exception as e:
#                 print(e)

#         print(f"{len(users)} jobs complete | {datetime.now()}")


#     @staticmethod
#     async def update_playlists_no_update():

#         users = await UserController.get_all_users()

#         print(f"running {len(users)} jobs | {datetime.now()}")

#         for user in users:
#             try:
#                 print(f"Running no update for user: {user['userId']}")

#                 userId = CryptoJS.AES.decrypt(
#                     user['userId'],
#                     CryptoJS.enc.Base64.parse(CLIENT_SECRET),
#                     {
#                         'mode': CryptoJS.mode.ECB
#                     }
#                 ).toString(CryptoJS.enc.Utf8)

#                 accessToken = await SpotifyUpdater.get_new_access_token(user['refreshToken'])

#                 all_top = await SpotifyUpdater.get_all_top(user['playlistOptions'], accessToken)
#                 seeds = await SpotifyUpdater.get_seeds(user['playlistOptions'], all_top)

#                 playlist = await SpotifyUpdater.get_playlist(userId, user['playlistId'], accessToken)

#                 does_my_playlist_exist = await SpotifyUpdater.does_my_playlist_exist(user['playlistId'], accessToken)

#                 if not playlist or not does_my_playlist_exist:
#                     print('HAD TO CREATE NEW PLAYLIST')

#                 playlist_id = playlist['id']
#                 tracks_already_in_playlist = set(map(lambda x: x['track']['id'], playlist['tracks']['items']))

#                 tracks = await SpotifyUpdater.get_tracks(user, userId, tracks_already_in_playlist, seeds, accessToken)

#                 print(f"{len(tracks)} tracks found")
#                 print('Playlist ID:', playlist_id)
#                 print('PLAYLIST EXISTS:', does_my_playlist_exist)
#                 print()

#             except Exception as e:
#                 print(e)

#         print(f"{len(users)} jobs complete | {datetime.now()}")

































