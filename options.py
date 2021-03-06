#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This class represents the main User Interface.
#It give the options to search, view current online streams
#and to view favourites

import gtk,webkit,streamViewer,sys,searchBox,search,onlineStreams,favourites	
	
class Options():
	def __init__(self):
	
		#Setup the main window
		self.options = gtk.Window()
		self.options.set_position(gtk.WIN_POS_CENTER)
		self.options.set_title('Dual Craft')
		self.options.set_default_size(500,500)
		self.options.connect('destroy', lambda w: gtk.main_quit())
		self.b1 = gtk.VBox()
		self.options.add(self.b1)
		self.options.set_default_size(500,500)

		#Create buttons
		self.button1 = gtk.Button("Search")
		self.button2 = gtk.Button("Online")
		self.button3 = gtk.Button('Favourites')

		#Add buttons to the main window
		self.b1.pack_start(self.button1)
		self.b1.pack_start(self.button2)
		self.b1.pack_start(self.button3)
	
		#Set onClick actions
		self.button1.connect('clicked', self.showSearchWindow)
		self.button2.connect('clicked', self.showOnline)
		self.button3.connect('clicked', self.showFavouritesWindow)

		#Show the window
		self.options.show_all()
		gtk.main()

	#Display a search window
	def showSearchWindow(self, object):
		test = searchBox.Main()
	
	#Display category and sub-category options for currently online streams
	def showOnline(self, object):
		s = onlineStreams.streamTypeChoice()
	
	#Show the users favourites
	def showFavouritesWindow(self,object):
		f = favourites.Favourites()
		f.showAll()
		

if __name__ == '__main__':
	sys.exit()
