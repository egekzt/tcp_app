import socket
import struct
def send_message(client_socket, message):
    # Pack the message length as a 4-byte integer in network byte order
    message_length = len(message)
    message_length_bytes = struct.pack('!I', message_length)

    # Send the message length to the server
    client_socket.sendall(message_length_bytes)

    # Send the message data to the server
    client_socket.sendall(message.encode())
    if message == quit:
        client_socket.close()

def receive_message(client_socket):
    # Receive the length of the response message
    response_length_bytes = client_socket.recv(4)

    # Unpack the response length as a 4-byte integer in network byte order
    response_length = struct.unpack('!I', response_length_bytes)[0]

    # Receive the response message data
    response_data = b''
    while len(response_data) < response_length:
        data = client_socket.recv(response_length - len(response_data))
        if not data:
             break
        response_data += data

    # Decode the response message data
    response_message = response_data.decode()

    # Handle the response message
    if response_message == 'Invalid command':
        print('Server received an invalid command')
    else:
        print('Received message:', response_message)

    # Close the connection to the server if the response message is 'Take care'
    if response_message == 'Take care':
        client_socket.close()

def main():
    # Connect to the server
    host = 'localhost'
    port = 5000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send messages to the server
    while True:
        message = input('Enter message (type quit to exit): ')
        send_message(client_socket, message)
        receive_message(client_socket)
        if message == 'quit':
            break

if __name__ == '__main__':
    main()
