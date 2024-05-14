import json
import re


YT_JSON_FILE_PATH = r'C:\Users\USUARIO\GR\Software Development\Projects\Spotify Playlists Manager\References\Ref Projects\Bukola YT PJ\Youtube_dl replacement\yt_dlp\yt_dlp_response.json'

with open(YT_JSON_FILE_PATH) as f:

    data = json.load(f)

result = []

for elem in data.values():

    result.append((elem['uploader'], elem['title']))


# #1st test base
# base = [
#     ('Manuel Turizo', 'La Bachata - MTZ Manuel Turizo | Video Oficial'), 
#     ('Xavi Oficial', 'Xavi - La Diabla (Official Video)'), 
#     ('KAROL G', 'KAROL G - Amargura (Visualizer)'), 
#     ('Bad Bunny', 'BAD BUNNY ft. FEID - PERRO NEGRO (Visualizer) | nadie sabe lo que va a pasar mañana'), 
#     ('Feid', 'Feid, ATL Jacob - LUNA (Official Video)')
#     ]


songs = []


# Regular expression pattern
pattern = re.compile(r'^(.+?)\s*-\s*(.+?)\s*[\(|\|].*') # this means "Match anything from the begning to the hyphen, and everything else from the hypen to the next '(' or '|'"

# Extractng song names
for artist, title in result:

    match = pattern.match(title)
    elem1, elem2 = None, None

    if match:
        elem1 = match.group(1)
        elem2 = match.group(2)
 

    if elem1 and elem2:

        art_name = artist.split()[0].casefold() #Sometimes the artist has a composed name

        if art_name in elem1.casefold():
            songs.append((artist, elem2))
        else:
            songs.append((artist, elem1))


print(songs)

