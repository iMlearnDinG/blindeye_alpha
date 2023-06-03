import socket
import threading
import pygame
import queue
import time
import pygame.font

class ServerInstance:
    def __init__(self, max_connections, update_queue, instance_number):
        self.max_connections = max_connections
        self.current_connections = 0
        self.update_queue = update_queue
        self.instance_number = instance_number
        self.clients = []  # List to store connected clients

    def add_connection(self, client_socket):
        if self.current_connections < self.max_connections:
            self.current_connections += 1
            self.clients.append(client_socket)
            self.update_queue.put(("connect", self.instance_number, self.current_connections - 1))
            return True
        else:
            return False

    def remove_connection(self, client_socket):
        if self.current_connections > 0:
            self.current_connections -= 1
            self.clients.remove(client_socket)
            self.update_queue.put(("disconnect", self.instance_number, self.current_connections))

    def send_to_all(self, message):  # Send message to all connected clients
        for client_socket in self.clients:
            client_socket.send(message.encode())

def handle_client(client_socket, instance):
    try:
        while True:
            message = client_socket.recv(1024).decode()
            print(f"Received: {message}")

            if message.lower() == "quit":
                break

            instance.send_to_all(f"Echo: {message}")  # Send message to all connected clients
    except ConnectionResetError:
        print("Connection closed by client")
    finally:
        instance.remove_connection(client_socket)
        client_socket.close()


def start_server(host, port):
    update_queue = queue.Queue()

    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Server Status")
    clock = pygame.time.Clock()

    instances = [ServerInstance(2, update_queue, i) for i in range(2)]

    threading.Thread(target=accept_clients, args=(host, port, instances)).start()

    clients = [[False, False], [False, False]]

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            while not update_queue.empty():
                action, instance_number, player_number = update_queue.get()
                if action == "connect":
                    clients[instance_number][player_number] = True
                elif action == "disconnect":
                    clients[instance_number][player_number] = False

            screen.fill((255, 255, 255))

            font = pygame.font.Font(None, 24)

            for i, instance in enumerate(clients):
                for j, client_connected in enumerate(instance):
                    pygame.draw.rect(screen, (0, 0, 0), (200 * j, 200 * i, 100, 100), 2)
                    if client_connected:
                        pygame.draw.circle(screen, (0, 0, 0), (200 * j + 50, 200 * i + 50), 25)

                    # Add label for each instance and player slot
                    text = font.render(f"Instance {i + 1}, Player {j + 1}", True, (0, 0, 0))
                    screen.blit(text, (200 * j, 200 * i + 120))

            pygame.display.flip()
            clock.tick(60)


    except pygame.error:
        return

def accept_clients(host, port, instances):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()

    print(f"Server is listening on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection attempt from {client_address}")

        for i, instance in enumerate(instances):
            if instance.add_connection(client_socket):
                print(f"Connected to instance {i + 1} with {client_address}")
                client_socket.send(f"Connected to instance {i + 1}".encode())  # send instance number to client
                client_handler = threading.Thread(target=handle_client, args=(client_socket, instance))
                client_handler.start()
                break
        else:
            print("All instances are full.")
            client_socket.send("Server full".encode())
            client_socket.close()



if __name__ == "__main__":
    start_server("localhost", 12345)
