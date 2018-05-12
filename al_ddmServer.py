import os
import requests
import threading
import time

class ddm:
    def __init__(self, portno):
        self.port = portno
        self.host = gethostname()
        self.serversoc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversoc.bind((self.host, self.port))
        self.serversoc.listen(5)

        self.socketslist = [self.serversoc]
        
    def catchservers():
        print("Starting to catch servers :) \nWait for 10 seconds")
        st = time.time()


if __name__=="__main__":
    obj = ddm(arg[1])
    obj.catchservers()
