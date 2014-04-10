import select
import socket
import sys
import signal
import fcntl
import struct
from communication import send, receive
import command
import subprocess
import multiprocessing
import time
BUFSIZ = 2048


class Server(object):
    port=50014
    backlog=5
    def __init__(self):
        self.clients = 0
        self.command=command.Command()
        self.clientmap = {}
        self.outputs = []
   
    def socketConnection(self):
        port=50014
        backlog=5
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('',port))
        print 'Listening to port',port,'...'
        self.server.listen(backlog)
        self.server.setblocking(1)
    def getSocketConnection(self):
        return self.server
        
    def sigHandler(self, signum, frame):
        # Close the server
        print 'Shutting down server...'
        # Close existing client sockets
        for o in self.outputs:
            o.close()
        
        self.server.close()
      
    def setClientData(self,sockets):
        try:
            client, address = sockets.accept()
            print 'MIA server: got connection %d from %s' % (client.fileno(), address)
            self.dataClient = receive(client)
            self.client=client
            self.address=address
        except socket.error,e:
            print e
        return self.client
        #sockets.close()
    def setClientDataDetail(self,data):
        passwd=''
        prefix=''
        #if not data:break
        for letter in data:
            if letter.isspace():    # memilah data dengan password
                break
            else:
                passwd=passwd + letter
                prefix=passwd +' '
        self.dataDetailClient=data.strip(prefix)
        self.passwd=passwd
    def getName(self, client):
        info = self.clientmap[client]
        host, name = info[0][0], info[1]
        return '@'.join((name, host))

    def getIpAddress(self,ifname):
        sx = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(sx.fileno(),0x8915, struct.pack('256s',ifname[:15]))[20:24])
        
    def getPassFromClient(self):
        return self.passwd
    def getClientData(self):
        return self.dataClient

    def getClientDataDetail(self):
        return self.dataDetailClient

    def serve(self):
        
        #inputs = [self.server,sys.stdin]
        #self.outputs = []

        running = 1

        while running:
            
            self.s=self.getSocketConnection()
            
            cl=self.setClientData(self.s)
            
            v=self.getClientData()
            if v=='':
                
                cl.close()
            else:
                self.setClientDataDetail(self.getClientData())
                
                dataDetail=self.getClientDataDetail()
                
                passwd=self.getPassFromClient()
                
                if dataDetail[:1] == 'R':
                    self.command.setUbuntuRootPass(passwd)
                    cmd1 = 'reboot'
                    self.command.setUbuntuCommand(cmd1)
                    self.command.shutdownOrRestart(self.command.getUbuntuRootPass(),self.command.getUbuntuCommand())
                elif dataDetail[:1] =='S':
                    self.command.setUbuntuRootPass(passwd)
                    cmd1 = 'shutdown -h now'
                    self.command.setUbuntuCommand(cmd1)
                    self.command.shutdownOrRestart(self.command.getUbuntuRootPass(),self.command.getUbuntuCommand())

                elif dataDetail[:1] == '~':
                    messg=''
                    sendData=[]
                    data1 = dataDetail.strip('~')
                    if dataDetail[1:2] == '~':
                        data2=data1.strip('~')
                        p=subprocess.Popen((['dpkg','--get-selections',data2]),stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                        stat = str(p.stdout.read())
                        if stat.find('install') != -1:
                            cmd = "apt-get -y autoremove --purge "+data2
                            self.command.setUbuntuCommand(cmd)
                            self.command.setUbuntuRootPass(self.passwd)              
                            self.command.installOrRemoveUbuntuApp(self.command.getUbuntuRootPass(),self.command.getUbuntuCommand())  
                            x=str(self.command.getStatus())
                            if x.find('Failed') != -1:
                                messg='RFAILED'
                            elif x.find('incorrect password attempts') != -1:
                                messg='UINPASS'
                            else:
                                messg='RSUCCESS'

                            print x
                        else :
                            messg='NOTINSTALLED'
                                    
                    else:
                        p=subprocess.Popen((['dpkg','--get-selections',data1]),stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                        stat = str(p.stdout.read())
                        if stat.find('install') != -1:
                            messg='INSTALLED'
                        elif stat.find('incorrect password attempts') != -1:
                            messg='UINPASS'
                        else :
                            cmd = "apt-get -y install "+data1
                            data2=data1
                            self.command.setUbuntuCommand(cmd)
                            self.command.setUbuntuRootPass(self.passwd)              
                            self.command.installOrRemoveUbuntuApp(self.command.getUbuntuRootPass(),self.command.getUbuntuCommand())  
                            x=self.command.getStatus()
                            x=str(self.command.getStatus())
                            if x.find('Failed') != -1:
                                messg='IFAILED'
                            elif x.find('unmet dependencies') != -1:
                                messg='NOTDEPENDS'
                            else:
                                messg='ISUCCESS'
                            print x
                    self.command.upInterface()
                    iface=self.command.getInterface()
                    tempSend1=self.getIpAddress(iface)
                    sendData.append(tempSend1)
                    sendData.append(messg)
                    sendData.append(data2)


                    send(self.client, sendData)
                else:
                    messg=''
                    self.command.setUbuntuRootPass(passwd)
                    self.command.importRepoFile(dataDetail,self.command.getUbuntuRootPass())
                    cmd1 = 'apt-get update'
                    self.command.setUbuntuCommand(cmd1)
                    self.command.updateRepoUbuntu(self.command.getUbuntuRootPass(),self.command.getUbuntuCommand())
                    x=str(self.command.getStatus())
                    if x.find('Failed') != -1:
                        messg='UFAILED'
                    elif x.find('incorrect password attempts') != -1:
                        messg='UINPASS'
                    else:
                        messg='USUCCESS'
                    print x
                    self.command.upInterface()
                    iface=self.command.getInterface()
                    tempSend=self.getIpAddress(iface)
                    sendData=[]
                    sendData.append(tempSend)
                    sendData.append(messg)
                    send(self.client, sendData)
                    print sendData
                    cl.close()

if __name__ == "__main__":
    server=Server()
    server.socketConnection()
    server.serve()
