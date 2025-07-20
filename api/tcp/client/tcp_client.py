import socket
import sys

args = sys.argv[1:]
if len(args) != 2:
    raise Exception("Usage: tcp_client <ip> <port>")

HOST = args[0]
PORT = args[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print(f"Attempting connection to: {HOST}:{PORT}")
    s.connect((HOST, PORT))
    
    while True:
        data = s.recv(33).decode()
        print(data)
