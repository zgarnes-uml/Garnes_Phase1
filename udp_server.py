#Zachary Garnes
#University of Massachusetts - Lowell
#Student ID# 01353567

import socket # Import the socket module to enable network communication
SERVER_IP = "127.0.0.1" # IP address of the UDP server, localhost
SERVER_PORT = 12025 # Port number of the UDP server


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a UDP socket, AF_INET specifies IPv4, SOCK_DGRAM specifies UDP (connectionless)
    sock.bind((SERVER_IP, SERVER_PORT))# Bind the socket to the IP address and port
    print("UDP server is ready to receive")# Print a message so the user knows the server is running

    # Enter an infinite loop so the server keeps running
    while True:
        data, client_addr = sock.recvfrom(2048)  # Receive data from a client
        message = data.decode() # Decode the received bytes into a string
        print(f"Received from {client_addr}: {message}") # Print the received message and the client’s address (IP, port)
        sock.sendto(data, client_addr) # Echo the same data back to the client
        print(f"Echoed back to {client_addr}") # Confirm that the echo was sent

# Ensure main() only runs when this file is executed directly
if __name__ == "__main__":
    main()

