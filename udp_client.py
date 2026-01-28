#Zachary Garnes
#University of Massachusetts - Lowell
#Student ID# 01353567

import socket # Import the socket module to enable network communication
SERVER_IP = "127.0.0.1" # IP address of the UDP server, localhost
SERVER_PORT = 12011 # Port number of the UDP server
CLIENT_IP = "127.0.0.1" # Client IP address, localhost same as UDP server
CLIENT_PORT = 12010 # Client port number, different from server


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a UDP socket, AF_INET specifies IPv4, SOCK_DGRAM specifies UDP (connectionless)
    sock.bind((CLIENT_IP, CLIENT_PORT)) # Bind the socket to the client IP and port, allows the server to send responses back to this port
    hello_message = "HELLO"  # Define the message to send
    sock.sendto(hello_message.encode(), (SERVER_IP, SERVER_PORT)) # Convert the string to bytes and send it to the server
    print(f"Sent: {hello_message}")
    data, server_addr = sock.recvfrom(2048)  # Wait for the server to echo the message back
    print("Echo received:", data.decode())    # Decode the received bytes into a string and print it
    sock.close()# Close the socket to release system resources

# Ensure main() only runs when this file is executed directly
if __name__ == "__main__":
    main()
