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
        self.tytul = Gtk.Label()
        self.btn_najnowszy = Gtk.Button(label=">|")
        self.btn_nastepny = Gtk.Button(label=">")
        self.btn_poprzedni = Gtk.Button(label="<")
        self.entry_nr_komiksu = Gtk.Entry()
        self.obrazek = Gtk.Image()
        self.vbox1 = Gtk.VBox(spacing=20)
        self.hbox1 = Gtk.HBox()
        self.hbox2 = Gtk.HBox()
        self.hbox3 = Gtk.HBox()

        self.btn_poprzedni.set_hint("Poprzedni")
        self.entry_nr_komiksu.set_size_request(10, 30)
        self.hbox1.set_baseline_position(1)

        # Pakowanie
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
        self.connect("delete-event", Gtk.main_quit) 
        self.show_all()


class App:
    def __init__(self):
        self.gui = GUI()
        self.xkcd_addr = "http://xkcd.com"
        self.gui.entry_nr_komiksu.connect("activate", self.wczytaj_komiks)
        self.gui.btn_najnowszy.connect("clicked", self.wczytaj_komiks)

    def komiks_info(self, adres):
        soup = BeautifulSoup(urllib.urlopen(adres), "html.parser")
        return {"url": "http:" + soup.find_all(id="comic")[0].img["src"],
                "nazwa_komiksu": soup.find_all(id="ctitle")[0].text,
                "nazwa_img": soup.find_all(id="comic")[0].img["src"].split('/')[-1]}

    def pobierz_komiks(self, adres):
        if not os.path.exists("cache"):
            os.mkdir("cache")
        
        if not os.path.exists("cache/" + self.komiks_info(adres)["nazwa_img"]):
            urllib.urlretrieve(self.komiks_info(adres)["url"], "cache/" + self.komiks_info(adres)["nazwa_img"])

    def wczytaj_komiks(self, wejscie):
        adres = "http://xkcd.com/" + wejscie.get_text()
        self.gui.tytul.set_markup("Komiks {}: ".format(wejscie.get_text()) + "<b>{}</b>".format(self.komiks_info(adres)["nazwa_komiksu"]))
        self.pobierz_komiks(adres)
        self.gui.obrazek.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file("cache/" + self.komiks_info(adres)["nazwa_img"]))
 
def main():
    app = App()
    Gtk.main()


if __name__ == "__main__":
    main()

