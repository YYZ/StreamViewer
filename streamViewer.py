#!/usr/bin/env python
# -*- coding: utf-8 -*-
#This class is used to view streams. Any class can create an object of type streamViewer.Main(URL-TO-VIEW), 
#and have URL-TO-VIEW appear on screen in it's own window.

import gtk,webkit,streamer,urllib

class Main():

    def __init__(self):
        #Setup the viewer window
        self.stream = gtk.Window()
        self.stream.set_default_size(500,400) 
        self.streamBox = gtk.VBox()
        self.scroller = gtk.ScrolledWindow()
        self.streamBox.pack_start(self.scroller, True, True, True)
        self.t =0

    def isOnline(self, url):
        self.jsonURL = ("http://api.justin.tv/api/stream/list.json?channel=")
        self.userURL = url
        
        self.userURL = self.userURL.replace('http://www.justin.tv/','')
        self.userURL = self.userURL.replace('http://www.twitch.tv/','')
        self.userURL = self.userURL.replace('htttp://justin.tv/','')
        self.userURL = self.userURL.replace('http://twitch.tv/','')
        self.userURL = self.userURL.replace('/popout','')
        self.jsonURL = self.jsonURL + self.userURL
        
        #Grab the contents of the json file
        http = urllib.urlopen(self.jsonURL)
        contents = http.read()
        http.close()
        if contents == '[]':
            return False
        else:
            return True
    
    #View the stream
    def view(self, s):  
        add= streamer.Streamer()
        add = s

        self.URL = add.getURL()
        self.cat = add.getCategory()
        self.stream.add(self.streamBox)

        self.streamData = webkit.WebView()
        self.scroller.add(self.streamData)
        if self.sanitiseURL():
            self.stream.set_title(add.getTitle())
            self.streamData.open(self.URL)
            self.stream.show_all()
        else:
            print ("Must be twitch.tv/justin.tv link")
            return

    def sanitiseURL(self):
        if "twitch" in self.URL:
            if self.URL.endswith("/popout"):
                return True
            else:
                self.URL = self.URL + ("/popout")
                return True
        else:
            if "justin.tv" in self.URL:
                if "gaming" in self.cat:
                    self.URL = self.URL.replace('justin.tv', 'twitch.tv')
                    self.URL = self.URL + ("/popout")
                    return True 
                self.URL = self.URL + ("/popout")
                return True
            return False

    def viewByUrl(self, url):
        self.twitchUrl = url
        self.stream.add(self.streamBox)
        self.stream.set_title("Dual Craft")
        self.streamData = webkit.WebView()
        self.scroller.add(self.streamData)
        if "twitch" in self.twitchUrl:
            if self.twitchUrl.endswith("/popout"):
                pass
            else:
                self.twitchUrl = self.twitchUrl + ("/popout")
        else:
            if "justin.tv" in self.twitchUrl:
                    self.twitchUrl = self.twitchUrl.replace('justin.tv', 'twitch.tv')
                    if self.twitchUrl.endswith('/popout'):
                        pass
                    else:
                        self.twitchUrl = self.twitchUrl + ("/popout")
            else:
                md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, 
gtk.MESSAGE_QUESTION,gtk.BUTTONS_CLOSE,"Not a valid URL!")
                md.run()
                md.destroy()
                return

        if self.isOnline(self.twitchUrl):
            self.streamData.open(self.twitchUrl)
            self.stream.show_all()  
        else:
            md = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, 
gtk.MESSAGE_QUESTION,gtk.BUTTONS_CLOSE,"Streamer is not online!")
            md.run()
            md.destroy()
            return

if __name__ == '__main__':
    s = Main()  
