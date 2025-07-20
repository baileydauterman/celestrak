import requests
from time import sleep

args = sys.argv[1:]
if len(args) != 2:
    raise Exception("Usage: tcp_client <ip> <port>")

HOST = args[0]
PORT = args[1]

session = requests.Session()
session.headers.update({'Connection': 'keep-alive'}) # Explicitly set keep-alive header

url = f'http://{HOST}:{PORT}/currentTime'


while True:
    response2 = session.get(url) # Subsequent requests will reuse the same connection
    print(response2.content)
