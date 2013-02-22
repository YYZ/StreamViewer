#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Class to save, load and delete favourites from the hard disk.
#Favourites are stored as XML, similiar to how justin.tv stores them, but with
#less details. Also parsed simliarly.
#Structure : Name, Title, URL, Category, Sub-Category, Game(IF APPLICABLE)

import streamer,streamViewer,gtk,searchResults,favourites,urllib
from lxml import etree
from StringIO import StringIO
import fileinput

class Favourites():
	def __init__(self):
		self.favFile = "favourites.xml"
		self.win = gtk.Window()
	def addFavourite(self, s):
		#Streamer object we're adding to favourites
		st = streamer.Streamer 
		st = s
		
		self.streamers = []
		self.streamers = self.loadFavourites()

		#Now that we have all of the favourites, we check if the streamer we're
		#trying to add is already there
		for x in self.streamers:
			if x.getName() == st.getName(): # He's already in the favourites
				return False

		#st is not already in favourites, so we add it!
		self.streamers.append(st)
		print st.getName()
		
		#If we get to here,then the streamer is not currently in the favourites
		#So we add it.
		self.writeToFav(self.streamers)
		return True

	def writeToFav(self, s):
		#Open file for appending, so we're adding to the end of the file and
		#not overwriting anything
		self.fav = open(self.favFile, "wb")

		#Setup the XMl so the parser won't complain
		self.fav.write("<streams>\n")
		for x in s:
			self.fav.write("<stream>\n")
			self.fav.write("<name>"+x.getName() + "</name>\n")
			self.fav.write("<title>" + x.getTitle() + "</title>\n")
			self.fav.write("<url>" + x.getURL() + "</url>\n")
			self.fav.write("<category>" + x.getCategory() + "</category>\n")
			self.fav.write("<subcategory>" + x.getSubCategory() + "</subcategory>\n")
			self.fav.write("<game>" + x.getGame() + "</game>\n")
			self.fav.write("<online>" + x.getStatus() + "</online>\n")
			self.fav.write("</stream>\n")

		self.fav.write("</streams>")
		self.fav.close()
	
	#Method to remove a streamer from favourites
	def remove(self, s):
		sts = streamer.Streamer
		sts=s
		self.st = []
		st = self.loadFavourites()
		for t in st:
			if t.getName() == sts.getName():
				st.remove(t)
		self.writeToFav(st)
		fav = favourites.Favourites()
		fav.showAll()
		self.win.destroy()
		

	def loadFavourites(self):
		#Get trees ready for searching
		self.a = etree.parse(self.favFile)
		self.b = etree.tostring(self.a)

		#Open favourites file to add the etree
		self.fav = open(self.favFile, "wb")
		self.fav.write(self.b)
		self.fav.close()
		
		#Now we open favourites for reading the XML
		self.fav = open(self.favFile) 

		#Read the contents of fav into the stiring favourites. Needs to be in a
		#string to be parsed
		self.favourites = self.fav.read()

		#Parses the file into an etree object 'parsed'. Enables easy searching.
		self.parsed = etree.iterparse(StringIO(self.favourites))


		#List to store all streamers
		self.streamers = []

		#Used when we're getting the details of each streamer in the fav's file
		parsedStreamer = streamer.Streamer()
		for action, elem in self.parsed:
			#checks for empty file
			if not elem.text:
				pass
			else:
				if elem.tag == 'name':
					parsedStreamer.setName(elem.text)
				if elem.tag == 'title':
					parsedStreamer.setTitle(elem.text)
				if elem.tag == 'url':
					parsedStreamer.setURL(elem.text)
				if elem.tag == 'category':
					parsedStreamer.setCategory(elem.text)
				if elem.tag == 'subcategory':
					parsedStreamer.setSubCategory(elem.text)
				if elem.tag == 'game':
					parsedStreamer.setGame(elem.text)
				if elem.tag == 'online':
					parsedStreamer.setStatus(elem.text)
				if elem.tag == 'stream':
					#Details of that streamer have been taken, so add the
					#object to the list
					self.streamers.append(parsedStreamer)
					#Empty the streamer object so we can re use it for the
					#next set of details 
					parsedStreamer = streamer.Streamer()


		sorted(self.streamers, key=lambda Streamer: Streamer.currentViewers)
		return self.streamers


	#Show the list of favourites, if there are any
	def showAll(self):
		self.win = gtk.Window()
		self.win.set_position(gtk.WIN_POS_CENTER)
		self.box1 = gtk.VBox()
			
		self.sw = gtk.ScrolledWindow()
		self.win.set_title("Favourites!")	
		self.win.set_default_size(300,300)

		#Add the scrolled window into the  VBox
		self.box1.pack_start(self.sw, True, True, 0)
		
		#Check if favourites are online or offline
		#and add the status to the XML
		self.setOnlineStatus()

		self.streams = []

		#Load the current favourites into the list
		self.streams =self.loadFavourites()
		
		#Model we use to populate the TreeView
		store = self.createModel()

		treeView = gtk.TreeView(store)
		treeView.connect("row-activated",self.onActivated)
		treeView.set_rules_hint(True)
		sel = treeView.get_selection()
		sel.set_mode(gtk.SELECTION_SINGLE)

		#Set's the function to call when an item is clicked once
		sel.set_select_function(self.setStatusBar)
		
		#Set which column to use when the user wishes to search (CTRL + F)
		treeView.set_search_column(1)

		self.sw.add(treeView)

		self.statusBar = gtk.Statusbar()
		self.box1.pack_start(self.statusBar, False, False, 0)
		self.createColumns(treeView)
		self.win.add(self.box1)

		#Make sure it spawns on top of any other windows
		self.win.grab_focus()

		self.win.show_all()
	
	#Populate the Treeview
	def createModel(self):
		store = gtk.ListStore(str,str)
		for s in self.streams:
			a = s.getName()
			b = s.getCategory()
			store.append([b,a])

		return store

	#Specify the structure of the TreeView
	def createColumns(self, treeView):
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Name", rendererText, text=1)
		column.set_sort_column_id(0)
		treeView.append_column(column)

	#Defne what to do upon receiving a double click
	def onActivated(self, widget, row, col):
		model = widget.get_model()

		#Grab the name of the streamer that was clicked
		text = model[row][1]

		for x in self.streams:
			if text in x.getName():
				self.showOptions(x)
				break
	
	#Return true if the streamer object given is currently in the favourites			
	def isFavourite(self, x):
		self.streamer = streamer.Streamer()
		self.streamer = x
		streams = []
		streams = self.loadFavourites()
		for s in streams:
			if s.getURL() == self.streamer.getURL():
				return True
		return False


	#Shows the options to remove from favourites, or view the stream
	def showOptions(self, x):
		self.window = gtk.Window()
		self.window.set_position(gtk.WIN_POS_CENTER)
		self.window.set_default_size(40,50)
		self.box2 = gtk.HBox()

		self.window.add(self.box2)
		self.s = streamer.Streamer()
		self.s = x

		#Set the title to the name of the streamer
		self.window.set_title(self.s.getName())
		
		#Add the button for each option
		self.viewButton = gtk.Button("View " + self.s.getName() + "'s stream!")
		self.removeFavouriteButton = gtk.Button("Remove "+ self.s.getName() +
 " from favourites")

		self.box2.pack_start(self.viewButton)
		self.box2.pack_start(self.removeFavouriteButton)

		self.viewButton.connect('clicked', lambda *a: self.viewStream(self.s))
		self.removeFavouriteButton.connect('clicked',
lambda *a :self.removeFavButton(self.s))
		self.window.grab_focus()
		self.window.show_all()

	#What we do when the remove button is clicked
	def removeFavButton(self, s):
		self.remove(s)
		self.box2.remove(self.viewButton)
		self.box2.remove(self.removeFavouriteButton)
		md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, 
gtk.MESSAGE_QUESTION,gtk.BUTTONS_CLOSE,s.getName() + 
" has been remove from your favourites!")
		md.run()
		md.destroy()

		#We hide the window instead of destroying it because it
		#may be used again
		self.window.hide()

	def viewStream(self, s):
		viewer = streamViewer.Main()
		viewer.view(s)

	#Method to mark which favourites are online and which are not
	def setOnlineStatus(self):
		streams = []
		streams = self.loadFavourites()
		url = ("http://api.justin.tv/api/stream/list.json?channel=")
		for x in streams:
			streamURL = x.getURL()

			#Remove the prefix so we're left with just the streamer name
			streamURL = streamURL.replace('http://www.justin.tv/','')
			streamURL = url + streamURL

			#Grab the contents of the json file
			http = urllib.urlopen(streamURL)

			contents = http.read()
			http.close()
			if contents == "[]":
				#Empty json file indicates the stream is offline
				x.setStatus("offline")
			else:	
				x.setStatus("online")

		self.writeToFav(streams)
			
	#Add the currently selected streamer's current viewers to the status bar
	def setStatusBar(self,selected):
		x = selected[0]
		self.statusBar.push(0,"Currently " + self.streams[x].getStatus())
		return True

if __name__ == '__main__':
	sys.exit()
