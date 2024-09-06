import socket
import threading
from data import AlbumData, get_albums, get_album_songs, get_song_length, get_song_lyrics, get_song_album, search_songs_by_name, search_songs_by_lyrics

# Constants
SERVER_IP: str = '127.0.0.1'
SERVER_PORT: int = 12345
BUFFER_SIZE: int = 1024
MAX_CLIENTS: int = 5

# Load data using the AlbumData class
FILE_PATH: str = 'Pink_Floyd_DB.txt'
album_data = AlbumData()
albums, songs_info = album_data.load_data(FILE_PATH)

# Create socket and listen for clients
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(MAX_CLIENTS)

print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}...")


def handle_client(client_socket: socket.socket) -> None:
    """Handle communication with a client."""
    client_socket.sendall(b"Welcome to the Pink Floyd Server!\n")
    stop_flag = False

    while not stop_flag:
        try:
            request = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            if not request:
                break

            response = process_request(request, client_socket)

            if request == "8":
                stop_flag = True

            client_socket.sendall(response.encode('utf-8'))
        except Exception as e:
            print(f"Error during client handling: {e}")
            break

    client_socket.close()
    print("Connection closed.")


def process_request(request: str, client_socket: socket.socket) -> str:
    """Process client requests and return appropriate responses."""
    match request:
        case "1":
            return ", ".join(get_albums(albums)) or "No albums found"
        case "2":
            album_name = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            return ", ".join(get_album_songs(albums, album_name)) or "Album not found"
        case "3":
            song_name = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            return get_song_length(songs_info, song_name) or "Song not found"
        case "4":
            song_name = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            return get_song_lyrics(songs_info, song_name) or "Song not found"
        case "5":
            song_name = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            return get_song_album(albums, song_name) or "Song not found"
        case "6":
            keyword = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            return ", ".join(search_songs_by_name(albums, keyword)) or "No songs found"
        case "7":
            keyword = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            return ", ".join(search_songs_by_lyrics(songs_info, keyword)) or "No songs found"
        case "8":
            return "Goodbye!"
        case _:
            return "Unknown command."

def main() -> None:
    """Main function to start the server."""
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    main()
