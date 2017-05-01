#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from bs4 import BeautifulSoup
import urllib
import os


html = urllib.urlopen("https://xkcd.com")
soup = BeautifulSoup(html, "html.parser")
comic_url = "http:" + soup.find_all(id="comic")[0].img["src"]
if not os.path.exists("cache"):
    os.mkdir("cache")
nazwa = comic_url.split('/')[-1]
urllib.urlretrieve(comic_url, "cache/" + nazwa)


class GUI(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, default_width=600, default_height=450, title="XKCD Browser")
        tytul = Gtk.Label("Hello World!")
        numer = Gtk.Label("4321")
        btn_najnowszy = Gtk.Button(label="Pokaż najnowszy")
        btn_nastepny = Gtk.Button(label="Następny")
        btn_poprzedni = Gtk.Button(label="Poprzedni")
        nr_komiksu = Gtk.Entry()
        obrazek = Gtk.Image()
        pixs = GdkPixbuf.Pixbuf.new_from_file("cache/" + nazwa)
        vbox1 = Gtk.VBox(spacing=20)
        hbox1 = Gtk.HBox()
        hbox2 = Gtk.HBox()
        hbox3 = Gtk.HBox()


        nr_komiksu.set_size_request(10, 30)
        hbox1.set_baseline_position(1)
        obrazek.set_from_pixbuf(pixs)

        # Pakowanie
        a1 = False
        a2 = False
        vbox1.pack_start(numer, False, True, 0)
        vbox1.pack_start(tytul, False, True, 0)
        vbox1.pack_start(obrazek, False, True, 0)
        hbox1.pack_start(btn_poprzedni, a1, a2, 0)
        hbox1.pack_start(btn_nastepny, a1, a2, 0)
        hbox1.pack_start(btn_najnowszy, a1, a2, 0)
        hbox2.set_center_widget(hbox1)
        vbox1.pack_start(hbox2, False, True, 0)
        hbox3.set_center_widget(nr_komiksu)
        vbox1.pack_start(hbox3, False, True, 0)
        self.add(vbox1)

        self.connect("delete-event", Gtk.main_quit) 
        self.show_all()


def main():
    app = GUI()
    Gtk.main()


if __name__ == "__main__":
    main()
