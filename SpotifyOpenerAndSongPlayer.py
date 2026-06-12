import os
import subprocess
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# serach the folder where this Python-script is in
script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(script_dir, 'Spotify_Secret_User_Info.txt')

#fill in your Spotify Developer Dashboard user settings/info
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""

with open(file_path, 'r') as Spotify_User_file:
    lines = Spotify_User_file.readlines()
    CLIENT_ID = lines[0].strip()
    CLIENT_SECRET = lines[1].strip()
    REDIRECT_URI = lines[2].strip()

print("\nChecking if Spotify is active...")
Result = subprocess.run(["tasklist"], capture_output=True, text=True, check=True)
TaskList = Result.stdout

if "Spotify.exe" not in TaskList:
    os.startfile("Spotify.exe")
    time.sleep(5)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))

file_path = os.path.join(script_dir, 'Songs.txt')

QueueSongList = []

# Open the file with complete path
with open(file_path, 'r') as songs_file:
    lines = songs_file.readlines()
    for line in lines:
        uri_part = line.split('#')[0]
        cleaned_line = uri_part.replace('"','').strip()
        # print(cleaned_line)

        if cleaned_line:
            QueueSongList.append(cleaned_line)

# search for available devices
devices = sp.devices()
device_id = None

if devices['devices']:
    # grab the first available device (for example your pc)
    device_id = devices['devices'][0]['id']
    # print(device_id)

time.sleep(.1)

sp.start_playback(device_id=device_id, uris=[QueueSongList[0]])

time.sleep(1)

for song_uri in QueueSongList[1:]:
    try:
        # this is the official command that talks to Spotify Premium!
        sp.add_to_queue(uri=song_uri)
        # print(f"succesfully added: {song_uri}")
        time.sleep(0.2) # short pause to not overload the server
    except Exception as e:
        print(f"error by adding: {e}")

print(f"Done! Check your Spotify queue there should be {len(QueueSongList)} for ya there\n")