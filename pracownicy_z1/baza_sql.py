# -*- coding: utf-8 -*-

import sqlite3
from dane import *

# połączenie z bazą w pliku lub w pamięci (':memory:')
con = sqlite3.connect('pracownicy.sqlite3')
cur = con.cursor()  # utworzenie obiektu kursora

# utworzenie tabel w bazie
with open('pracownicy.sql', 'r') as plik:
    skrypt = plik.read()
    cur.executescript(skrypt)

# wstawiamy dane
cur.executemany('INSERT INTO dzial VALUES(?,?,?)', dzial)
cur.executemany('INSERT INTO premia VALUES(?,?)', premia)
cur.executemany('INSERT INTO pracownicy VALUES(?,?,?,?,?,?,?,?)', pracownicy)
con.commit()
