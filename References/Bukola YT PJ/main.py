import requests
import base64
import json
import spotify_helper
import time

# CONSTANTS
TOKENS_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Bukola YT PJ\tokens.json'



# GREETING AND FIRST CONTACT
print('''
\nHey! Welcome to the Spotify Playlist Manager app.
Thanks for your preference for our service, 

Before anything else, a little heads-up:
        
    If this is your first time using the app or did you revoke the authorization
    of the app from spotify, please go to the flask_app file and start the server
    to receive the authorization code necessary to make changes in the playlists on your behalf.
      
Ok. Now, let's get going...
      
'''
)


greeting_response = input('- Is this your first time using the app or did you revoke authorization from spotify priorly? (Y/N)\n').upper()

# Input handling
while greeting_response not in ('Y', 'N'):
    print('\nSorry, invalid answer...')
    greeting_response = input('\n- Is this your first time using the app or did you revoke authorization from spotify priorly? (Y/N)\n').upper()



# If Authorization is needed
if greeting_response == 'Y':    
    code = spotify_helper.SpotifyHelper.authorize()
            
                


# TOKEN CHECKING: Revising is a Token already exist in the tokens.json file
with open(TOKENS_JSON_FILE_PATH, 'r') as f:

    try:
        tokens_contents = json.load(f)
        token = tokens_contents.get('token')

        if token is not None:
            print('\n   - It was confirmed that we also got a token to proceed.\n')
        
        else:
            print(f'''\n  ERROR: Apparently we don't have have a Token to work with, please go back to the authorization process so we can ask for a Token to modify your playlist on your behalf.''')
            raise Exception(f'''\n  ERROR: Apparently we don't have have a Token to work with, please go back to the authorization process so we can ask for a Token to modify your playlist on your behalf.''')
                
    except Exception as e:
        raise Exception(f'''\n  ERROR - {e} -: Apparently we don't have have a Token to work with, please go back to the authorization process so we can ask for a Token to modify your playlist on your behalf.''')





# Now that we made sure we have a code to work with...

# 1. Understand how the tokens works and implement the token requesting and refreshing
# 2. After having a token, go back to Bukola's pj to keep learning.












