import subprocess
import os
import multiprocessing
class Command(object):
	def __init__(self):
		pass
	def setUbuntuCommand(self,cmd):
		self.cmd=cmd
	def setUbuntuRootPass(self,passwd):
		self.passwd=passwd
	def setStatus(self,status):
		self.status=status

	def importRepoFile(self,filename,passwd):
		f=open('/tmp/sources.list','wb')
		f.write(filename)
		cmd='mv /tmp/sources.list /etc/apt/'
		z=os.system('echo %s|sudo -S %s' % (passwd,cmd))		
		f.close()
		self.status='file repo has updated'
	
	def updateRepoUbuntu(self,passwd,cmd):
		p=subprocess.Popen('echo %s|sudo -S %s' % (passwd,cmd),bufsize=1, shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True) #previledge untuk update
		self.status=str(p.stdout.read())
	def upInterface(self):
		iface =subprocess.Popen('ifconfig',stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		x=str(iface.stdout.read())
		self.iface=str(x[0:4])
	def installOrRemoveUbuntuApp(self,passwd,cmd):
		subp =subprocess.Popen('echo %s| sudo -S %s' %(passwd,cmd), shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		self.status=str(subp.stdout.read())
	
	def shutdownOrRestart(self,passwd,cmd):
		subp =subprocess.Popen('echo %s| sudo -S %s' %(passwd,cmd), shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		self.status=str(subp.stdout.read())
	def packageName(self):
		pkl=subprocess.Popen((['apt-cache','pkgnames']),stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.pklResult=pkl.stdout.readlines()
	def versionPackage(self,pkgname):
		vpkl=subprocess.Popen((['apt-cache','showpkg',pkgname]),stdin=subprocess.PIPE,stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
		self.vpklResult=vpkl.stdout.readlines()
	
	def getPackageNameList(self,pklist):
		listpkg=[]
		for i in pklist:
			pkg =str(i)
			listpkg.append(pkg[:-1])
		return listpkg
	def getVersionPackageList(self,vpkgresult):
		vpackage=''
		count=2
		for i in vpkgresult:
			if count>=0:
				if count==0:
					infoversi=str(i)
					for letter in infoversi:
						if letter == ' ':
							break
						else:
							vpackage=vpackage+letter
			else:
				break
			count=count-1
		return vpackage
	def getVersionPackage(self):
		return self.vpklResult

	def getPackageName(self):
		return self.pklResult
	def getInterface(self):
		return self.iface

	def getUbuntuCommand(self):
		return self.cmd

	def getUbuntuRootPass(self):
		return self.passwd

	def getStatus(self):
		return self.status
