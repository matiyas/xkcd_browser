#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
from gi.repository import GdkPixbuf
from random import randint
from bs4 import BeautifulSoup
from math import floor
import urllib
import os


class GUI(Gtk.Window):
    """Klasa reprezentująca graficzny interfejs użytkownika."""
    def __init__(self):
        """Metoda inicjalizująca obiekt klasy GUI.
        
        Metoda tworzy okno na którym umieszczany jest tytuł, obrazek, przyciski odpowiadające za: losowanie, przejście do
        poprzedniego obrazka, przejście do następnego obrazka, oraz przejście do najnowszego obrazka, a także pole tekstowe
        służące do wpisywania numeru obrazka do którego użytkownik chce przejść.
        """
        Gtk.Window.__init__(self, title="XKCD Browser", border_width=20)
        self.tytul = Gtk.Label()
        self.label_strona = Gtk.Label("Strona: ")
        self.scrolled_window = Gtk.ScrolledWindow(min_content_height=500, min_content_width=800)
        self.btn_najnowszy = Gtk.Button(">|", tooltip_text="Najnowszy")
        self.btn_nastepny = Gtk.Button(">", tooltip_text="Następny")
        self.btn_poprzedni = Gtk.Button("<", tooltip_text="Poprzedni")
        self.btn_losuj = Gtk.Button("Losuj")
        self.btn_przejdz = Gtk.Button("Przejdź")
        self.btn_powieksz = Gtk.Button("+", tooltip_text="Powiększ")
        self.btn_pomniejsz = Gtk.Button("-", tooltip_text="Pomniejsz")
        self.entry_nr_komiksu = Gtk.Entry(max_length=4)
        self.pixs = GdkPixbuf.Pixbuf()
        self.obrazek = Gtk.Image()
        self.vbox1 = Gtk.VBox(spacing=20)
        self.hbox1 = Gtk.HBox()
        self.hbox2 = Gtk.HBox()
        self.ramka = Gtk.Frame()
        self.skala = 1.0    # Skala obrazka od 0.2 do 2.0
        self.sciezka = ""   # Ścieżka pod którą znajduje się aktualnie wczytany obrazek

        # Pakowanie widgetów
        self.scrolled_window.add(self.obrazek)
        self.ramka.add(self.scrolled_window)
        self.vbox1.pack_start(self.tytul, False, True, 0)
        self.vbox1.pack_start(self.ramka, False, True, 0)
        self.hbox1.pack_start(Gtk.Label(), True, False, 0)
        self.hbox1.pack_start(self.btn_losuj, False, False, 0)
        self.hbox1.pack_start(self.btn_poprzedni, False, False, 0)
        self.hbox1.pack_start(self.btn_nastepny, False, False, 0)
        self.hbox1.pack_start(self.btn_najnowszy, False, False, 0)
        self.hbox1.pack_start(self.btn_powieksz, False, False, 0)
        self.hbox1.pack_start(self.btn_pomniejsz, False, False, 0)
        self.hbox1.pack_start(Gtk.Label(), True, False, 0)
        self.vbox1.pack_start(self.hbox1, False, True, 0)
        self.hbox2.pack_start(Gtk.Label(), True, False, 0)
        self.hbox2.pack_start(self.label_strona, False, False, 0)
        self.hbox2.pack_start(self.entry_nr_komiksu, False, False, 0)
        self.hbox2.pack_start(self.btn_przejdz, False, False, 0)
        self.hbox2.pack_start(Gtk.Label(), True, False, 0)
        self.vbox1.pack_start(self.hbox2, False, True, 0)
        self.add(self.vbox1)

        self.btn_powieksz.connect("clicked", self.zoom, "+")
        self.btn_pomniejsz.connect("clicked", self.zoom, "-")
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def ustaw_obraz(self, obraz):
        """Metoda wczytująca wybrany obraz.
        
        Argumenty:
            obraz (str):    Ścieżka pod którą znajduje się obraz, który ma zostać wczytany.
        """
        self.skala = 1.0
        self.sciezka = obraz
        self.obrazek.set_from_pixbuf(self.pixs.new_from_file(obraz))

    def zoom(self, przycisk, rodzaj):
        """Metoda zmieniająca rozmiar wyświetlanego obrazu.
        
        Argumenty:
            przycisk (Gtk.Button):  Wciśnięty przycisk, uruchamiający metodę.
            rodzaj (str):           Rodzaj zmiany rozmiaru obrazu. "+" odpowiada za powiększenie, a "-" odpowiada za pomniejszenie obrazu.
           
        Metoda zmienia rozmiar wyświetlanego obrazu o 20% względem oryginalnego rozmiaru. Rozmiar jest ustawiany w zakresie od 40% do 200%
        względem oryginalnego rozmiaru.
        """
        # Powiększenie
        if rodzaj == "+":
            if self.skala + 0.2 >= 2.0:
                self.skala = 2.0
            else:
                self.skala += 0.2
        # Pomniejszenie
        elif rodzaj == "-":
            if self.skala - 0.2 <= 0.4:
                self.skala = 0.4
            else:
                self.skala -= 0.2

        # Ustaw w oknie obraz o nowym rozmiarze 
        self.obrazek.set_from_pixbuf(GdkPixbuf.Pixbuf.new_from_file_at_scale(
            self.sciezka, int(floor(GdkPixbuf.Pixbuf.get_file_info(self.sciezka)[1] * self.skala)), -1, True))


class App:
    def __init__(self):
        self.gui = GUI()
        self.glowna = "http://xkcd.com/"
        self.aktywna = "http://xkcd.com/"
        self.max_numer = self.komiks_info(self.glowna)["numer"]
        self.gui.btn_losuj.connect("clicked", self.wczytaj_komiks, "rand")
        self.gui.btn_najnowszy.connect("clicked", self.wczytaj_komiks, "main")
        self.gui.btn_nastepny.connect("clicked", self.wczytaj_komiks, "next")
        self.gui.btn_poprzedni.connect("clicked", self.wczytaj_komiks, "prev")
        self.gui.entry_nr_komiksu.connect("activate", self.wczytaj_komiks, "entry")
        self.wczytaj_komiks(self, "main")

    @staticmethod
    def komiks_info(adres):
        soup = BeautifulSoup(urllib.urlopen(adres), "html.parser")
        numer = soup.find_all(rel="prev")[0]["href"]

        if numer == "#":
            numer = "1"
        else:
            numer = str(int(numer.split('/')[1]) + 1)

        url = "http:" + soup.find_all(id="comic")[0].img["src"]
        return {"url": url, "nazwa_komiksu": soup.find_all(id="ctitle")[0].text, "nazwa_img": url.split('/')[-1], "numer": numer}

    def wczytaj_komiks(self, wejscie, nav):
        adres = self.glowna

        try:
            aktywny_info = self.komiks_info(self.aktywna)

            if nav == "entry":
                adres += wejscie.get_text()
            elif nav == "next":
                adres += str(int(aktywny_info["numer"]) + 1)
            elif nav == "prev":
                adres += str(int(aktywny_info["numer"]) - 1)
            elif nav == "rand":
                adres += str(randint(1, int(self.max_numer)))

            nowy_info = self.komiks_info(adres)

            self.gui.tytul.set_markup(u"<b>{}</b>".format(nowy_info["nazwa_komiksu"]))
            self.gui.entry_nr_komiksu.set_text(nowy_info["numer"])

            if not os.path.exists("cache"):
                os.mkdir("cache")
            if not os.path.exists("cache/" + nowy_info["nazwa_img"]):
                urllib.urlretrieve(nowy_info["url"], "cache/" + nowy_info["nazwa_img"])

            self.gui.ustaw_obraz("cache/" + nowy_info["nazwa_img"])
            self.aktywna = adres

        except IndexError:
            self.gui.tytul.set_markup('<span foreground="red"><b>Wystąpił błąd podczas wczytywania komiksu!</b></span>')


if __name__ == "__main__":
    app = App()
    Gtk.main()
