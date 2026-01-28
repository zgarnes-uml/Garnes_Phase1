#Zachary Garnes
#University of Massachusetts - Lowell
#Student ID# 01353567

import socket # Import the socket module for UDP communication
import struct # Import struct for packing and unpacking binary packet headers
import math # Import math for ceiling division (to compute number of packets)
import time # Import time so we can add a tiny delay between packets (helps avoid buffer overflow)
#import os # Import os for checking if the transfer file exists

SERVER_IP = "127.0.0.1"# IP address of the UDP server, localhost
SERVER_PORT = 5020  # Port number of the UDP server

# Header format for packet metadata
# ! -> network byte order (big-endian)
# I -> unsigned 32-bit integer (4 bytes)
# III -> three unsigned ints: seq, total_packets, payload_length
HEADER_FMT = "!III"
HEADER_SIZE = struct.calcsize(HEADER_FMT) # Calculate the size of the header in bytes (12 bytes)
PAYLOAD_SIZE = 1024 # Maximum number of bytes for packet payload


# Function to break the file into packets (Make_Packet step)
def make_packets(file_bytes: bytes):
    # math.ceil ensures we include a final packet if bytes don't divide evenly
    total_packets = math.ceil(len(file_bytes) / PAYLOAD_SIZE)  # Compute how many packets are needed
    packets = []  # List to store all generated packets

    # Loop through each packet index (sequence number)
    for seq in range(total_packets):
        # Calculate byte range for this chunk
        start = seq * PAYLOAD_SIZE
        end = start + PAYLOAD_SIZE
        chunk = file_bytes[start:end]# Extract up to 1024 bytes for the payload
        # Create a 12-byte header with:
        # seq          -> which packet this is
        # total_packets-> total number of packets in the file
        # len(chunk)   -> payload length (last chunk may be smaller than 1024)
        header = struct.pack(HEADER_FMT, seq, total_packets, len(chunk))
        packet = header + chunk  # Packet = header + payload bytes
        packets.append(packet) # Store packet in list
    # Return the list of packets ready to send
    return packets


def main():
    filename = "Donkey_Kong.bmp"    # Name of the BMP file to transfer, in the project folder

    # Open the file in binary mode and read all bytes
    with open(filename, "rb") as f:
        file_bytes = f.read()

    packets = make_packets(file_bytes) # Convert the file bytes into a list of RDT packets
    # Print file size and number of packets
    print(f"File size: {len(file_bytes)} bytes")
    print(f"Total packets: {len(packets)} (payload size: {PAYLOAD_SIZE} bytes)")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Create a UDP socket for sending packets

    # RDT 1.0 assumes the channel is perfectly reliable, so o we do NOT wait for ACKs or retransmit.
    for i, pkt in enumerate(packets):
        sock.sendto(pkt, (SERVER_IP, SERVER_PORT))  # Send the packet to the server address
        # Print progress occasionally
        if (i + 1) % 50 == 0 or (i + 1) == len(packets):
            print(f"Sent {i+1}/{len(packets)} packets")
        time.sleep(0.001) # Small sleep helps reduce packet drops due to OS buffer overflow
    print("Done sending file.")  # Print completion message after sending all packets
    sock.close()   # Close the socket to free resources

# Ensure main() only runs when executed directly (not imported)
if __name__ == "__main__":
    main()
