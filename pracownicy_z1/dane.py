# -*- coding: utf-8 -*-

import csv  # moduł do obsługi formatu csv
import sqlite3


def dane_z_pliku(plik):
    """
    Zwraca wiersze z pliku csv w postaci listy list (rekordów)
    """
    dane = []
    with open(plik, newline='') as plikcsv:
        tresc = csv.reader(plikcsv, delimiter='\t')
        for lista in tresc:
            dane.append(lista)
    return dane


def wyczysc_dane(dane, pole):
    """
    Przygotowanie wartości finansowych do zapisania w bazie
    @param: dane – lista rekordów, pole – numer pola do oczyszczenia
    """
    for i, rekord in enumerate(dane):
        el = rekord[pole]
        el = el.replace('zł', '')  # usuń zł
        el = el.replace(' ', '')  # usun spacje
        el = el.replace(',', '.')  # zamien przecinki na kropki
        dane[i][pole] = el
    return dane


def wstaw_premie(dane, stawki=None):
    """
    Wstawia wartość dla pola premia w tabeli pracownicy
    @params: dane – lista rekordów, stawki – tabela premia
    """
    premia = ""
    for i, row in enumerate(dane):
        if stawki:
            premia = float(row[5]) * float(stawki[row[3]])
        row.insert(6, premia)
        dane[i] = row
    return dane


dzial = dane_z_pliku('dział.txt')
premia = dane_z_pliku('premia.txt')
premia = wyczysc_dane(premia, 1)
pracownicy = dane_z_pliku('pracownicy.txt')
pracownicy = wyczysc_dane(pracownicy, 5)
# pracownicy = wstaw_premie(pracownicy, stawki=dict(premia))
pracownicy = wstaw_premie(pracownicy)


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
