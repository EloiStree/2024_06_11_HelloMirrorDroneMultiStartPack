import socket
import struct
import datetime
import random
import time

my_index=45
my_integer = 275757575
now_utc = int(datetime.datetime.now(datetime.UTC).timestamp())


while True:

    my_integer=200000000
    my_integer += random.randint(10000000, 99999999)
    now_utc = int(datetime.datetime.now(datetime.UTC).timestamp())
    # Convert the integer and ulong to bytes
    integer_bytes = struct.pack('iiQ', my_index,my_integer,now_utc)

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the destination IP address and port
    ip_address = '127.0.0.1'
    port = 2561

    # Send the integer bytes
    sock.sendto(integer_bytes, (ip_address, port))

    time.sleep(1)


sock.close()