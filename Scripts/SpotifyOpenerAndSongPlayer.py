import Basic_Imports as bi

# serach the folder where this Python-script is in
script_dir = bi.os.path.dirname(bi.os.path.abspath(__file__))

project_dir = bi.os.path.dirname(script_dir)

file_path = bi.os.path.join(project_dir, 'Txt_Files', 'Spotify_Secret_User_Info.txt')

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
Result = bi.subprocess.run(["tasklist"], capture_output=True, text=True, check=True)
TaskList = Result.stdout

if "Spotify.exe" not in TaskList:
    bi.os.startfile("Spotify.exe")
    bi.time.sleep(5)

sp = bi.spotipy.Spotify(auth_manager=bi.SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-modify-playback-state user-read-playback-state"
))

file_path = bi.os.path.join(project_dir, 'Txt_Files', 'Songs.txt')

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

# Hide the blank main window
root = bi.Tk()
root.withdraw()

# QUICK POPUP: Ask right away before loading songs
shuffle_choice = bi.messagebox.askyesno(
    title="Spotify Shuffler", 
    message="Would you like to randomize the queue?"
)

if (shuffle_choice):
    bi.random.shuffle(QueueSongList)

bi.time.sleep(.1)
sp.start_playback(device_id=device_id, uris=[QueueSongList[0]])
bi.time.sleep(1)

remaining_songs = QueueSongList[1:]

for song_uri in remaining_songs:
    try:
        # this is the official command that talks to Spotify Premium!
        sp.add_to_queue(uri=song_uri)
        # print(f"succesfully added: {song_uri}")
        bi.time.sleep(0.2) # short pause to not overload the server
    except Exception as e:
        print(f"error by adding: {e}")

print(f"Done! Check your Spotify queue there should be {len(QueueSongList)} for ya there\n")