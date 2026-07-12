import Basic_Imports as bi
from ClassStorage import WaitTime

def SavePlaylistToTxt(sp, playlist_id, output_file_path):
    offset = 0
    limit = 100
    
    # Open het bestand om in te schrijven (met UTF-8 om rare tekens in songtitels te ondersteunen)
    with open(output_file_path, 'w', encoding='utf-8') as f:
        while True:
            # Vraag de nummers op inclusief titel en artiesten
            results = sp.playlist_items(
                playlist_id=playlist_id,
                fields="items(track(uri, name, artists)),next",
                limit=limit,
                offset=offset
            )

            for item in results['items']:
                track = item.get('track')
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
                    f.write(line)

            # Stop de loop als er geen nummers meer zijn
            if not results.get('next'):
                break
                
            offset += limit

    print(f"Klaar! De playlist is succesvol opgeslagen in: {output_file_path}")

# Bepaal waar het bestand moet komen (in jouw 'Txt_Files' map)
output_path = bi.os.path.join(project_dir, 'Txt_Files', 'Mijn_Gexporteerde_Songs.txt')

# Voer de functie uit (vervang JOUW_PLAYLIST_ID door de echte ID)
SavePlaylistToTxt(sp, "JOUW_PLAYLIST_ID_HIER", output_path)
