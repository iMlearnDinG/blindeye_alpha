import socket

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    initial_check = client_socket.recv(1024).decode()

    if initial_check == "Server full":
        print("Server is full. Closing connection.")
        client_socket.close()
        return

    while True:
        message = input("Enter a command (type 'quit' to exit): ")
        client_socket.send(message.encode())
        response = client_socket.recv(1024).decode()
        print(f"Response: {response}")

        if message.lower() == "quit":
            break

    client_socket.close()

if __name__ == "__main__":
    start_client("localhost", 12345)
