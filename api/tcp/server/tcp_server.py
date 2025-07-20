import sys
import socket
from datetime import datetime, UTC

args = sys.argv[1:]
if len(args) != 2:
    raise Exception("Usage: tcp_server.py <ip> <port")

HOST = args[0]
PORT = args[1]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"Server listening on {HOST}:{PORT}")
    
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        try:
            while True:
                send_data = f"{datetime.now(UTC).isoformat()}\n".encode()
                conn.sendall(send_data)
        except Exception as e:
            print(f"Failed with: {e}")
