import socket
import time

server_ip = '192.168.1.127'  # Replace with the private IP of Device A
server_port = 5005

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, server_port))
server_socket.listen()

print("Server listening on {}:{}".format(server_ip, server_port))

while True:
    client_socket, client_address = server_socket.accept()
    print("Connected to client:", client_address)

    while True:
        # Send data to the client every 5 seconds
        data_to_send = b'This is the data from the server!'
        client_socket.send(data_to_send)

        # Wait for 5 seconds before sending the next data
        time.sleep(5)

    client_socket.close()