def load_data(file_path):
    albums = {} # מילון של כל האלבומים בפורמט של שם האלבום כמפתח וערך שמות השירים 
    songs_info = {} # מילון של כל השירים בפורמט של שם השיר כמפתח וערך של שם האלבום, שם השיר, משך השיר וטקסט השיר

    with open(file_path, 'r', encoding='utf-8') as file:
        current_album = None
        current_song_lyrics = []
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                album_details = line[1:].strip().split("::") # מתחיל מהתו שני ומחלק את השורה לפי המפריד :: 
                current_album = album_details[0].strip()  # שם האלבום בלבד
                albums[current_album] = [] # שם האלבום בתוך המילון בתור מפתח וערך ריק כלומר אין שירים עדיין
            elif line.startswith("*"): 
                if current_song_lyrics:  # שמירת השיר הקודם
                    songs_info[song_name]["lyrics"] = "\n".join(current_song_lyrics)
                    current_song_lyrics = []
                
                parts = line[1:].split("::")# מתחיל מהתו השני ומחלק את השורה לפי המפריד ::
                song_name = parts[0].strip() # שם השיר בלבד
                artist = parts[1].strip() # שם האלבום בלבד
                song_length = parts[2].strip() # משך השיר בלבד

                albums[current_album].append(song_name) 
                songs_info[song_name] = {"artist": artist, "length": song_length, "lyrics": ""}
            else:
                current_song_lyrics.append(line)
        
        # שמירת השיר האחרון בסיום הקובץ
        if current_song_lyrics:
            songs_info[song_name]["lyrics"] = "\n".join(current_song_lyrics)

    return albums, songs_info

def get_albums(albums):
    return list(albums.keys())

def get_album_songs(albums, album_name):
    return albums.get(album_name, []) # מחזירה את השירים של האלבום שנשלח ואם אין אלבום מזהה מחזירה ריק

def get_song_length(songs_info, song_name):
    song = songs_info.get(song_name)
    if song:
        return song["length"] 
    return None

def get_song_lyrics(songs_info, song_name):
    song = songs_info.get(song_name)
    if song:
        return song["lyrics"]
    return None

def get_song_album(albums, song_name):
    for album, songs in albums.items():
        if song_name in songs:
            return album
    return None

def search_songs_by_name(albums, keyword):
    matching_songs = []
    keyword = keyword.lower()
    for album, songs in albums.items():
        for song in songs:
            if keyword in song.lower():
                matching_songs.append(song)
    return matching_songs

def search_songs_by_lyrics(songs_info, keyword):
    matching_songs = []
    keyword = keyword.lower()
    for song, info in songs_info.items():
        if keyword in info["lyrics"].lower():
            matching_songs.append(song)
    return matching_songs
