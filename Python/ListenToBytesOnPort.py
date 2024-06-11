import socket
import struct

UDP_IP = "127.0.0.1"  
UDP_PORT = 2571  

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind((UDP_IP, UDP_PORT))

while True:
    data, addr = sock.recvfrom(1024)

    # Define the format string for the initial part
    header_format_str = 'Bqq'  # 1 byte, 2 unsigned long longs (8 bytes each)
    byte = data[0]
    long1 = struct.unpack("Q",data[1:9])
    long2 =  struct.unpack("Q",data[9:17])
    header_size = 1+8+8
    print((header_size))
  
    # Remaining data after the initial part
    remaining_data = data[header_size:]
    print(len(remaining_data))
    # Define the format string for one set of 3 shorts and 3 bytes
    set_format_str = '3h3B'  # 3 shorts (2 bytes each) and 3 bytes

    # Calculate the size of one set
    set_size = struct.calcsize(set_format_str)

    # Number of sets
    num_sets = len(remaining_data) // set_size

    # Unpack the sets
    sets = []
    for i in range(num_sets):
        start = i * set_size
        end = start + set_size
        sets.append(struct.unpack(set_format_str, remaining_data[start:end]))

    # Display results
    print(f"Byte: {byte}")
    print(f"Long 1: {long1}")
    print(f"Long 2: {long2}")
    print("Sets of 3 shorts and 3 bytes:")
    for i, (short1, short2, short3, byte1, byte2, byte3) in enumerate(sets):
        print(f"Set {i + 1}: Shorts = ({short1}, {short2}, {short3}), Bytes = ({byte1}, {byte2}, {byte3})")