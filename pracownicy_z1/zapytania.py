# -*- coding: utf-8 -*-

import sqlite3


# połączenie z bazą w pliku lub w pamięci (':memory:')
con = sqlite3.connect('pracownicy.sqlite3')
con.row_factory = sqlite3.Row  # dostęp do kolumn przez indeksy i przez nazwy
cur = con.cursor()  # utworzenie obiektu kursora


def pokaz_wyniki(dane):
    for row in dane:
        print(tuple(row))


def kwerenda_c():
    """
    Kwota pieniędzy potrzebna na wypłatę pensji zasadniczej w każdym mieście,
    wyniki uporządkowane rosnąco.
    """

    cur.execute("""
        SELECT dzial.siedziba, sum(pracownicy.placa) as pensje
        FROM dzial, pracownicy
        WHERE pracownicy.id_dzial=dzial.id
        GROUP BY dzial.siedziba
        ORDER BY pensje ASC
        """)

    pokaz_wyniki(cur.fetchall())
    # for siedziba, total in wyniki:
    #     print(siedziba, total)


def kwerenda_d():
    """
    Numer działu, nazwa działu, nazwisko i imię kierownika
    """

    cur.execute("""
        SELECT dzial.id, dzial.nazwa, pracownicy.nazwisko, pracownicy.imie
        FROM dzial, pracownicy
        WHERE pracownicy.id_dzial=dzial.id
        ORDER BY dzial.nazwa ASC
        """)

    pokaz_wyniki(cur.fetchall())


def kwerenda_e():
    """
    Premia dla każdego pracownika jako procent pensji zasadniczej zależny
    od stanowiska
    """

    cur.execute("""
        SELECT pracownicy.nazwisko, pracownicy.imie,
        pracownicy.placa *
        (SELECT premia.premia FROM premia
         WHERE pracownicy.stanowisko=premia.id)
        as premia
        FROM pracownicy;
        """)

    pokaz_wyniki(cur.fetchall())


def kwerenda_f():
    """
    Średnią pensja dla kobiet i dla mężczyzn
    """

    cur.execute("""
        SELECT avg(placa) FROM pracownicy WHERE pracownicy.imie LIKE('%a');
        """)
    pokaz_wyniki(cur.fetchall())

    # f) mężczyźni
    cur.execute("""
        SELECT avg(placa) FROM pracownicy WHERE pracownicy.imie NOT LIKE('%a');
        """)
    pokaz_wyniki(cur.fetchall())


def kwerenda_g():
    """
    Ile lat pracuje każdy z pracowników
    """

    cur.execute("""
        SELECT imie, nazwisko, stanowisko, CAST(
            (JulianDay() - JulianDay(data_zatr)
        ) / 365 AS Integer) as lata FROM pracownicy;
        """)
    pokaz_wyniki(cur.fetchall())

    # W Pythonie
    # from datetime import datetime
    # dzis = datetime.today()
    # wtedy = datetime.strptime('1998-09-01', %Y-%m-%d')
    # lata = dzis.year() - wtedy.year()


kwerenda_c()
kwerenda_d()
kwerenda_e()
kwerenda_f()
kwerenda_g()
