import os
import sys
import requests
import socket
import threading
import time
import select

class ddm:
    def __init__(self, portno):
        self.port = portno
        self.host = socket.gethostname()
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversock.bind(("", self.port))
        self.serversock.listen(5)

        self.socketlist = [self.serversock]
        self.threads = 0
    
    def Handler(self,start, end, url, filename, sock, threadnum):
        print("Starting thread ",threadnum)
        
        print("sending url.... to thread ", threadnum)
        sock.send(url.encode('ascii'))
        start = '%32s' %start
        print("Sending start = %s" %start)
        sock.send(start.encode('ascii'))
        end =  '%32s' %end
        print("sending end = %s" %end)
        sock.send(end.encode('ascii'))

        start = int(start)
        end = int(end)
        with open(filename,"r+b") as fp:
            msg = sock.recv(1024*1024)
            fp.seek(start)
            var=fp.tell()
            while(msg != "EOFREACHEDKABOOM".encode('ascii')):
                fp.write(msg)
                msg=sock.recv(1024*1024)
                if not msg:
                    break

        print("Thread %d Download finished :)"%threadnum)

        
    def distdownload(self):
        file_name = str(input("Enter file name: "))
        url_of_file = str(input("Enter url of file: "))
        
        r = requests.head(url_of_file)
        file_size = int(r.headers['content-length'])
        print("File length is : %d" %file_size)

        part = int(file_size) // self.threads
        fp = open(file_name,"w")
        fp.write('\0' * file_size)
        fp.close()

        for i in range(self.threads):
            starts = i*part
            end = starts + part
            t = threading.Thread(target=self.Handler,kwargs={'start':starts, 'end':end, 'url':url_of_file, 'filename':file_name, 'sock':self.socketlist[i+1], 'threadnum':int(i+1)})
            t.setDaemon(True)
            t.start()

        main_thread = threading.current_thread()
        for t in threading.enumerate():
            if t is main_thread:
                continue
            t.join()

        print("Done :)")
        


    def catchservers(self):
        print("Starting to catch servers :) \nWait for 10 seconds")
        st = time.time()
        
        while(time.time() - st <= 10.0):
            (sread, swrite, serr) = select.select( self.socketlist, [], [], 0 )
            
            for sock in sread:
                if sock == self.serversock:
                    self.accept_new_connection()
            

    def accept_new_connection(self):
        newsock, newsockaddr = self.serversock.accept()
        self.socketlist.append( newsock )
        
        self.threads += 1
        print("Thread %s joined" %self.threads)

        msg = "You are thread %s\r\n" %self.threads
        newsock.send( msg.encode('ascii') )

if __name__=="__main__":
    obj = ddm( int(sys.argv[1]) )
    obj.catchservers()
    obj.distdownload()

