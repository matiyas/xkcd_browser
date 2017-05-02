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
        Gtk.Window.__init__(self, title="XKCD Browser", border_width=20)
        self.tytul = Gtk.Label()
        self.btn_najnowszy = Gtk.Button(label=">|", tooltip_text="Najnowszy")
        self.btn_nastepny = Gtk.Button(label=">", tooltip_text="Następny")
        self.btn_poprzedni = Gtk.Button(label="<", tooltip_text="Poprzedni")
        self.entry_nr_komiksu = Gtk.Entry()
        self.obrazek = Gtk.Image()
        self.vbox1 = Gtk.VBox(spacing=20)
        self.hbox1 = Gtk.HBox()
        self.hbox2 = Gtk.HBox()
        self.hbox3 = Gtk.HBox()

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

        self.connect("delete-event", Gtk.main_quit) 
        self.show_all()


class App:
    def __init__(self):
        self.gui = GUI()
        self.aktualny_adres = "http://xkcd.com"
        self.gui.entry_nr_komiksu.connect("activate", self.wczytaj_komiks)
        self.gui.btn_najnowszy.connect("clicked", self.wczytaj_komiks)

    def komiks_info(self, adres):
        soup = BeautifulSoup(urllib.urlopen(adres), "html.parser")
        numer = soup.find_all(rel="prev")[0]["href"]

        if numer == "#":
            numer = "1"
        else:
            numer = str(int(numer.split('/')[1]) + 1)

        return {"url": "http:" + soup.find_all(id="comic")[0].img["src"],
                "nazwa_komiksu": soup.find_all(id="ctitle")[0].text,
                "nazwa_img": soup.find_all(id="comic")[0].img["src"].split('/')[-1],
                "numer": numer}

    def nastepny(self, adres):
        soup = BeautifulSoup(urllib.urlopen(adres), "html.parser")
        numer = soup.find_all(rel="next")[0]["href"]

    def pobierz_komiks(self, adres):
        if not os.path.exists("cache"):
            os.mkdir("cache")
        
        if not os.path.exists("cache/" + self.komiks_info(adres)["nazwa_img"]):
            urllib.urlretrieve(self.komiks_info(adres)["url"], "cache/" + self.komiks_info(adres)["nazwa_img"])

    def wczytaj_komiks(self, wejscie):
        adres = "http://xkcd.com/"

        if type(wejscie) == Gtk.Entry:
            adres += wejscie.get_text()

        self.gui.tytul.set_markup("Komiks {}: ".format(self.komiks_info(adres)["numer"]) + "<b>{}</b>".format(self.komiks_info(adres)["nazwa_komiksu"]))
        self.pobierz_komiks(adres)
        self.gui.obrazek.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file("cache/" + self.komiks_info(adres)["nazwa_img"]))
        self.aktualny_adres = adres
 

def main():
    app = App()
    Gtk.main()


if __name__ == "__main__":
    main()

