from typing import List, Dict, Tuple

class AlbumData:
    """Class to handle album and song data."""

    def __init__(self):
        self.albums: Dict[str, List[str]] = {}
        self.songs_info: Dict[str, Dict[str, str]] = {}

    def load_data(self, file_path: str) -> Tuple[Dict[str, List[str]], Dict[str, Dict[str, str]]]:
        """Load album and song data from a file."""
        current_album = None
        current_song_lyrics = []

        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                current_album = self._process_line(line, current_album, current_song_lyrics)

            # Finalize the last song's lyrics, if any
            self._finalize_song(current_song_lyrics)

        return self.albums, self.songs_info

    def _process_line(self, line: str, current_album: str, current_song_lyrics: List[str]) -> str:
        """Process a line of the file and organize it into albums and songs."""
        if line.startswith("#"):
            current_album = self._process_album_line(line)
        elif line.startswith("*"):
            self._process_song_line(line, current_album, current_song_lyrics)
        else:
            current_song_lyrics.append(line)

        return current_album

    def _process_album_line(self, line: str) -> str:
        """Process an album line and update the albums dictionary."""
        album_details = line[1:].strip().split("::")
        current_album = album_details[0].strip()
        self.albums[current_album] = []
        return current_album

    def _process_song_line(self, line: str, current_album: str, current_song_lyrics: List[str]) -> None:
        """Process a song line and update the albums and songs_info dictionaries."""
        if current_album is None:
            raise ValueError("No album defined before song line")

        if current_song_lyrics:
            song_name = list(self.songs_info.keys())[-1]  # Last song processed
            self.songs_info[song_name]["lyrics"] = "\n".join(current_song_lyrics)
            current_song_lyrics.clear()

        parts = line[1:].split("::")
        song_name = parts[0].strip()
        artist = parts[1].strip()
        song_length = parts[2].strip()

        self.albums[current_album].append(song_name)
        self.songs_info[song_name] = {"artist": artist, "length": song_length, "lyrics": ""}

    def _finalize_song(self, current_song_lyrics: List[str]) -> None:
        """Finalize the song by adding the last song's lyrics to the songs_info dictionary."""
        if current_song_lyrics:
            song_name = list(self.songs_info.keys())[-1]  # Last song processed
            self.songs_info[song_name]["lyrics"] = "\n".join(current_song_lyrics)


"""Utility functions"""
def get_albums(albums: Dict[str, List[str]]) -> List[str]:
    """Returns a list of album names"""
    return list(albums.keys())

def get_album_songs(albums: Dict[str, List[str]], album_name: str) -> List[str]:
    """Returns a list of songs in the specified album"""
    return albums.get(album_name, []) 

def get_song_length(songs_info: Dict[str, Dict[str, str]], song_name: str) -> str:
    """Returns the length of the specified song"""
    song = songs_info.get(song_name)
    if song:
        return song["length"] 
    return "Unknown"

def get_song_lyrics(songs_info: Dict[str, Dict[str, str]], song_name: str) -> str:
    """Returns the lyrics of the specified song"""
    song = songs_info.get(song_name)
    if song:
        return song["lyrics"]
    return "Lyrics not found"

def get_song_album(albums: Dict[str, List[str]], song_name: str) -> str:
    """Returns the album of the specified song"""
    for album, songs in albums.items():
        if song_name in songs:
            return album
    return "Album not found"

def search_songs_by_name(albums: Dict[str, List[str]], keyword: str) -> List[str]:
    """Returns a list of songs that contain the specified keyword in their names"""
    matching_songs = []
    keyword = keyword.lower()
    for album, songs in albums.items():
        for song in songs:
            if keyword in song.lower():
                matching_songs.append(song)
    return matching_songs

def search_songs_by_lyrics(songs_info: Dict[str, Dict[str, str]], keyword: str) -> List[str]:
    """Returns a list of songs that contain the specified keyword in their lyrics"""
    matching_songs = []
    keyword = keyword.lower()
    for song, info in songs_info.items():
        if keyword in info["lyrics"].lower():
            matching_songs.append(song)
    return matching_songs
