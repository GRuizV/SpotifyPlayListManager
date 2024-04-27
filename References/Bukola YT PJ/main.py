import requests
import base64
import json
import spotify_helper
import time

# CONSTANTS
TOKENS_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Bukola YT PJ\tokens.json'


if __name__ == '__main__':


    # GREETING AND FIRST CONTACT
    print('''
\nHey! Welcome to the Spotify Playlist Manager app.
Thanks for your preference for our service, 

Now, let's stat...
'''
)

    greeting_response = input('Is this your first time using the app? (Y/N)\n')

    while greeting_response not in ('Y', 'N'):
        print('Invalid answer...')
        greeting_response = input('Is this your first time using the app? (Y/N)')

    
    if greeting_response == 'Y':
        print('\nAlright, so let us begin then.', end='\n')
        print('''Since the Spotify Authorization Service does not callback when the authorization fails, we will set a time limit of 3 minutes,
if we have not received an authentication code by then, we will assume the authorization process goes wrong and please contact us to further check the issue.\n''')
    
        print(f'''\nNow, please go to the 'flask_app.py' file and run the server and with the server up and running,\nPlease go to this url to authorize the app
        https://accounts.spotify.com/authorize?client_id={spotify_helper.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={spotify_helper.REDIRECT_URI}&scope={spotify_helper.SPOTIFY_AUTH_SCOPE}\n''')

       
        #Timer setting for the auth timeout
        start_time = time.time()
        timeout_duration = 180

        while time.time() - start_time < timeout_duration:

            with open(TOKENS_JSON_FILE_PATH,'r') as f:
                tokens_data = json.load(f)
                code = tokens_data.get('code')
            
                if code:
                    print('Great! the code was received, now we will exchange it for a Token to modify your playlist on your behalf')
                    break

            if time.time() - start_time >= timeout_duration:
                print('Authorization process failed. Please try again or contact support.')




    # The logic of the existance of the 'code' paramenter in the json file will be here
    # and the flask app will only run if that code doesn't exist and the first contact with spotify
    # is needed to be made and when the code is retrieved it will stop the flask app.

    # The case where the code already exists, I will pass to validate if the token exist, and otherwise, 
    # it will request for the first time or refresh the token if needed to keep working with the app.











    