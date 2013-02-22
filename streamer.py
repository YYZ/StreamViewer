#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This class represents a streamer object
#It contains variables that represent various attributes
#of a streamer, as well as methods to alter and retreive these values
import sys

class Streamer():
    #When an object is created, we make default values
	def __init__(self):
		self.name = ""
		self.title = ""
		self.URL = ""
		self.currentViewers =0
		self.category=""
		self.subCategory =""
		
		#Only if the streamer is streaming a game
		self.game = ""
		
		self.status = ""

	def setName(self, s):
		t = s
		s = t.lower().strip()
		self.name = s

	def setURL(self, u):
		self.URL = u
	
	def setViewers(self, v):
		self.currentViewers = v

	def setTitle(self, i):
		self.title = i
	
	def setCategory(self, c):
		self.category = c

	def setSubCategory(self, s):
		self.subCategory = s

	def setGame(self, g):
		self.game = g

    #Indicates whether the streamer is online or offline
	def setStatus(self, s):
		self.status = s

	def getStatus(self):
		return self.status

	def getName(self):
		return self.name
	
	def getSubCategory(self):
		return self.subCategory

	def getURL(self):
		return self.URL

	def getTitle(self):
		return self.title
		
	def getCategory(self):
		return self.category

	def getGame(self):
		return self.game

	def getViewers(self):
		return self.currentViewers

if __name__ == '__main__':
	sys.exit()
