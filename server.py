import socket
import threading
from data import load_data, get_albums, get_album_songs, get_song_length, get_song_lyrics, get_song_album, search_songs_by_name, search_songs_by_lyrics

#משתנים קבועים
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

#טעינת הנתונים
FILE_PATH = 'Pink_Floyd_DB.txt'
albums, songs_info = load_data(FILE_PATH)

#יצירת הסוקט והקשורות לשרת עד 5 לקוחות
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(5)

print(f"Server is listening on {SERVER_IP}:{SERVER_PORT}...")

#פונקציה לטיפול בלקוחות
def handle_client(client_socket):
    client_socket.sendall(b"Welcome to the Pink Floyd Server!\n")
    
    while True:
        request = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
        if not request:
            break

        print(f"Received request: {request}")

        response = ""
        if request == "1":
            response = ", ".join(get_albums(albums))
        elif request == "2":
            album_name = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            response = ", ".join(get_album_songs(albums, album_name))
        elif request == "3":
            song_name = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            response = get_song_length(songs_info, song_name) or "Song not found"
        elif request == "4":
            song_name = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            response = get_song_lyrics(songs_info, song_name) or "Song not found"
        elif request == "5":
            song_name = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            response = get_song_album(albums, song_name) or "Song not found"
        elif request == "6":
            keyword = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            response = ", ".join(search_songs_by_name(albums, keyword)) or "No songs found"
        elif request == "7":
            keyword = client_socket.recv(BUFFER_SIZE).decode('utf-8').strip()
            response = ", ".join(search_songs_by_lyrics(songs_info, keyword)) or "No songs found"
        elif request == "8":
            response = "Goodbye!"
            client_socket.sendall(response.encode('utf-8'))
            break
        else:
            response = "Unknown command."

        client_socket.sendall(response.encode('utf-8'))

    client_socket.close()
    print("Connection closed.")

#לולאה לקבלת התחברות מלקוחות
while True:
    client_socket, client_address = server_socket.accept()
    print(f"New connection from {client_address}")
    
    client_thread = threading.Thread(target=handle_client, args=(client_socket,))
    client_thread.start()
