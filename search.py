#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This class performs all searches.
#Used to find specific streamers, and to find people streaming a 
#certain category or sub-category

import gtk,webkit,sys,streamer,urllib,streamViewer
from lxml import etree
from StringIO import StringIO

class Main(object):
	notFound =True
	def findStreamer(self,q):
	    #User inputed query
		self.query = q 
		self.query = self.query.lower().strip()
		self.query = self.query.replace(' ', '')

		#Before making a request for the XML, we send a request for a channel
		#id using the name given by the user. If the user gives the right name
		#then we find the stream without parsing the XML, speeding things up.

		self.firstTry = ("http://api.justin.tv/api/stream/list.xml?channel=")
		self.firstTry = self.firstTry + self.query
		
		self.ur = etree.parse(self.firstTry)#Get trees ready for searching
		self.x = etree.tostring(self.ur)

		self.temp = open("temp.xml", "wb")
		self.temp.write(self.x)
		self.temp.close()
		self.temp = open("temp.xml")
		self.url = self.temp.read()
		self.temp.close()
		self.context = etree.iterparse(StringIO(self.url))

		self.s = streamer.Streamer()

		for action, elem in self.context:
			if not elem.text:
				pass
			else:
				if elem.tag == "channel_count":
					self.s.setViewers(elem.text)
				if elem.tag == "login":
					t = elem.text
					t = t.lower().strip()
					t = t.replace('_', '')
					t = t.replace('-', '')
					t = t.replace('/', '')
					t= t.replace(' ', '')
					self.s.setName(t)
				if elem.tag == "title":
					self.s.setTitle(elem.text)
				if elem.tag == "channel_url":
					self.s.setURL(elem.text)	
				if elem.tag == "stream":
					if self.s.name == self.query:
						Main.notFound = False
						return self.s
		
		#If we get to here, then the user didn't type in an exact name,
		#so we have to search the XML for a match.
		#Now we call the doSearch function to try and find the streamers URL,
		#who is hopefully near the beginning of the XML
		
		self.offset = 0
		self.streamDetails = streamer.Streamer()
		self.streamDetails = self.doSearch(self.query,self.offset)

        #Found on the first go!
		if self.streamDetails != None:
			Main.notFound = False
			return self.streamDetails
		else:
		    #While we still haven't found the correct streamer
			while Main.notFound == True:
				self.offset = int(self.offset) + 100
				
				#For the sake of performance, we only search the first 
                #1000 streamers. 
				if not self.offset == 1000:
					self.streamDetails = self.doSearch(self.query, self.offset)
				else:
					return self.streamDetails

        #Set this to true again. This ensure that if the user wants to search
        #again, the seacher will function correctly
		Main.notFound = True
		return self.streamDetails	


	#Searches for a specific user, from a specified offset	
	def doSearch(self,query,offset):
		self.query = query
		
		#Sanities the query
        #Remove odd characters and spaces
		self.query= self.query.replace('_', '')
		self.query= self.query.replace('-', '')
		self.query= self.query.replace('/', '')
		self.query= self.query.replace(' ', '')

		self.offset = str(offset)
		self.URL = ("http://api.justin.tv/api/stream/list.xml?limit=50&offset=")
		 
		#Streamer object to store details
		self.s = streamer.Streamer()

        #We need to make a seperate holder so we can edit the url if
        #we don'find the streamer on the first go.
		self.url = self.URL
		self.url = self.url + self.offset

        #Get trees ready for searching
		self.ur = etree.parse(self.url)
		self.x = etree.tostring(self.ur)

        #Open temp file for writing XML
		self.temp = open("test.xml", "wb") 
		self.temp.write(self.x)
		self.temp.close()
		   
		#Open for reading
		self.temp = open("test.xml") 
		self.url = self.temp.read()
		self.temp.close()
		 
		#Parse file containg XML to etree object
		self.context = etree.iterparse(StringIO(self.url))

        #Go through the XML object
		for action, elem in self.context:
		    #Nothing in the object, so either end of file or empty file
			if not elem.text:
				pass
			else:
				if elem.tag == "channel_count":
					self.s.setViewers(elem.text)
				if elem.tag == "login":
					t = elem.text
					t = t.lower().strip()
					
					#Remove any random characters from the Streamer name
					t = t.replace('_', '')
					t = t.replace('-', '')
					t = t.replace('/', '')
					t= t.replace(' ', '')
					
					self.s.setName(t)
				if elem.tag == "title":
					self.s.setTitle(elem.text)
				if elem.tag == "channel_url":
					self.s.setURL(elem.text)
				if elem.tag == "stream":
				    #If the name is an exact match 
                    #(ie. query = TSLPolt, name = TSLPolt)
					if self.s.name == self.query:
						Main.notFound = False
						return self.s
					else:
					    #Not an exact match, but query is in name
                        #(ie, query = polt, name = TSLPolt)
						if self.query in self.s.name:
							Main.notFound = False
							return self.s
						else:
							self.s=streamer.Streamer()
			

	def findOnlineStreams(self, c, s, isGaming, g, off):
		self.URL = ("http://api.justin.tv/api/stream/list.xml?limit=50")
		
		#Gaming category does not have subcategories, 
        #instead it has 'meta_game' tags.
		self.offset = off
		
		self.URL = self.URL + "&offset="+ str(self.offset)

		if not isGaming:
		    #What category is the streamer?
			self.category = c
			self.category = self.category.lower().strip()

			self.category = self.category.replace(' ', '_')	

            #What sub-category is the streamer?
			self.subCategory = s
			self.subCategory = self.subCategory.lower().strip()
			 
			#Sub categories with 2 words need to be appended with '_'
			self.subCategory = self.subCategory.replace(' ', '_')

            #Append the category and sub-category to the URL
			t = self.category.__len__()
			x = self.subCategory.__len__()
			if t != 0:
				self.URL = self.URL + "&category=" + self.category
				if x != 0:
					self.URL = self.URL + "&subcategory=" + self.subCategory

        #If we're looking for a game, things are done slightly differently
		if isGaming:
			self.game = g
			self.game = self.game.replace(' ', '%20')
			self.URL = self.URL + ("&meta_game=" + self.game)
			
	
	
	    #Streamer object to store details
		self.s = streamer.Streamer()
		
		#List to store streamers
		self.streamers = []

        #URL we're going to query for XML
		self.url = self.URL

        #Get trees ready for searching
		self.ur = etree.parse(self.url)
		self.x = etree.tostring(self.ur)

        #Open temp file for writing XML
		self.temp = open("test.xml", "wb")
		self.temp.write(self.x)
		self.temp.close()
		        
		#Open for reading
		self.temp = open("test.xml")
		self.url = self.temp.read()
		self.temp.close()
		   
		#Parse file containg XML to etree object
		self.context = etree.iterparse(StringIO(self.url))

        #Go through the object
		for action, elem in self.context:
			if not elem.text:
				text = "none"
			else:
				if elem.tag == "subcategory":
					self.s.setSubCategory(elem.text)
				if elem.tag == "category":
					self.s.setCategory(elem.text)
				if elem.tag == "meta_game":
					self.s.setGame(elem.text)
				if elem.tag == "channel_count":
					self.s.setViewers(elem.text)
				if elem.tag == "login":
					t = elem.text
					t = t.lower().strip()
					self.s.setName(t)
				if elem.tag == "title":
					self.s.setTitle(elem.text)
				if elem.tag == "channel_url":
					self.s.setURL(elem.text)
				if elem.tag == "stream":
					self.streamers.append(self.s)
					self.s=streamer.Streamer()


        #Return the list of streamers, possibly empty, 
        #limit of 50 per search
		return self.streamers
		
if __name__ == '__main__':	
	sys.exit()
