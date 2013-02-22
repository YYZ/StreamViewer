#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This class presents the options for category and sub-category to be searched
#Uses two combo boxed for displaying and getting the users choice
#Once the Go button is clicked, this window closes and the results window
#is shown

import gtk,sys,searchBox,streamer,search,searchResults

class streamTypeChoice():
	def __init__(self):
	    #Setup the window layout and size
		self.win = gtk.Window()
		self.win.set_size_request(230, 150)
		self.win.set_position(gtk.WIN_POS_CENTER)
		self.win.set_title("Online Streams")
		self.b1 = gtk.VBox()
		self.b2 = gtk.HBox()
		self.win.add(self.b1)

		#Create the category combo boxes
		self.category = gtk.combo_box_new_text()
		self.subCategory = gtk.combo_box_new_text()
		self.gaming= gtk.combo_box_new_text()
		self.social = gtk.combo_box_new_text()
		self.entertainment = gtk.combo_box_new_text()
		self.sports = gtk.combo_box_new_text()
		self.news = gtk.combo_box_new_text()
		self.animals = gtk.combo_box_new_text()
		self.science = gtk.combo_box_new_text()
		self.education = gtk.combo_box_new_text()
		self.other = gtk.combo_box_new_text()


		self.button1 = gtk.Button("Go!")
		self.button1.connect('clicked',self.clicked)
	
		#Add the main categories
		self.category.append_text("Category")
		self.category.append_text("Gaming")
		self.category.append_text("Social")
		self.category.append_text("Entertainment")
		self.category.append_text("Sports")
		self.category.append_text("News")
		self.category.append_text("Animals")
		self.category.append_text("Science Tech")
		self.category.append_text("Other")

		#Specific Sub-Categories (None for gaming) 
		#Unfortunately very long and repetitive, but necessary.

		#Social
		self.social.append_text("Lifecasting")
		self.social.append_text("New Broadcaster")

		#Entertainment
		self.entertainment.append_text("Arts")
		self.entertainment.append_text("Celebrities")	
		self.entertainment.append_text("Comedy")
		self.entertainment.append_text("Documentary")
		self.entertainment.append_text("Entertainment News")
		self.entertainment.append_text("Fashion")
		self.entertainment.append_text("Game Shows")
		self.entertainment.append_text("Movies")
		self.entertainment.append_text("Music")
		self.entertainment.append_text("Radio Stations")
		self.entertainment.append_text("Sci-Fi")
		self.entertainment.append_text("Series")
		self.entertainment.append_text("Other Entertainment")

		#Sports

		self.sports.append_text("Auto Racing")
		self.sports.append_text("Baseball")
		self.sports.append_text("Basketball")
		self.sports.append_text("Boxing")
		self.sports.append_text("Cricket")
		self.sports.append_text("Hockey")
		self.sports.append_text("Martial Arts")
		self.sports.append_text("Sports News")
		self.sports.append_text("Rugby")
		self.sports.append_text("Soccer")
		self.sports.append_text("Softball")
		self.sports.append_text("Swimming")
		self.sports.append_text("Tennis")
		self.sports.append_text("Volleyball")
		self.sports.append_text("Wrestling")

		#News
		self.news.append_text("Festivals")
		self.news.append_text("Government Politics")
		self.news.append_text("International News")
		self.news.append_text("Local News")
		self.news.append_text("National News")
		self.news.append_text("Other News")
		self.news.append_text("Weather")

		#Animals
		self.animals.append_text("Birds")
		self.animals.append_text("Cats")
		self.animals.append_text("Dogs")
		self.animals.append_text("Exotic Wild Animals")
		self.animals.append_text("Farm Animals")
		self.animals.append_text("Fish")
		self.animals.append_text("Lizards & Amphibians")
		self.animals.append_text("Other Animals")
		self.animals.append_text("Rodents")

		#Science
		self.science.append_text("Enviornment")
		self.science.append_text("Science")
		self.science.append_text("Technology")

		#Other
		self.other.append_text("Auto")
		self.other.append_text("Business")
		self.other.append_text("Food")
		self.other.append_text("Misc")
		self.other.append_text("Real Estate")
		self.other.append_text("Travel")

		#Gaming (technically no sub categories, but we add some popular games
        #to ease searching)
		self.gaming.append_text("StarCraft II: Wings of Liberty")
		self.gaming.append_text("League of Legends")
		self.gaming.append_text("Call of Duty: Modern Warfare 3")
		self.gaming.append_text("Battlefield 3")
		self.gaming.append_text("Mass Effect 3")
		self.gaming.append_text("World of Warcraft: Cataclysm")
		self.gaming.append_text("Minecraft")
		self.gaming.append_text("Diablo III")

		self.b1.pack_start(self.category)
		self.b2.pack_start(self.subCategory)
		self.b1.pack_start(self.b2)
		self.b1.pack_start(self.button1)
		
		self.subCategory.append_text("Sub-Categories")
		self.subCategory.set_active(0)
		self.social.set_active(0)

		self.category.set_active(0)
		self.category.connect('changed', self.setSub)
		
		self.win.show_all()

    #Called when the user changes their choice of main category, this
    #changes the corresponding sub-category to match
	def reDraw(self, t):
		self.c = gtk.combo_box_new_text()
		
		#Clear the current choice
		self.b2.remove(self.subCategory)
		self.b1.remove(self.b2)
		self.b1.remove(self.button1)
		
		#Change the sub-category
		self.subCategory = t

        #Re-populate the window
		self.b2.pack_start(self.subCategory)
		self.b1.pack_start(self.b2)
		self.b1.pack_start(self.button1)
		self.subCategory.set_active(0)
		self.win.show_all()

    #Called when go is clicked
	def clicked(self, object):
	
	    #Create search object
		searcher=search.Main()
		res = []

        #Perform search using current values for category and sub-category
		if self.category.get_active_text() == "Gaming":
			res = searcher.findOnlineStreams(self.category.get_active_text() 
,'', True,self.subCategory.get_active_text(),0)
		else:
			res = searcher.findOnlineStreams(self.category.get_active_text(),
self.subCategory.get_active_text(), False,"", 0)

        #Sort the results
		sorted(res, key=lambda Streamer: Streamer.currentViewers)
		
		results = searchResults.Main()
		#Display the results
		results.multipleStreamers(res, 0)
		
		#Remove the current window
		self.win.destroy()
			

    #Set's the sub-category according to the current main category
	def setSub(self, object):
		mainCat = self.category.get_active_text()
		if "Social" in mainCat:
			self.reDraw(self.social)
		if "Gaming" in mainCat:
			self.reDraw(self.gaming)
		if "Entertainment" in mainCat:
			self.reDraw(self.entertainment)
		if "Sports" in mainCat:
			self.reDraw(self.sports)
		if "News" in mainCat:
			self.reDraw(self.news)
		if "Animals" in mainCat:
			self.reDraw(self.animals)
		if "Science" in mainCat:
			self.reDraw(self.science)
		if "Education" in mainCat:
			self.reDraw(self.education)
		if "Other" in mainCat:
			self.reDraw(self.other)
							
if __name__ == '__main__':
	sys.exit(1)
