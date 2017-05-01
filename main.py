import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import urllib
from bs4 import BeautifulSoup

html = urllib.urlopen("https://xkcd.com")
soup = BeautifulSoup(html, "html.parser")
comic_url = "http:" + soup.find_all(id="comic")[0].img['src']
urllib.urlretrieve(comic_url, "cache/asdfgh.jpg")

class Okno(Gtk.Window):
    def __init__(self):
        pass