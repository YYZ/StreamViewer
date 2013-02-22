#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This class presents the UI for viewing search results.
#Allows the user to view a stream or to add the user to their favourites

import gtk,webkit,streamViewer,sys,searchBox,search,onlineStreams,streamer
import searchResults,favourites
from urllib import urlretrieve

class Main():
	URL = ""
	def __init__(self):
		self.offset = 0
		self.win = gtk.Window()
		self.win.set_position(gtk.WIN_POS_CENTER)
		self.win.set_default_size(40,50)
		self.box1 = gtk.VBox()

    #used when a user searches for just a single streamer 
	def singleStreamer(self, st):
		self.box1=gtk.HBox()
		self.win.add(self.box1)
		self.s = streamer.Streamer()
		self.s = st
		self.win.set_title(self.s.getName())

		self.viewButton = gtk.Button("View " + self.s.getName() + "'s stream!")
		self.favouriteButton = gtk.Button("Add "+ self.s.getName()
+ " to favourites")
		self.removeFavouriteButton = gtk.Button("Remove "+ self.s.getName() 
+ " from favourites")

		self.box1.pack_start(self.viewButton)
		fav = favourites.Favourites()
		
		#If the user is in favourites, then we give the option to remove
		#them, if not we give the option to add them
		if fav.isFavourite(self.s):
			self.box1.pack_start(self.removeFavouriteButton)
		else:
			self.box1.pack_start(self.favouriteButton)


        #Set onClick for the buttons
		self.viewButton.connect('clicked', lambda *a: self.viewStream(self.s))
		self.favouriteButton.connect('clicked', 
lambda *a :self.addFavourite(self.s))
		self.removeFavouriteButton.connect('clicked', 
lambda *a :self.removeFavourite(self.s))
		
		self.win.show_all()

    #Used to display more than one streamer(ie.favourites/currently 
    #online in a category/subcategory)
	def multipleStreamers(self, st, off):
		self.offset = off

		self.win = gtk.Window()
		self.win.set_position(gtk.WIN_POS_CENTER)
		self.box1 = gtk.VBox()
			
		self.sw = gtk.ScrolledWindow()
		self.win.set_title("Online Streamers")	
		self.win.set_default_size(300,300)
		self.box1.pack_start(self.sw, True, True, 0)
		
		self.streams = []
		self.streams =st
		#If the search result was empty, we inform the user and exit
		if len(st) == 0:
			md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, 
gtk.MESSAGE_QUESTION,gtk.BUTTONS_CLOSE," No streams online")
			md.run()
			md.destroy()
			return
			
        #Create the model that will populate the TreeView
		store = self.createModel()
		
		#Populate the TreeView
		treeView = gtk.TreeView(store)
		
		treeView.connect("row-activated",self.onActivated)
		treeView.set_rules_hint(True)
		sel = treeView.get_selection()
		sel.set_mode(gtk.SELECTION_SINGLE)
		
		#Set method for a single click on a streamer
		sel.set_select_function(self.selectCategory)
		
		#Tell the TreeView which column to use for searching (CTRL-F)
		treeView.set_search_column(1)
		
		self.sw.add(treeView)

		self.createColumns(treeView)

		self.statusBar = gtk.Statusbar()
		self.box1.pack_start(self.statusBar, False, False, 0)
		self.win.add(self.box1)
			
		self.win.show_all()
		self.win.grab_focus()

	def createModel(self):
	    #Sort the search results by current viewers
		sorted(self.streams, key=lambda Streamer: Streamer.currentViewers)
		
		store = gtk.ListStore(str,str)
		
		#Populate the TreeView
		for s in self.streams:
			a = s.getName()
			b = s.getCategory()
			store.append([b,a])

        #If there were more than 50 streams returned, then we give the option
        #To view the next 50 (or however many)
		if len(self.streams) == 50:
			store.append([b,"Next 50 streams"])
			
	    #If we're already past the first 50 streams, we give the option to 
	    #return to the previous set of results
		if self.offset >= 50:
			store.append([b, "Previous 50 streams"])
			
		return store

    #Create the column to populate
	def createColumns(self, treeView):
		rendererText = gtk.CellRendererText()
		column = gtk.TreeViewColumn("Name", rendererText, text=1)
		column.set_sort_column_id(0)
		treeView.append_column(column)

    #Define what to do when a streamer is double clicked
	def onActivated(self, widget, row, col):
		model = widget.get_model()
		text = model[row][1]
		if text == "Next 50 streams":
			self.reDraw(self.streams[0], True)
		else:
			if text == "Previous 50 streams":
				self.reDraw(self.streams[0], False)
			else:
				for x in self.streams:
					if text in x.getName():
						view = searchResults.Main()
						view.singleStreamer(x)
						break

    #Define what happens upon receiving a single click
	def selectCategory(self, selection):
		x = selection[0]
		try:
			self.statusBar.push(0,self.streams[x].getViewers() + " viewers")
		except:
			pass
		return True

    #View the selected stream
	def viewStream(self, r):
		s = streamer.Streamer()
		s = r
		viewer = streamViewer.Main()
		viewer.view(s)

    #Show either the next 50 results or the previous 50 results
	def reDraw(self, s, isNext):
		self.search=search.Main()
		if isNext == True:
			self.offset = self.offset + 50
		else:
			self.offset = self.offset -50
	
		st = streamer.Streamer()
		st = s
		res = []
        
        #We have to search again to find the streams to display
		if st.getCategory() == "gaming":
			res = self.search.findOnlineStreams("gaming", "", True,
st.getGame(), self.offset)
		else:
			res = self.search.findOnlineStreams(st.getCategory(), 
st.getSubCategory(), False, "", self.offset)
		
		#Sort the streams
		sorted(res, key=lambda Streamer: Streamer.currentViewers)
		
		newWin = searchResults.Main()
		newWin.multipleStreamers(res, self.offset)	
		
		#get rid of this window so we can show the new one with next 50 results
		self.win.destroy()


	def addFavourite(self, f):
		fav = favourites.Favourites()
		fav.addFavourite(f)
		s = searchResults.Main()
		s.singleStreamer(f)	
		self.win.destroy()
		

	def removeFavourite(self, f):
		fav = favourites.Favourites()
		fav.remove(f)
		s = searchResults.Main()
		s.singleStreamer(f)
		self.win.destroy()
		
if __name__ == '__main__':	
	sys.exit(0)		
