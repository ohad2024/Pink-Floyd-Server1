import socket

# Constants
SERVER_IP: str = '127.0.0.1'
SERVER_PORT: int = 12345
BUFFER_SIZE: int = 1024

class Client:
    def __init__(self, server_ip: str, server_port: int, buffer_size: int):
        self.server_ip = server_ip
        self.server_port = server_port
        self.buffer_size = buffer_size
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.stop_flag = False

    def connect(self) -> None:
        """Connect to the server."""
        self.client_socket.connect((self.server_ip, self.server_port))
        welcome_message = self.client_socket.recv(self.buffer_size).decode('utf-8')
        print(welcome_message)

    def communicate(self) -> None:
        """Communicate with the server."""
        while not self.stop_flag:
            self.display_menu()
            command = input("Enter your choice: ").strip()
            self.client_socket.sendall(command.encode('utf-8'))

            if command in {"2", "3", "4", "5", "6", "7"}:
                keyword = input("Enter album/song/keyword: ").strip()
                self.client_socket.sendall(keyword.encode('utf-8'))

            if command == "8":
                print("Disconnecting from the server...")
                self.stop_flag = True
                break

            # Receiving and printing the response properly
            response = self.receive_response()
            if response:  # Only print if there's a response
                print(f"Server response:\n{response}")
            else:
                print("No response received.")

        self.client_socket.close()

    def receive_response(self) -> str:
        """Receive a response from the server."""
        response = ""
        while True:
            try:
                part = self.client_socket.recv(self.buffer_size).decode('utf-8')
                if not part:  # Connection closed
                    break
                response += part
                if len(part) < self.buffer_size:  # Finished receiving data
                    break
            except Exception as e:
                print(f"Error receiving response: {e}")
                break
        return response.strip()  # Strip any extra newlines or spaces

    def display_menu(self) -> None:
        """Display the menu."""
        print("\nMenu:")
        print("1. Get Albums")
        print("2. Get Album Songs")
        print("3. Get Song Length")
        print("4. Get Song Lyrics")
        print("5. Get Song Album")
        print("6. Search Song by Name")
        print("7. Search Song by Lyrics")
        print("8. Quit")


def main() -> None:
    """Main function to start the client."""
    client = Client(SERVER_IP, SERVER_PORT, BUFFER_SIZE)
    client.connect()
    client.communicate()


if __name__ == "__main__":
    main()
