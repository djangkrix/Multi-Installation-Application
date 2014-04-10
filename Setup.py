import subprocess
import os
import getpass
passwd=getpass.getpass('Enter your root password : ')
print passwd

p=subprocess.Popen('pwd',bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
path=str(p.stdout.read()[:-1])
print path
cmd ='cp -r '+path+' $HOME/'
p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
status=str(p.stdout.read())
print status

cmd ='mkdir /usr/local/lib/mipc-gui'
p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
status=str(p.stdout.read())
print status


cmd ='cp $HOME/mipc/gui_pa1.xml /usr/local/lib/mipc-gui/'
p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
status=str(p.stdout.read())
print status

cmd='chmod +x $HOME/mipc/runClient'
p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
status=str(p.stdout.read())
print status

cmd='ln -s $HOME/mipc/runClient /usr/local/bin/mipc-admin'
p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
status=str(p.stdout.read())
print status

cmd ='cp $HOME/mipc/runServer /etc/init.d/'
p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
status=str(p.stdout.read())
print status

cmd='chmod +x /etc/init.d/runServer'
p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
status=str(p.stdout.read())
print status


cmd='update-rc.d -f runServer start 99 2 3 4 5 .'
p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
status=str(p.stdout.read())
print status

