import sys
import gtk
import socket
import os
import sys
from datetime import datetime
import select
from communication import send, receive
import client
import database
import command
import time
import threading
from multiprocessing import Process,Queue
	
class MainApplication():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.db=database.database()
		self.klien=client.client()
		self.command=command.Command()
		self.flag = False
		builder = gtk.Builder()
		builder.add_from_file('/usr/local/lib/mipc-gui/gui_pa1.xml')
		builder.connect_signals(self)
		self.rootpass = builder.get_object('rootpass')
		self.startip = builder.get_object('startip')
		self.endip = builder.get_object('endip')
		self.inputapp = builder.get_object('inputapp')
		self.modelipaddrlist = builder.get_object('liststore1')
		self.listipaddrlist = builder.get_object('treeview1')
		self.modelstatus = builder.get_object('liststore2')
		self.liststatus = builder.get_object('treeview4')
		self.listapp = builder.get_object('treeview2')
		self.modelapp = builder.get_object('liststore3')
		self.listpkg = builder.get_object('treeview3')
		self.modelpkg = builder.get_object('liststore4')
		self.importfilerepo = builder.get_object('filechooserbutton1')
		self.dialograngeip = builder.get_object('messagedialog1')
		self.dialogipselect = builder.get_object('messagedialog2')
		self.dialogrootpass = builder.get_object('messagedialog3')
		self.dialogappname = builder.get_object('messagedialog4')
		self.dialogrmapp = builder.get_object('messagedialog5')
		self.dialogfilerepo = builder.get_object('messagedialog6')
		self.dialoginvalid = builder.get_object('messagedialog7')
		self.dialognoip = builder.get_object('messagedialog8')
		self.dialogipresult = builder.get_object('messagedialog9')
		self.dialogabout = builder.get_object('aboutdialog1')
		self.dialogassistant = builder.get_object('assistant1')
		self.dialogpkglist = builder.get_object('dialog1')
		self.dialogprogress = builder.get_object('dialog2')
		self.progressbar1 = builder.get_object('progressbar1')
		self.buttonadd = builder.get_object('add')
		self.buttonrm = builder.get_object('rm')
		#make icon visible
		#make multiple selection
		self.listipaddrlist.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
		self.listpkg.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
		#self.listapp.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
		#make column 1
		column = gtk.TreeViewColumn('Ip Address',gtk.CellRendererText(), text=0)
		column.set_clickable(True)
		column.set_resizable(True)
		self.listipaddrlist.append_column(column)
		#make column 2
		column = gtk.TreeViewColumn('Host Name',gtk.CellRendererText(),text=1)
		column.set_clickable(True)
		column.set_resizable(True)
		self.listipaddrlist.append_column(column)
		
		self.db.createDBIpAddress()
		self.loadListItems()
		#================================
		#make column 1
		columnapp = gtk.TreeViewColumn('Application Name',gtk.CellRendererText(), text=0)
		columnapp.set_clickable(True)
		columnapp.set_resizable(True)
		self.listapp.append_column(columnapp)

		columnapp = gtk.TreeViewColumn('Version',gtk.CellRendererText(), text=1)
		columnapp.set_clickable(True)
		columnapp.set_resizable(True)
		self.listapp.append_column(columnapp)
		#================================
		#make column 1
		columnpkg = gtk.TreeViewColumn('Package Name',gtk.CellRendererText(), text=0)
		columnpkg.set_clickable(True)
		columnpkg.set_resizable(True)
		self.listpkg.append_column(columnpkg)
		'''
		columnpkg = gtk.TreeViewColumn('Version',gtk.CellRendererText(), text=1)
		columnpkg.set_clickable(True)
		columnpkg.set_resizable(True)
		self.listpkg.append_column(columnpkg)'''
		#================================
		
		columnStatus = gtk.TreeViewColumn('From',gtk.CellRendererText(), text=0)
		columnStatus.set_clickable(True)
		columnStatus.set_resizable(True)
		self.liststatus.append_column(columnStatus)
		#make column 2
		columnStatus = gtk.TreeViewColumn('Message',gtk.CellRendererText(),text=1,foreground=2, background=3)
		columnStatus.set_clickable(True)
		columnStatus.set_resizable(True)
		self.liststatus.append_column(columnStatus)
		
		#self.db.createDBStatus()
		#self.loadListStatusItems()
		#self.db.createDBPkg()
		#self.loadListPkgItems()

		#================================
		self.window = builder.get_object('window1')
		self.windowicon = self.window.render_icon(gtk.STOCK_DIALOG_AUTHENTICATION, gtk.ICON_SIZE_MENU)
		self.window.set_icon(self.windowicon)
		self.window.show_all()

	
	
			

	#def foreach(self,model, path, iter, selected):
		#self.selected.append(self.modelipaddrlist.get_value(iter, 0))
	def setSelectedIpAddress(self,model, path, iter, selected):
		self.selected.append(self.modelipaddrlist.get_value(iter, 0))
	def setSelectedPkg(self,model, path, iter, selectedpkg):
		self.selectedpkg.append(self.modelpkg.get_value(iter, 0))
	def setSelectedApp(self,model, path, iter, selectedapp):
		self.selectedapp.remove(self.modelapp.get_path(iter, 0))

	def setResetStartIpAdd(self):
		self.startlist = self.startip.set_text('')
		return self.startlist
	def setResetEndIpAdd(self):
		self.endlist = self.endip.set_text('')
		return self.endlist
	def setResetRootPassword(self):
		self.passwd = self.rootpass.set_text('')
		return self.passwd
	def setResetApplicationName(self):
		self.namaaplikasi = self.inputapp.set_text('')
		return self.namaaplikasi
	def setResetStatusList(self):
		self.modelstatus.clear()

	def getStartIpAdd(self):
		self.startlist = self.startip.get_text().split('.')
		return self.startlist
	def getEndIpAdd(self):
		self.endlist = self.endip.get_text().split('.')
		return self.endlist
	def getRootPassword(self):
		self.passwd = self.rootpass.get_text()
		return self.passwd

	def getSelectedIpAddress(self):
		return self.selected
	
	def getSelectedPkg(self):
		return self.selectedpkg

	def getFilename(self):
		self.filename = self.importfilerepo.get_filename()
		return self.filename

	def getApplicationName(self):
		self.namaaplikasi = self.inputapp.get_text()
		return self.namaaplikasi

	def getDialogIpAddr(self):
		self.dialograngeip.show()

	def getDialogIpAddrSelected(self):
		self.dialogipselect.show()
	def getdDialogFileRepo(self):
		self.dialogfilerepo.show()

	def getDialogRootPass(self):
		self.dialogrootpass.show()

	def getDialogAppName(self):
		self.dialogappname.show()
	def checkStart(self,start):
		for i in start:
			if i.isalpha():
				#self.dialograngeip.show()
				return False
			elif i=='':
				return False
			elif not 0 <= int(i) <= 255:
				#self.dialograngeip.show()
				return False
		
	def checkEnd(self,end):
		for i in end:
			if i.isalpha():
				#self.dialograngeip.show()
				return False
			elif i=='':
				return False
			elif not 0 <= int(i) <= 255:
				#self.dialograngeip.show()
				return False
				
	
	def isValid(self,start,end):
		if len(end)!= 4:
			#self.dialograngeip.show()
			return False
		elif len(start)!= 4:
			#self.dialograngeip.show()
			return False
		elif len(start)!= 4 and len(start)!= 4:
		    #self.dialograngeip.show()
			return False
		  
	

	def loadListItems(self):
		self.modelipaddrlist.clear()
		self.db.setIpAddressTable()
		result =self.db.getIpAddressTable()
		for row in result:
			self.modelipaddrlist.append([row[1],row[2]])
	
	def loadScanningResult(self):
		#alfabeth=[a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]
		#caps=[A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z]
		jml=''
		ipaddlist=[]
		awal=self.getStartIpAdd()
		akhir=self.getEndIpAdd()
		if (self.startip.get_text()==''):
			self.dialograngeip.show()
		elif (self.endip.get_text()=='' ):
			self.dialograngeip.show()
		elif (self.startip.get_text()=='') and (self.endip.get_text()=='' ):
			self.dialograngeip.show()
		elif self.isValid(awal,akhir) == False:
			#print 'invalid ip'
			self.dialoginvalid.show()
		elif self.checkStart(awal) == False:
			#print 'invalid ip'
			self.dialoginvalid.show()
		elif self.checkEnd(akhir) == False:
			#print 'invalid ip'
			self.dialoginvalid.show()

		else:
			
			 
			start2=int(self.getStartIpAdd()[3])
			end2=int(self.getEndIpAdd()[3])
			network = self.getStartIpAdd()[0]+'.'+self.getStartIpAdd()[1]+'.'+self.getStartIpAdd()[2]+'.'
			self.db.deleteAllRow()
			self.loadListItems()
			for ip in xrange(start2,end2):    ## 'ping' addresses 192.168.1.1 to .1.255
				addr = network + str(ip)
				if self.klien.checkUpIpAddr(addr):
					try:
						ipaddlist.append(addr)
						hostname=socket.gethostbyaddr(addr)
						self.db.addNewRow(addr,hostname[0]);
						self.loadListItems()
					except socket.herror,x:
						print "Cannot find name :", x
		#self.engine.close()
			if ipaddlist==[]:
				self.dialognoip.show()			
			else:
				jml=len(ipaddlist)
				jml=str(jml)
				self.dialogipresult.show()


	def loadListStatusItems(self):
		self.modelstatus.clear()
		self.db.setStatusTable()
		result =self.db.getStatusTable();
		for row in result:
			self.modelstatus.append([row[1],row[2]])
	
	def loadListPkgItems(self,pkg):
		self.modelpkg.append([pkg,pkg])
	
	def loadUpdateStatus(self,userinput,iphost,defaultport1,passwd,q):
		messg=''
		dt=[]
		k=self.klien.runClient(userinput,iphost,defaultport1,passwd)
		tm=str(datetime.now())
		for kl in k:
			#dl=[]
			print kl
			if kl[1]=='UFAILED':
				messg='repository failed to be updated on '+tm
			elif kl[1]=='UINPASS':
				messg='incorect password'
			elif kl[1]=='USUCCESS':
				messg='+repository has been updated on '+tm
			else:
				pass
			print messg
			dt.append(kl[0])
			dt.append(messg)

		q.put(dt)

	def loadInstallStatus(self,userinput,iphost,defaultport1,passwd,q)	:
		messg=''
		dt=[]
		k=self.klien.runClient(userinput,iphost,defaultport1,passwd)
		tm=str(datetime.now())
		for kl in k:
			app=str(k[2])
			if kl[1]=='IFAILED':
				messg=app+' fail to be installed on '+tm
			elif kl[1]=='ISUCCESS':
				messg='+'+ app +' success to be installed on '+tm
			elif kl[1]=='NOTDEPENDS':
				messg='there are unmet dependencies on '+tm
			elif kl[1]=='UINPASS':
				messg='incorect password'
			elif kl[1]=='INSTALLED':
				messg=app+' has installed on '+tm
			else:
				pass
			print messg
			dt.append(kl[0])
			dt.append(messg)

		q.put(dt)

	def loadRemoveStatus(self,userinput,iphost,defaultport1,passwd,q)	:
		messg=''
		dt=[]
		k=self.klien.runClient(userinput,iphost,defaultport1,passwd)
		tm=str(datetime.now())
		for kl in k:
			app=str(k[2])
			if kl[1]=='RFAILED':
				messg=app+' fail to be removed on '+tm
			elif kl[1]=='RSUCCESS':
				messg='+'+app+' success to be removed on '+tm
			elif kl[1]=='UINPASS':
				messg='incorect password'
			elif kl[1]=='NOTINSTALLED':
				messg=app+' not installed on '+tm
			else:
				pass
			print messg
			dt.append(kl[0])
			dt.append(messg)

		q.put(dt)
	def loadRestartStatus(self,userinput,iphost,defaultport1,passwd,q)	:
		messg=''
		dt=[]
		kl=self.klien.runRestart(userinput,iphost,defaultport1,passwd)
		tm=str(datetime.now())
		if kl[0]=='REBOOT':
			messg='+rebooting @%s on %s' % (iphost,tm)
		
		else:
			pass
		print messg
		dt.append(kl[1])
		dt.append(messg)

		q.put(dt)
	def loadShutdownStatus(self,userinput,iphost,defaultport1,passwd,q)	:
		messg=''
		dt=[]
		kl=self.klien.runRestart(userinput,iphost,defaultport1,passwd)
		tm=str(datetime.now())
		if kl[0]=='SHUTDOWN':
			messg='+shutting down @%s on %s' % (iphost,tm)
		else:
			pass
		print messg
		dt.append(kl[1])
		dt.append(messg)

		q.put(dt)	
	def loadPkgList(self):
		self.command.packageName()
		pkg=self.command.getPackageName()
		pkglist=self.command.getPackageNameList(pkg)
		pkglist.sort()
		for pkgname in pkglist:
			self.loadListPkgItems(pkgname)
	def insertApp(self):
		self.selectedpkg = []
		self.listpkg.get_selection().selected_foreach(self.setSelectedPkg, self.selectedpkg)
		if self.selectedpkg==[]:
			self.dialogrmapp.show()
		else:
			self.command.versionPackage(self.selectedpkg[0])
			vpkg=self.command.getVersionPackage()
			version=self.command.getVersionPackageList(vpkg)
    			self.modelapp.append([self.selectedpkg[0],version])
  

	
	def on_scan_clicked(self,widget):
		self.loadScanningResult()
	def setRemoveSelected(self):
		self.selectedapp  = self.listapp.get_selection()
	def getRemoveSelected(self):
		return self.selectedapp
	def removeApp(self):
		self.setRemoveSelected()
		self.selectedapp  = self.getRemoveSelected()
		print self.selectedapp
		model, iter, = self.selectedapp.get_selected()
		print iter
		if iter != None:
			path = model.get_path(iter)
			model.remove(iter)
			self.selectedapp.select_path(path)
			if not self.selectedapp.path_is_selected(path):
				row = path[0]-1
				if row >= 0:
					self.selectedapp.select_path((row,))
		else:
			self.dialogrmapp.show()
	def getAllApp(self):
		listapp=[]
		self.listreadyapp=''
		iter = self.modelapp.get_iter_first()
		listapp.append(self.modelapp.get(iter,0))
		try:
			while 1:
				if not iter:break
				iter=self.modelapp.iter_next(iter)
				listapp.append(self.modelapp.get(iter,0))
				
		except Exception,err:
			pass
		#print listapp
		for i in listapp:
			app=str(i).strip("'(),''")
			#print app
			self.listreadyapp=self.listreadyapp+app+' '
			#print self.listreadyapp
		#print self.listreadyapp
		return self.listreadyapp

	def on_update_clicked(self,widget):
		defaultport1 = 50014
		datalist=[]
		hslist=[]
		localhost='127.0.0.1'
		passwd = self.getRootPassword()
		namafile = self.getFilename()
		print namafile
		self.selected = []
		self.listipaddrlist.get_selection().selected_foreach(self.setSelectedIpAddress, self.selected)

		if self.getRootPassword()=='':
			self.getDialogRootPass()
		elif self.getSelectedIpAddress() == []:
			self.getDialogIpAddrSelected()
		elif self.getFilename()==None:
			self.getdDialogFileRepo()
		else:
			#update server-adminself
			self.command.setUbuntuRootPass(passwd)
			self.command.importSelfRepoFile(namafile,self.command.getUbuntuRootPass())
			cmd1 = 'apt-get update'
			self.command.setUbuntuCommand(cmd1)
			self.command.updateRepoUbuntu(self.command.getUbuntuRootPass(),self.command.getUbuntuCommand())
			stat=str(self.command.getStatus())
			print stat
			#end




			q1=Queue() 
			q2=Queue() 
			q3=Queue() 
			q4=Queue() 
			q5=Queue()
			pilihan = self.getSelectedIpAddress()
			panjangpilihan=len(self.getSelectedIpAddress())
			pembagi=(((panjangpilihan-1)/5)+1)
			sisa=panjangpilihan%5
			counter=0
			bagianbesar=[]
			for j in range(pembagi):
				bagian=[]
				if panjangpilihan/5 != 0:
					isi=5
				else:
					isi=panjangpilihan%5
				for i in range(isi):
					ix=i+counter
					bagian.append(pilihan[ix])
				bagianbesar.append(bagian)
				panjangpilihan=panjangpilihan-5
				counter=counter+5
			#print bagianbesar
			
			for iphost in bagianbesar:
				pp=len(iphost)
				try:
					hsl=''
					#t=client.client(namafile, iphost, defaultport1, passwd)
					
					if pp ==1 :
						p1=Process(target=self.loadUpdateStatus,args=(namafile, iphost[0], defaultport1, passwd,q1))
						p1.start()
						p1.join()
						hslist.append(q1.get())
					elif pp>4:
						p1=Process(target=self.loadUpdateStatus,args=(namafile, iphost[0], defaultport1, passwd,q1))
						p2=Process(target=self.loadUpdateStatus,args=(namafile, iphost[1], defaultport1, passwd,q2))
						p3=Process(target=self.loadUpdateStatus,args=(namafile, iphost[2], defaultport1, passwd,q3))
						p4=Process(target=self.loadUpdateStatus,args=(namafile, iphost[3], defaultport1, passwd,q4))
						p5=Process(target=self.loadUpdateStatus,args=(namafile, iphost[4], defaultport1, passwd,q5))
						p1.start()
						p2.start()
						p3.start()
						p4.start()
						p5.start()
						p1.join()
						p2.join()
						p3.join()
						p4.join()
						p5.join()
						hslist.append(q1.get())
						hslist.append(q2.get())
						hslist.append(q3.get())
						hslist.append(q4.get())
						hslist.append(q5.get())
					elif pp>3:
						p1=Process(target=self.loadUpdateStatus,args=(namafile, iphost[0], defaultport1, passwd,q1))
						p2=Process(target=self.loadUpdateStatus,args=(namafile, iphost[1], defaultport1, passwd,q2))
						p3=Process(target=self.loadUpdateStatus,args=(namafile, iphost[2], defaultport1, passwd,q3))
						p4=Process(target=self.loadUpdateStatus,args=(namafile, iphost[3], defaultport1, passwd,q4))
						p1.start()
						p2.start()
						p3.start()
						p4.start()
						p1.join()
						p2.join()
						p3.join()
						p4.join()
						hslist.append(q1.get())
						hslist.append(q2.get())
						hslist.append(q3.get())
						hslist.append(q4.get())
					elif pp>2:
						p1=Process(target=self.loadUpdateStatus,args=(namafile, iphost[0], defaultport1, passwd,q1))
						p2=Process(target=self.loadUpdateStatus,args=(namafile, iphost[1], defaultport1, passwd,q2))
						p3=Process(target=self.loadUpdateStatus,args=(namafile, iphost[2], defaultport1, passwd,q3))
						p1.start()
						p2.start()
						p3.start()
						p1.join()
						p2.join()
						p3.join()
						hslist.append(q1.get())
						hslist.append(q2.get())
						hslist.append(q3.get())
						
					elif pp>1:
						p1=Process(target=self.loadUpdateStatus,args=(namafile, iphost[0], defaultport1, passwd,q1))
						p2=Process(target=self.loadUpdateStatus,args=(namafile, iphost[1], defaultport1, passwd,q2))
						p1.start()
						p2.start()
						p1.join()
						p2.join()
						hslist.append(q1.get())
						hslist.append(q2.get())
					#p.join()
					
					
					
					
					
					#print hslist
					#print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
					#datalist.append(hsl)
					#p.terminate()
				except Exception,err:
					print err
			#print datalist
			for hsl in hslist:
				c=hsl[1]
			
				if c[0] != '+':
						
					self.modelstatus.append([hsl[0],hsl[1],"black","red"])
				else:
 					chsl=c.strip('+')
					self.modelstatus.append([hsl[0],chsl,"black","white"])
					
					
				
	def on_install_clicked(self,widget):
		defaultport1 = 50014
		passwd = self.getRootPassword()
		datalist=[]
		hslist=[]
		self.selected = []
		self.listipaddrlist.get_selection().selected_foreach(self.setSelectedIpAddress, self.selected)
		try:#namaCmd = self.getApplicationName()
			namaCmd = self.getAllApp()
			if self.getRootPassword()=='':
				self.getDialogRootPass()
			elif self.getSelectedIpAddress() == []:
				self.getDialogIpAddrSelected()
			elif self.getAllApp()=='':
				self.getDialogAppName()
			else:
				idnamaCmd = '~' + namaCmd
				#namafile1 = os.path.split(namafile)[1]
				q1=Queue() 
				q2=Queue() 
				q3=Queue() 
				q4=Queue() 
				q5=Queue()
				pilihan = self.getSelectedIpAddress()
				panjangpilihan=len(self.getSelectedIpAddress())
				pembagi=(((panjangpilihan-1)/5)+1)
				sisa=panjangpilihan%5
				counter=0
				bagianbesar=[]
				for j in range(pembagi):
					bagian=[]
					if panjangpilihan/5 != 0:
						isi=5
					else:
						isi=panjangpilihan%5
					for i in range(isi):
						ix=i+counter
						bagian.append(pilihan[ix])
					bagianbesar.append(bagian)
					panjangpilihan=panjangpilihan-5
					counter=counter+5
				#print bagianbesar
			
				for iphost in bagianbesar:
					pp=len(iphost)
					try:
						hsl=''
						#t=client.client(namafile, iphost, defaultport1, passwd)
						#t.start()
						if pp ==1 :
							p1=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p1.start()
							p1.join()
							hslist.append(q1.get())
						elif pp>4:
							p1=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p2=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[1], defaultport1, passwd,q2))
							p3=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[2], defaultport1, passwd,q3))
							p4=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[3], defaultport1, passwd,q4))
							p5=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[4], defaultport1, passwd,q5))
							p1.start()
							p2.start()
							p3.start()
							p4.start()
							p5.start()
							p1.join()
							p2.join()
							p3.join()
							p4.join()
							p5.join()
							hslist.append(q1.get())
							hslist.append(q2.get())
							hslist.append(q3.get())
							hslist.append(q4.get())
							hslist.append(q5.get())
						elif pp>3:
							p1=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p2=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[1], defaultport1, passwd,q2))
							p3=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[2], defaultport1, passwd,q3))
							p4=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[3], defaultport1, passwd,q4))
							p1.start()
							p2.start()
							p3.start()
							p4.start()
							p1.join()
							p2.join()
							p3.join()
							p4.join()
							hslist.append(q1.get())
							hslist.append(q2.get())
							hslist.append(q3.get())
							hslist.append(q4.get())
						elif pp>2:
							p1=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p2=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[1], defaultport1, passwd,q2))
							p3=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[2], defaultport1, passwd,q3))
							p1.start()
							p2.start()
							p3.start()
							p1.join()
							p2.join()
							p3.join()
							hslist.append(q1.get())
							hslist.append(q2.get())
							hslist.append(q3.get())
						
						elif pp>1:
							p1=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p2=Process(target=self.loadInstallStatus,args=(idnamaCmd, iphost[1], defaultport1, passwd,q2))
							p1.start()
							p2.start()
							p1.join()
							p2.join()
							hslist.append(q1.get())
							hslist.append(q2.get())
						
						
					
						
						
						#p.join()
					
					
					
					
					
						#print hslist
						#print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
						#datalist.append(hsl)
						#p.terminate()
					except Exception,err:
						print err
				#print datalist
				for hsl in hslist:
					c=hsl[1]
			
					if c[0] != '+':
						
						self.modelstatus.append([hsl[0],hsl[1],"black","red"])
					else:
 						chsl=c.strip('+')
						self.modelstatus.append([hsl[0],chsl,"black","white"])
		except Exception,err:
			if err:
				self.getDialogAppName()
	
	def on_remove_clicked(self,widget):
		defaultport1 = 50014
		passwd = self.getRootPassword()
		datalist=[]
		hslist=[]
		self.selected = []
		self.listipaddrlist.get_selection().selected_foreach(self.setSelectedIpAddress, self.selected)
		#namaCmd = self.getApplicationName()
		try:#namaCmd = self.getApplicationName()
			namaCmd = self.getAllApp()
			if self.getRootPassword()=='':
				self.getDialogRootPass()
			elif self.getSelectedIpAddress() == []:
				self.getDialogIpAddrSelected()
			elif self.getAllApp()=='':
				self.getDialogAppName()
			else:
				idnamaCmd = '~~' + namaCmd
				#namafile1 = os.path.split(namafile)[1]
				q1=Queue() 
				q2=Queue() 
				q3=Queue() 
				q4=Queue() 
				q5=Queue()
				pilihan = self.getSelectedIpAddress()
				panjangpilihan=len(self.getSelectedIpAddress())
				pembagi=(((panjangpilihan-1)/5)+1)
				sisa=panjangpilihan%5
				counter=0
				bagianbesar=[]
				for j in range(pembagi):
					bagian=[]
					if panjangpilihan/5 != 0:
						isi=5
					else:
						isi=panjangpilihan%5
					for i in range(isi):
						ix=i+counter
						bagian.append(pilihan[ix])
					bagianbesar.append(bagian)
					panjangpilihan=panjangpilihan-5
					counter=counter+5
				#print bagianbesar
			
				for iphost in bagianbesar:
					pp=len(iphost)
					try:
						hsl=''
						#t=client.client(namafile, iphost, defaultport1, passwd)
						#t.start()
						if pp ==1 :
							p1=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p1.start()
							p1.join()
							hslist.append(q1.get())
						elif pp>4:
							p1=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p2=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[1], defaultport1, passwd,q2))
							p3=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[2], defaultport1, passwd,q3))
							p4=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[3], defaultport1, passwd,q4))
							p5=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[4], defaultport1, passwd,q5))
							p1.start()
							p2.start()
							p3.start()
							p4.start()
							p5.start()
							p1.join()
							p2.join()
							p3.join()
							p4.join()
							p5.join()
							hslist.append(q1.get())
							hslist.append(q2.get())
							hslist.append(q3.get())
							hslist.append(q4.get())
							hslist.append(q5.get())
						elif pp>3:
							p1=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p2=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[1], defaultport1, passwd,q2))
							p3=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[2], defaultport1, passwd,q3))
							p4=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[3], defaultport1, passwd,q4))
							p1.start()
							p2.start()
							p3.start()
							p4.start()
							p1.join()
							p2.join()
							p3.join()
							p4.join()
							hslist.append(q1.get())
							hslist.append(q2.get())
							hslist.append(q3.get())
							hslist.append(q4.get())
						elif pp>2:
							p1=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p2=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[1], defaultport1, passwd,q2))
							p3=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[2], defaultport1, passwd,q3))
							p1.start()
							p2.start()
							p3.start()
							p1.join()
							p2.join()
							p3.join()
							hslist.append(q1.get())
							hslist.append(q2.get())
							hslist.append(q3.get())
						
						elif pp>1:
							p1=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[0], defaultport1, passwd,q1))
							p2=Process(target=self.loadRemoveStatus,args=(idnamaCmd, iphost[1], defaultport1, passwd,q2))
							p1.start()
							p2.start()
							p1.join()
							p2.join()
							hslist.append(q1.get())
							hslist.append(q2.get())
						
						
					
						
						
						#p.join()
					
					
					
					
					
						#print hslist
						#print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
						#datalist.append(hsl)
						#p.terminate()
					except Exception,err:
						print err
				#print datalist
				for hsl in hslist:
					c=hsl[1]
			
					if c[0] != '+':
						
						self.modelstatus.append([hsl[0],hsl[1],"black","red"])
					else:
 						chsl=c.strip('+')
						self.modelstatus.append([hsl[0],chsl,"black","white"])
		except Exception,err:
			if err:
				self.getDialogAppName()
	def on_restart_clicked(self,widget):
		defaultport1 = 50014
		passwd = self.getRootPassword()
		self.selected = []
		datalist=[]
		self.listipaddrlist.get_selection().selected_foreach(self.setSelectedIpAddress, self.selected)
		#namaCmd = self.getApplicationName()
		try:#namaCmd = self.getApplicationName()
			
			if self.getRootPassword()=='':
				self.getDialogRootPass()
			elif self.getSelectedIpAddress() == []:
				self.getDialogIpAddrSelected()
			else:
				idnamaCmd = 'R'
				q=Queue() 
				for iphost in self.getSelectedIpAddress():
					try:
						p=Process(target=self.loadRestartStatus,args=(idnamaCmd, iphost, defaultport1, passwd,q))
						p.start()
						#p.join()
						hsl=q.get()
						datalist.append(hsl)
						#p.terminate()
					except Exception,err:
						print err
				for hsl in datalist:
					c1=hsl[0]
					c=hsl[1]
					if c[0] != '+':
						self.modelstatus.append([c1,hsl[1],"black","red"])
							
					else:
						chsl=c.strip('+')
						self.modelstatus.append([c1,chsl,"black","white"])
		except Exception,err:
			if err:
				self.getDialogAppName()
	def on_shutdown_clicked(self,widget):
		defaultport1 = 50014
		passwd = self.getRootPassword()
		self.selected = []
		datalist=[]
		self.listipaddrlist.get_selection().selected_foreach(self.setSelectedIpAddress, self.selected)
		#namaCmd = self.getApplicationName()
		try:
			#namaCmd = self.getApplicationName()
			
			if self.getRootPassword()=='':
				self.getDialogRootPass()
			elif self.getSelectedIpAddress() == []:
				self.getDialogIpAddrSelected()
			else:
				idnamaCmd = 'S' 
				#namafile1 = os.path.split(namafile)[1]
				q=Queue() 
				for iphost in self.getSelectedIpAddress():
					try:
						#t=client.client(namafile, iphost, defaultport1, passwd)
						#t.start()
						p=Process(target=self.loadShutdownStatus,args=(idnamaCmd, iphost, defaultport1, passwd,q))
						p.start()
						#p.join()
						hsl=q.get()
						datalist.append(hsl)
						#p.terminate()
					except Exception,err:
						print err
				for hsl in datalist:
					c1=hsl[0]
					c=hsl[1]
					if c[0] != '+':
						self.modelstatus.append([c1,hsl[1],"black","red"])
							
					else:
						chsl=c.strip('+')
						self.modelstatus.append([c1,chsl,"black","white"])			
		except Exception,err:
			if err:
				self.getDialogAppName()

	def on_add_clicked(self,widget):
		self.dialogpkglist.show()
		self.loadPkgList()
	def on_pkglist_clicked(self,widget):
		self.insertApp()
	def on_rm_clicked(self,widget):
		self.removeApp()
		#self.getAllApp()

	def on_window1_destroy(self, widget, data=None):
		gtk.main_quit()

	def on_dialog_assistant_destroy(self, widget, data=None):
		self.dialogassistant.hide()
	def on_dialog_removeapp_destroy(self, widget, data=None):
		self.dialogrmapp.hide()
	def on_dialog1_destroy(self,widget,data=None):
		self.dialogpkglist.destroy()
	def on_dialog_ip_range_destroy(self, widget, data=None):
		self.dialograngeip.hide()
	def on_dialog_ip_selected_destroy(self, widget, data=None):
		self.dialogipselect.hide()
	def on_dialog_file_repo_destroy(self,widget, data=None):
		self.dialogfilerepo.hide()
	def on_dialog_root_pass_destroy(self, widget, data=None):
		self.dialogrootpass.hide()

	def on_dialog_app_name_destroy(self, widget, data=None):
		self.dialogappname.hide()
	def on_dialog_invalid_ip_destroy(self, widget, data=None):
		self.dialoginvalid.hide()
	def on_dialog_no_ip_destroy(self, widget, data=None):
		self.dialognoip.hide()
	def on_dialog_ip_result_destroy(self, widget, data=None):
		self.dialogipresult.hide()	
	def on_about_menu_destroy(self,widget, data=None):
		self.dialogabout.hide()
	def on_dialog_pkg_list_destroy(self, widget, data=None):
		self.dialogpkglist.hide()
	def on_reset_menu(self, widget):
		self.setResetStartIpAdd()
		self.setResetEndIpAdd()
		self.setResetRootPassword()
		self.modelapp.clear()
		#self.setResetApplicationName()
		self.db.deleteAllRow()
		self.loadListItems()
		#self.db.deleteAllStatusRow()
		self.setResetStatusList()
	def on_delete_event(self,widget,event):
   		return True
	def on_dialog_assistant(self,widget):
		self.dialogassistant.show()

	def on_about_menu(self,widget):
		self.dialogabout.show()
	def on_fullscreen_menu(self,widget):
		self.window.fullscreen()
	def on_leave_fullscreen_menu(self,widget):
		self.window.unfullscreen()

	
   
if __name__ == "__main__":
    gtkSign=MainApplication()
    gtk.main()

