#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This class takes care of notifications of favourite streamers
#coming online. It checks every five minutes whether or not
#a streamer who was previously offline has come online

import pygtk
import pynotify
import sys,favourites,streamer,gtk

class Main():
    def __init__(self): 
        self.startFav = []
        self.fav = favourites.Favourites()

        #Sets the online tag of each favourite
        self.fav.setOnlineStatus()

        #Load all of the favourites at start time into here
        self.startFav = self.fav.loadFavourites()

        #Check if streamers come online every 5 minutes
        gtk.timeout_add(60*1000, self.myTimer) 
    
    def myTimer(self):
        self.currentFav = []
        self.cFav = favourites.Favourites()
        self.cFav.setOnlineStatus()

        #Load all of the current fav's(Every 5 mins)
        self.currentFav = self.cFav.loadFavourites()

        #Most recent favourites list
        for x in self.currentFav:
            #Previous list
            for z in self.startFav:
                #Same streamer in both
                if x.getName() == z.getName():
                    #Currently online
                    if x.getStatus() == "online":
                        #Stream has gone from offline to online
                        if z.getStatus() == "offline": 
                            if pynotify.init("Basics"):
                                #Notification of stream coming online!  
                                a = z.getName()
                                print a + " is now online!"
                                n = pynotify.Notification(a,"is now online")
                                n.show()
                            else:       
                                print "Failed to send notification"
                                sys.exit(1) 
        
        #Put the most recent list into the old one, so people
        #who have gone offline since the program started will 
        #trigger a notification if the come back online 
        self.startFav = self.currentFav
        return True



if __name__ == '__main__':
    sys.exit()
