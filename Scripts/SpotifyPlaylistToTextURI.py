import Basic_Imports as bi
from ClassStorage import WaitTime
from SpotifyOpenerAndSongPlayer import GetItems

def SavePlaylistToTxt(sp, playlist_id, output_file_path):
    offset = 0
    limit = 100
    total_tracks_saved = 0
    
    # Open het bestand om in te schrijven (met UTF-8 om rare tekens in songtitels te ondersteunen)
    with open(output_file_path, 'w', encoding='utf-8') as songs_file:
        while True:
            # Vraag de nummers op (fields is hier weggehaald voor stabiliteit)
            results = sp.playlist_items(
                playlist_id=playlist_id,
                limit=limit,
                offset=offset
            )

            # Controleer of we überhaupt een antwoord hebben gekregen
            if not results:
                break

            items = results.get('items', [])

            # Als deze pagina leeg is, stoppen we direct
            if not items:
                break

            for item in items:
                track = item.get('track') or item.get('item')
                if track and track.get('uri'):
                    uri = track['uri']
                    song_name = track['name']
                    
                    # Voeg alle artiesten samen (als er meerdere zijn, gescheiden door een komma)
                    artists_list = [artist['name'] for artist in track['artists']]
                    artists_string = ", ".join(artists_list)
                    
                    # Maak exact de regel zoals jij hem wilt:
                    # "spotify:track:..." # Titel - Artiest
                    line = f'"{uri}" # {song_name} - {artists_string}\n'
                    
                    # Schrijf de regel direct naar het tekstbestand
                    songs_file.write(line)
                    total_tracks_saved += 1

            # Stop de loop als er geen nummers meer zijn volgens de 'next' url
            if not results.get('next'):
                break
                
            offset += limit

    print(f"Klaar! Er zijn {total_tracks_saved} nummers succesvol opgeslagen in: {output_file_path}")

sp, project_dir = GetItems()

output_path = bi.os.path.join(project_dir, 'Txt_Files', 'My_Song_URIs.txt')

playlistID = "spotify:playlist:2VMUxzv5asxkLNcCpSBNBo"

# Voer de functie uit
SavePlaylistToTxt(sp, playlistID, output_path)
