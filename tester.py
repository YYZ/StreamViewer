import urllib
import favourites, streamer

s = streamer.Streamer()
s.setName("Gannon Balls")
s.setGame("SAM")
s.setTitle("SAM")
s.setCategory("SAM")
s.setSubCategory("SAM")
s.setURL("SAM")
f = favourites.Favourites()
f.addFavourite(s)
