import pygame
import sys
import socket
import threading
import queue

def handle_socket(client_socket, message_queue, instance_number):
    while True:
        response = client_socket.recv(1024).decode()
        if response:
            if response.startswith("Connected to instance"):
                instance_number[0] = int(response.split()[-1])
            else:
                message_queue.put((instance_number[0], response))  # add instance number to message queue

def start_client(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    message_queue = queue.Queue()  # create a new queue
    instance_number = [None]  # use list so it can be updated in other threads
    threading.Thread(target=handle_socket, args=(client_socket,message_queue, instance_number)).start()

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    font = pygame.font.Font(None, 24)
    input_box = pygame.Rect(25, 550, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    messages = []

    while not done:
        while not message_queue.empty():
            instance, msg = message_queue.get()  # get instance number and message from queue
            messages.append((instance, msg))  # add instance number to messages list

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        print(text)
                        client_socket.send(text.encode())
                        text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))

        # Render messages:
        for i, (instance, msg) in enumerate(messages[-10:]):
            msg_surface = font.render(f"Instance {instance}: {msg}", True, pygame.Color('white'))
            screen.blit(msg_surface, (20, 20 + i * 40))

        txt_surface = font.render(text, True, color)
        width = max(350, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    pygame.quit()
    client_socket.close()

if __name__ == "__main__":
    start_client("localhost", 12345)
