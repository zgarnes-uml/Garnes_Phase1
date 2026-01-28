#Zachary Garnes
#University of Massachusetts - Lowell
#Student ID# 01353567

import socket # Import the socket module for UDP communication
import struct # Import struct for packing and unpacking binary packet headers

SERVER_IP = "127.0.0.1"# IP address of the UDP server, localhost
SERVER_PORT = 5020 # Port number of the UDP server

# Header format string for struct
# !   -> network byte order (big-endian)
# I   -> unsigned 32-bit integer (4 bytes)
# III -> three unsigned integers: seq, total_packets, payload_length
HEADER_FMT = "!III"
HEADER_SIZE = struct.calcsize(HEADER_FMT) # Calculate the size of the header in bytes (12 bytes)
PAYLOAD_SIZE = 1024 # Maximum number of bytes for packet payload
PACKET_SIZE = HEADER_SIZE + PAYLOAD_SIZE # Maximum total UDP packet size (header + payload)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket, AF_INET specifies IPv4, SOCK_DGRAM specifies UDP (connectionless)
    sock.bind((SERVER_IP, SERVER_PORT)) # Bind the socket to the IP address and port
    print("RDT1.0 UDP server  is ready to receive")
    expected_seq = 0   # Sequence number of the next packet the server expects
    total_packets = None   # Total number of packets expected for this transfer, not known until first packet
    received_data = bytearray()   # Bytearray used to accumulate file data in order

    # Enter loop to continuously receive packets
    while True:
        packet, client_addr = sock.recvfrom(PACKET_SIZE)   # Receive a UDP packet (blocking call)

        # Extract and decode the header fields from the packet
        seq, total, length = struct.unpack(
            HEADER_FMT,
            packet[:HEADER_SIZE]
        )
        payload = packet[HEADER_SIZE:HEADER_SIZE + length] # Extract the payload using the payload length from the header

        # If this is the first packet, record how many packets to expect
        if total_packets is None:
            total_packets = total
            print(
                f"File transfer started from {client_addr}, "
                f"expecting {total_packets} packets")

        # RDT 1.0 assumes no loss and in-order delivery
        received_data.extend(payload) # Append the received payload to the output buffer
        expected_seq += 1    # Increment expected sequence number

        # Print progress periodically
        if expected_seq % 50 == 0 or expected_seq == total_packets:
            print(f"Received {expected_seq}/{total_packets} packets")

        # Check if all packets have been received
        if total_packets is not None and expected_seq >= total_packets:
            # Write the reassembled data to a BMP file
            output_filename = "received.bmp"
            with open(output_filename, "wb") as f:
                f.write(received_data)
            print(
                f"File transfer complete. "
                f"Wrote {len(received_data)} bytes to {output_filename}")
            break

    # Close the socket after the transfer completes
    sock.close()

# Ensure main() runs only when executed directly
if __name__ == "__main__":
    main()
