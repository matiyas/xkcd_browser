#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from bs4 import BeautifulSoup
import urllib
import os


class GUI(Gtk.Window):
    def __init__(self):
        # Gtk.Window.__init__(self, default_width=600, default_height=450, title="XKCD Browser")
        Gtk.Window.__init__(self, title="XKCD Browser")
        self.tytul = Gtk.Label("Hello World!")
        self.numer = Gtk.Label("4321")
        self.btn_najnowszy = Gtk.Button(label="Pokaż najnowszy")
        self.btn_nastepny = Gtk.Button(label="Następny")
        self.btn_poprzedni = Gtk.Button(label="Poprzedni")
        self.entry_nr_komiksu = Gtk.Entry()
        self.obrazek = Gtk.Image()
        self.vbox1 = Gtk.VBox(spacing=20)
        self.hbox1 = Gtk.HBox()
        self.hbox2 = Gtk.HBox()
        self.hbox3 = Gtk.HBox()

        self.entry_nr_komiksu.set_size_request(10, 30)
        self.hbox1.set_baseline_position(1)

        # Pakowanie
        self.vbox1.pack_start(self.numer, False, True, 0)
        self.vbox1.pack_start(self.tytul, False, True, 0)
        self.vbox1.pack_start(self.obrazek, False, True, 0)
        self.hbox1.pack_start(self.btn_poprzedni, False, False, 0)
        self.hbox1.pack_start(self.btn_nastepny, False, False, 0)
        self.hbox1.pack_start(self.btn_najnowszy, False, False, 0)
        self.hbox2.set_center_widget(self.hbox1)
        self.vbox1.pack_start(self.hbox2, False, True, 0)
        self.hbox3.set_center_widget(self.entry_nr_komiksu)
        self.vbox1.pack_start(self.hbox3, False, True, 0)
        self.add(self.vbox1)

        self.set_border_width(20)
        self.entry_nr_komiksu.connect('activate', self.ustaw_obrazek)
        self.connect("delete-event", Gtk.main_quit) 
        self.show_all()

    def ustaw_obrazek(self, obrazek):
        self.obrazek.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file(obrazek))


class App:
    def __init__(self):
        self.gui = GUI()
        self.pobierz_komiks("http://xkcd.com")
        self.gui.ustaw_obrazek("cache/" + self.komiks_info("http://xkcd.com")["nazwa_img"])
        self.gui.entry_nr_komiksu.connect("activate", self.wczytaj_komiks)

    def komiks_info(self, addr):
        return {"url": "http:" + BeautifulSoup(urllib.urlopen(addr), "html.parser").find_all(id="comic")[0].img["src"],
                "nazwa_komiksu": BeautifulSoup(urllib.urlopen(addr), "html.parser").find_all(id="ctitle")[0].text,
                "nazwa_img": self.url_komiksu(addr).split('/')[-1]}

    def wczytaj_komiks(self, entry):
        addr = "http://xkcd.com/" + entry.get_text()
        self.pobierz_komiks(addr)
        self.gui.ustaw_obrazek("cache/" + self.komiks_info(addr)["nazwa_img"])
        print self.komiks_info(addr)["nazwa_komiksu"]

    
def main():
    app = App()
    Gtk.main()


if __name__ == "__main__":
    main()
