#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This class represents a searchBox object.
#It is used when the user wishes to search for a streamer
#either by name or by URL

import gtk,sys,streamViewer,search,streamer,searchResults

class Main():
	def __init__(self):
	
		#Create the main window
		self.searchWindow = gtk.Window()
		self.searchWindow.set_position(gtk.WIN_POS_CENTER)
		self.searchBox = gtk.VBox()
		self.searchBar = gtk.Entry()
		self.searchBox.pack_start(self.searchBar)  
		
		#Create buttons
		self.searchBar.set_text("Enter Search Query")
		self.searchButton = gtk.Button('Search By User')
		self.searchButton3 = gtk.Button('View by URL')

		#Add buttons
		self.searchBox.add(self.searchButton)
		self.searchBox.add(self.searchButton3)
		
		#Set button onClick
		self.searchButton.connect('clicked', self.searchForStream)
		self.searchButton3.connect('clicked', self.viewByUrl)


		self.searchWindow.set_default_size(300,300)
		self.searchWindow.set_title("Search")

		self.searchWindow.add(self.searchBox)
		self.searchWindow.show_all()

	#Function checks if the user provided URL is valid, and creates a 
	#new streamViewer.Main(URL) instance.
	def viewByUrl(self, object):
		#Get whatever URL the user entered
		stream = self.searchBar.get_text()
		
		#Make sure it starts with http://, more validity checking done in 
		#streamViewer
		if stream.startswith("http://"):
				view = streamViewer.Main()
				view.viewByUrl(stream)
		else:
			stream = "http://" + stream
			view = streamViewer.Main()
			view.viewByUrl(stream)

	#Calls instance of search function, with string to be searched for.
	def searchForStream(self, object):
		if self.searchBar.get_text() == "":
			md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
 gtk.MESSAGE_QUESTION,gtk.BUTTONS_CLOSE,"Invalid Search Query")
                        md.run()
                        md.destroy()
                        return
                if self.searchBar.get_text() == "Enter Search Query":
                        md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
 gtk.MESSAGE_QUESTION,gtk.BUTTONS_CLOSE,"Invalid Search Query")
                        md.run()
                        md.destroy()
                        return
                
                searcher = search.Main()
		
		#See if we can find the streamer they're looking for
		streamDetails = searcher.findStreamer(self.searchBar.get_text())
		
		#Streamer not found
		if streamDetails == None:
			self.showNotFound()
		else:
			#Streamer found
			#Popup box to see if the user wants to view said stream.
			pop = searchResults.Main()
			pop.singleStreamer(streamDetails)

	#Popup box to inform the user that the streamer wasn't found.
	def showNotFound(self):
		md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT,
 gtk.MESSAGE_QUESTION,gtk.BUTTONS_CLOSE,"Streamer not found!\nYou may have" + 
" spelled something wrong, or that streamer may be offline!")
		md.run()
		md.destroy()
		
if __name__ == '__main__':
	sys.exit()
