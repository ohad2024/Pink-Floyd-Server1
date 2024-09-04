import socket

# משתנים קבועים
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# יצירת הסוקט והתחברות לשרת
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, SERVER_PORT))

# קבלת הודעת הפתיחה מהשרת
welcome_message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
print(welcome_message)

# לולאה לתקשורת עם השרת
while True:
    # הצגת התפריט למשתמש
    print("\nMenu:")
    print("1. Get Albums")
    print("2. Get Album Songs")
    print("3. Get Song Length")
    print("4. Get Song Lyrics")
    print("5. Get Song Album")
    print("6. Search Song by Name")
    print("7. Search Song by Lyrics")
    print("8. Quit")
    
    command = input("Enter your choice: ").strip()
    client_socket.sendall(command.encode('utf-8'))
    
    if command in {"2", "3", "4", "5", "6", "7"}:
        keyword = input("Enter album/song/keyword: ").strip()
        client_socket.sendall(keyword.encode('utf-8'))
    
    if command == "8":
        print("Disconnecting from the server...")
        break
    
    response = ""
    while True:
        part = client_socket.recv(BUFFER_SIZE).decode('utf-8')
        response += part
        if len(part) < BUFFER_SIZE:
            break

    print(f"Server response:\n{response}")

client_socket.close()
