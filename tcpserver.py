import socket
import struct
import threading

def handle_client(client_socket, client_address):
    while True:
        # Receive the length prefix of the message
        message_length_bytes = client_socket.recv(4)

        # Unpack the message length as a 4-byte integer in network byte order
        message_length = struct.unpack('!I', message_length_bytes)[0]

        # Receive the client's message
        data = b''
        while len(data) < message_length:
            chunk = client_socket.recv(message_length - len(data))
            if not chunk:
                break
            data += chunk

        if not data:
            break

        # Check if the client wants to quit
        if data.decode() == 'quit':
            print('Client', client_address, 'is quitting...')
            response = 'take care'
             # Get the length of the response data
            response_length = len(response)

        # Pack the response length as a 4-byte integer in network byte order
            response_length_bytes = struct.pack('!I', response_length)

        # Send the response length and response to the client
            client_socket.sendall(response_length_bytes)
            client_socket.sendall(response.encode())
            break

        # Process the client's message and send a response
        print(data.decode())
        if data == b'Hello':
            response = 'hello'
        elif data == b'How are you?':
            response = 'good and you!'
        elif data == b'Goodbye':
            response = 'bai bai'
        else:
            response = 'Invalid command'

        # Get the length of the response data
        response_length = len(response)

        # Pack the response length as a 4-byte integer in network byte order
        response_length_bytes = struct.pack('!I', response_length)

        # Send the response length and response to the client
        client_socket.sendall(response_length_bytes)
        client_socket.sendall(response.encode())

    # Close the connection to the client
    client_socket.close()



# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_address = ('localhost', 5000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(5)
print("Server is listening on", server_address)

while True:
    # Wait for a connection
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print("Accepted connection from", client_address)

    # Start a new thread to handle the connection
    t = threading.Thread(target=handle_client, args=(client_socket, client_address))
    t.start()
