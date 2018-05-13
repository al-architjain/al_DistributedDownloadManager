import socket
import sys
import requests
import threading
import time
import select

clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = int(sys.argv[1])

clientsock.connect((host,port))

msg  = clientsock.recv(1024).decode('ascii')
print(msg)


url = clientsock.recv(1024).decode('ascii')
print("URL received! = %s" %url)

start = clientsock.recv(32).decode('ascii')
print("Start received!= %s " %start)

end = clientsock.recv(32).decode('ascii')
print("End received! = %s" %end)

start = int(start)
end = int(end)
header={'Range':"bytes=%d-%d"%(start,end)}

r = requests.get(url, headers=header, stream=True)

print("Starting download.....")
for chunk in r.iter_content(chunk_size=1024*1024):
    if chunk:
        clientsock.send(chunk)

clientsock.send("EOFREACHEDKABOOM".encode('ascii'))
print("Downloading finished!")


