import os
import subprocess
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Zoek de map op waarin dit Python-script staat
script_dir = os.path.dirname(os.path.abspath(__file__))

file_path = os.path.join(script_dir, 'Spotify_Secret_User_Info.txt')

# Vul hier de gegevens in van je Spotify Developer Dashboard
CLIENT_ID = ""
CLIENT_SECRET = ""
REDIRECT_URI = ""

# bestand met het volledige pad
with open(file_path, 'r') as Spotify_User_file:
    lines = Spotify_User_file.readlines()
    CLIENT_ID = lines[0]
    CLIENT_SECRET = lines[1]
    REDIRECT_URI = lines[2]



print("Controleren of Spotify actief is...")
Result = subprocess.run(["tasklist"], capture_output=True, text=True, check=True)
TaskList = Result.stdout

if "Spotify.exe" not in TaskList:
    os.startfile("Spotify.exe")
    time.sleep(5)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-modify-playback-state"
))

file_path = os.path.join(script_dir, 'Songs.txt')

QueueSongList = []

# Open het bestand met het volledige pad
with open(file_path, 'r') as songs_file:
    lines = songs_file.readlines()
    for line in lines:
        uri_part = line.split('#')[0]
        cleaned_line = uri_part.replace('"','').strip()
        print(cleaned_line)

        # Alleen toevoegen als de regel na het opschonen niet leeg is
        if cleaned_line:
            QueueSongList.append(cleaned_line)

sp.start_playback(uris=[QueueSongList[0]])

for song_uri in QueueSongList[1:]:
    try:
        # Dit is het officiële commando dat direct met Spotify Premium praat!
        sp.add_to_queue(uri=song_uri)
        print(f"Succesvol toegevoegd: {song_uri}")
        time.sleep(0.5) # Korte pauze om de server niet te overbelasten
    except Exception as e:
        print(f"Fout bij toevoegen: {e}")

print("\nKlaar! Open Spotify en bekijk je wachtrij.")

print(f"Er staan {len(QueueSongList)} nummers klaar voor de wachtrij.")
print("Zorg dat Spotify openstaat op je scherm!")