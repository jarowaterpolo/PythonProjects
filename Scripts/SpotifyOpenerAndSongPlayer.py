import Basic_Imports as bi
from ClassStorage import WaitTime

def GetItems():
    # search the folder where this Python-script is in
    script_dir = bi.os.path.dirname(bi.os.path.abspath(__file__))
    # find parent directory
    project_dir = bi.os.path.dirname(script_dir)
    # find where the text file is
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
        WaitTime.Wait(5)

    sp = bi.spotipy.Spotify(auth_manager=bi.SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="user-modify-playback-state user-read-playback-state playlist-read-private playlist-modify-public playlist-modify-private"
    ))

    return sp, project_dir

def Main():
    (sp, project_dir) = GetItems()

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

    WaitTime.Wait(.1)
    sp.start_playback(device_id=device_id, uris=[QueueSongList[0]])
    WaitTime.Wait(1)

    remaining_songs = QueueSongList[1:]

    for song_uri in remaining_songs:
        try:
            # this is the official command that talks to Spotify Premium!
            sp.add_to_queue(uri=song_uri)
            # print(f"succesfully added: {song_uri}")
            WaitTime.Wait(0.2) # short pause to not overload the server
        except Exception as e:
            print(f"error by adding: {e}")

    print(f"Done! Check your Spotify queue there should be {len(QueueSongList)} for ya there\n")

     # QUICK POPUP: Ask right away before loading songs
    doCreatePlaylist = bi.messagebox.askyesno(
        title="Create Playlist", 
        message="Would you like to create a playlist?"
    )

    if (doCreatePlaylist):
        CreatePlaylist(sp, QueueSongList)

def CreatePlaylist(sp, QueueSongList):
    playlist_name = "Spotipy Playlist"

    DeletePlaylistByName(sp, playlist_name)

    # 2. Gecorrigeerde aanroep (Maakt gebruik van /v1/me/playlists in plaats van /v1/users/{id}/playlists)
    try:
        new_playlist = sp.current_user_playlist_create(
            name=playlist_name, 
            public=False, 
            description="Created programmatically using Spotipy!"
        )
        playlist_id = new_playlist["id"]
        print(f"Afspeellijst succesvol aangemaakt! ID: {playlist_id}")
    except Exception as e:
        print(f"Fout bij het aanmaken van de afspeellijst: {e}")
        return

    # 3. Voeg de nummers toe (In plukjes van maximaal 100 om API-fouten te voorkomen)
    if QueueSongList:
        print("Nummers toevoegen aan de afspeellijst...")
        for i in range(0, len(QueueSongList), 100):
            chunk = QueueSongList[i:i + 100]
            try:
                sp.playlist_add_items(playlist_id=playlist_id, items=chunk)
                print(f"Groep toegevoegd ({len(chunk)} nummers)...")
                WaitTime.Wait(0.2)
            except Exception as e:
                print(f"Fout bij toevoegen van deze groep nummers: {e}")
                
    print("Alles klaar!")

def DeletePlaylistByName(sp, playlist_name):
    # 1. Controleer op en verwijder bestaande afspeellijsten met dezelfde naam
    try:
        playlists = sp.current_user_playlists()
        for playlist in playlists['items']:
            if playlist['name'] == playlist_name:
                print(f"Oude afspeellijst '{playlist_name}' gevonden. Wordt verwijderd...")
                sp.current_user_unfollow_playlist(playlist_id=playlist['id'])
    except Exception as e:
        print(f"Kon oude afspeellijsten niet controleren: {e}")

if __name__ == "__main__":
    Main()