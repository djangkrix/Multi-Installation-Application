import socket
import sys
import select
import os
import gtk
import time
import gobject
from communication import send, receive
from multiprocessing import Process,Queue
import progressbar
import subprocess
import signal

BUFSIZ = 1024

class client(object):
    def getClientSocket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self.sock
               
    def checkUpIpAddr(self,addr):
        self.getClientSocket()
        self.sock.settimeout(0.01)    ## set a timeout of 0.01 sec
        self.version=sys.platform
        if not self.sock.connect_ex((addr,50014)):    # connect to the remote host on port 445
            self.sock.close()                       ## (port 135 is always open on Windows machines, AFAIK)
            return 1
        else:
            self.sock.close()
    def dataSend(self,passw,data):
        self.dataSend=passw+' '+data
        return self.dataSend
    def getData(self,que):
        inputs = [self.s,sys.stdin]
        self.outputs = []
        data=''
        datalist=[]
        while True:
            try:
                inputready,outputready,exceptready = select.select(inputs, self.outputs, [])
            except select.error, e:
                break
            except socket.error, e:
                break
           
            for s in inputready:
                if s == self.s:
                    #print self.s
                    #print 'tunggu dulu...'
                    data = receive(self.s)
                    datalist.append(data)
                    #time.sleep(2)
                    #break
                else:
                    #print 'tunggu...'
                    time.sleep(1)
            if datalist:
                break
        que.put(datalist)
    def pendingData(self,q1):
        pending=subprocess.Popen(['python','progressbar.py']).pid
        q1.put(pending)
    def runClient(self,filename, host, port, passw):
        self.filename =filename
        self.port = int(port)
        self.host=host
        self.passw=passw
        que=Queue()
        q1=Queue()
        self.data=''
        self.flag=False
        
        try:
            
            self.s=self.getClientSocket()
            self.s.connect((self.host, self.port))
            if self.filename[:1] == '~' :
                tempToSend=self.dataSend(self.passw,self.filename)
            else:
                self.file=open(self.filename, 'rb')
                while True:
                    self.data = self.file.read(1024)
                    if not self.data:break
                    tempToSend=self.dataSend(self.passw,self.data)
            send(self.s,tempToSend)
            q=Process(target=self.getData,args=(que,))
            p=Process(target=self.pendingData,args=(q1,))
            q.start()
            p.start()
            self.data=que.get()
            self.pid=q1.get()
            #q.terminate()
            if self.data:
                self.flag = False
            print 'sudah terima'
            if self.flag == False:
                
                os.kill(self.pid, signal.SIGTERM)
                p.terminate()
                #p.join()

            # Contains client address, set it
            addr = self.data
            print self.data

            return addr
            messg='repo updated..>!!!!'
            print messg
        except socket.error, e:
            print 'Could not connect to server @%d' % self.port
            sys.exit(1)
        self.s.close()
    def runRestart(self,filename, host, port, passw):
        self.filename =filename
        self.port = int(port)
        self.host=host
        self.passw=passw
        que=Queue()
        # Quit flag
        self.data=''
        self.flag=False
        self.hsl=[]
        
        # Initial prompt
        # Connect to server at port
        try:
            #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s=self.getClientSocket()
            self.s.connect((self.host, self.port))
            #print 'Connected to chat server@%d' % self.port
            # Send my name...
            if self.filename[:1] == 'R' :
                tempToSend=self.dataSend(self.passw,self.filename)
                self.hsl.append('REBOOT')
            elif self.filename[:1] == 'S':
                tempToSend=self.dataSend(self.passw,self.filename)
                self.hsl.append('SHUTDOWN')
            else:
                pass
            send(self.s,tempToSend)
            addr=socket.gethostbyname(socket.gethostname())
            self.hsl.append(addr)
            return self.hsl
        except socket.error, e:
            print 'Could not connect to server @%d' % self.port
            sys.exit(1)
        self.s.close()
    
                
