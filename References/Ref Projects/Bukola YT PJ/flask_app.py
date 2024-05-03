import flask, json
import spotify_helper


# CONSTANTS
TOKENS_JSON_FILE_PATH = spotify_helper.TOKENS_JSON_FILE_PATH


# Flask app setting
app = flask.Flask(__name__)

@app.route('/')
def home():
    
    # Spotify authorization URL
    auth_url = f'https://accounts.spotify.com/authorize?client_id={spotify_helper.SPOTIFY_CLIENT_ID}&response_type=code&redirect_uri={spotify_helper.REDIRECT_URI}&scope={spotify_helper.SPOTIFY_AUTH_SCOPE}'
    
    # HTML content with embedded URL
    html_content = f"""
    <html>
    <body>
    <h1>Welcome to the Spotify Playlist Manager!</h1>
    <p>Please authorize the app by visiting the following Link:</p>
    <a href="{auth_url}">Link</a>
    </body>
    </html>
    """
    return html_content


@app.route('/callback')
def callback():

    code = flask.request.args.get('code')

    if code:

        with open(TOKENS_JSON_FILE_PATH) as f:
            data = json.load(f)

        # Store the code in the tokens.json file ***Careful with the path***
        with open(TOKENS_JSON_FILE_PATH, 'w') as f:
            data['code'] = code
            json.dump(data, f, indent=2)

        # Redirect to a success page
        return flask.redirect('/sucess')
    
    else:
        # Handle the case where the code is missing
        return 'Authorization code missing', 400


@app.route('/sucess')
def sucess():
    return f'<h1> Authorization successful! Now you can start to modify your playlists.</h1>'



if __name__ == '__main__':

    app.run(port=5000)
