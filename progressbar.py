import pygtk
import gtk
import gobject
import time

class ProgressBar():
	def __init__(self):
		
		builder = gtk.Builder()
		builder.add_from_file('progressbar.xml')
		builder.connect_signals(self)
		#self.progressbar = builder.get_object('progressbar')
		self.progressbar1 = builder.get_object('progressbar1')
		self.progressbar1.pulse()
		gobject.timeout_add(100, self.update_progress_bar)
		#self.start = time.time()


		
		
		#================================
		self.window2 = builder.get_object('window2')
		self.window2.show()
	def update_progress_bar(self):
		self.progressbar1.pulse()
		return True
	def on_delete_event(self,widget,event):
   		
   		return True
	def hide(self):
		self.window2.hide()
	def on_window2_destroy(self,widget,data=None):
		gtk.main_quit()
		#self.window2.hide()
	
if __name__ == "__main__":
    gtkSign=ProgressBar()
    gtk.main()
