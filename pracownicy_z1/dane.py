# -*- coding: utf-8 -*-

import csv  # moduł do obsługi formatu csv
import sqlite3


def dane_z_pliku(plik):
    """
    Zwraca wiersze z pliku csv w postaci listy list
    """
    dane = []
    with open(plik, newline='') as plikcsv:
        tresc = csv.reader(plikcsv, delimiter='\t')
        for lista in tresc:
            dane.append(lista)
    return dane


def wyczysc_dane(dane, pole):
    """
    @param: dane – lista rekordów, pole – numer pola do oczyszczenia
    """
    for i, rekord in enumerate(dane):
        el = rekord[pole]
        el = el.replace('zł','')  # usuń zł
        el = el.replace(' ','')  # usun spacje
        el = el.replace(',','.')  # usun spacje
        # d[5] = float(liczba)
        dane[i][pole] = float(el)
    return dane


def wylicz_premie(dane, stawki):
    for i, l in enumerate(dane):
        p = l[5] * stawki[l[3]]
        l.insert(6, p)
        dane[i] = l
    return dane


dzial = dane_z_pliku('dział.txt')
premia = dane_z_pliku('premia.txt')
premia = wyczysc_dane(premia, 1)
pracownicy = dane_z_pliku('pracownicy.txt')
pracownicy = wyczysc_dane(pracownicy, 5)
pracownicy = wylicz_premie(pracownicy, stawki = dict(premia))

# utworzenie połączenia z bazą przechowywaną na dysku
# lub w pamięci (':memory:')
con = sqlite3.connect('pracownicy.sql')

# dostęp do kolumn przez indeksy i przez nazwy
con.row_factory = sqlite3.Row

# utworzenie obiektu kursora
cur = con.cursor()

# tworzenie tabel
cur.executescript("""
    DROP TABLE IF EXISTS dzial;
    CREATE TABLE IF NOT EXISTS dzial (
        id INTEGER PRIMARY KEY,
        nazwa varchar(20) NOT NULL,
        siedziba varchar(20) NOT NULL
    )""")

cur.executemany('INSERT INTO dzial VALUES(?,?,?)', dzial)

cur.executescript("""
    DROP TABLE IF EXISTS premia;
    CREATE TABLE IF NOT EXISTS premia (
        id varchar(20) PRIMARY KEY,
        premia NUMERIC
    )""")

cur.executemany('INSERT INTO premia VALUES(?,?)', premia)

cur.execute("DROP TABLE IF EXISTS pracownicy;")

cur.execute("""
    CREATE TABLE IF NOT EXISTS pracownicy (
        id varchar(6) PRIMARY KEY,
        nazwisko varchar(20) NOT NULL,
        imie varchar(20) NOT NULL,
        stanowisko varchar(20) NOT NULL,
        data_zatr varchar(23) NOT NULL,
        placa NUMERIC NOT NULL,
        premia NUMERIC,
        id_dzial INTEGER NOT NULL,
        FOREIGN KEY(stanowisko) REFERENCES premia(id),
        FOREIGN KEY(id_dzial) REFERENCES dzial(id)
    )""")

cur.executemany('INSERT INTO pracownicy VALUES(?,?,?,?,?,?,?,?)', pracownicy)
# wstawiamy wiele rekordów

# c)
cur.execute("""
    SELECT dzial.siedziba, sum(pracownicy.placa) as total
    FROM dzial, pracownicy
    WHERE pracownicy.id_dzial=dzial.id
    GROUP BY dzial.siedziba
    ORDER BY total ASC
    """)
wyniki = cur.fetchall()
for siedziba, total in wyniki:
    print(siedziba, total)

# d)
cur.execute("""
    SELECT dzial.id, dzial.nazwa, pracownicy.nazwisko, pracownicy.imie
    FROM dzial, pracownicy
    WHERE pracownicy.id_dzial=dzial.id
    ORDER BY dzial.nazwa ASC
    """)
wyniki = cur.fetchall()
for id, nazwa, nazwisko, imie in wyniki:
    print(id, nazwa, nazwisko, imie)

con.commit()


# print(pracownicy)
# print(premia)
