# -*- coding: utf-8 -*-

import os
from peewee import *

baza_plik = "pracownicy.sqlite3"
#if os.path.exists(baza_plik):
#    os.remove(baza_plik)
# tworzymy instancję bazy używanej przez modele
baza = SqliteDatabase(baza_plik)  # ':memory:'

class BazaModel(Model):  # klasa bazowa
    class Meta:
        database = baza


class Dzial(BazaModel):
    id = IntegerField(primary_key=True)
    nazwa = CharField(null=False)
    siedziba = CharField(null=False)


class Premia(BazaModel):
    id = CharField(primary_key=True)
    premia = DecimalField()


class Pracownik(BazaModel):
    id = CharField(primary_key=True)
    nazwisko = CharField(null=False)
    imie = CharField(null=False)
    stanowisko = ForeignKeyField(Premia, related_name='pracownicy')
    data_zatr = DateField(formats='%Y-%m-%d', null=False)
    placa = DecimalField(decimal_places=2)
    premia = DecimalField(decimal_places=2, default=0)
    id_dzial = ForeignKeyField(Dzial, related_name='pracownicy')

baza.connect()  # nawiązujemy połączenie z bazą

def kw_c():
    query = (Dzial
             .select(Dzial.siedziba, fn.Sum(Pracownik.placa).alias('place'))
             .join(Pracownik)
             .group_by(Dzial.siedziba)
             .order_by('place').asc())

    for obj in query:
        print(obj.siedziba, obj.place)


def kw_d():
    query = (Pracownik
             .select(Dzial.id, Dzial.nazwa, Pracownik.nazwisko, Pracownik.imie)
             .join(Dzial)
             .order_by(Dzial.nazwa).asc())

    for obj in query:
        print(obj.id_dzial.id, obj.id_dzial.nazwa, obj.nazwisko, obj.imie)


def kw_e():
    query = (Pracownik
             .select()
             .join(Premia))

    for obj in query:
        print(obj.nazwisko, obj.stanowisko.id, obj.placa * obj.stanowisko.premia)


def kw_f():
    query = (Pracownik
             .select(fn.Avg(Pracownik.placa).alias('srednia'))
             .group_by(Pracownik.imie.endswith('a')))
    for obj in query:
        print(obj.srednia)
    # zob.: https://stackoverflow.com/questions/20589462/string-matching-in-peewee-sql


def kw_g():
    from datetime import datetime
    query = (Pracownik
    .select(Pracownik.imie, Pracownik.stanowisko,
        (Pracownik.data_zatr.year).alias('rok')))

    for obj in query:
        print(obj.imie,
              obj.nazwisko,
              obj.stanowisko.id,
              datetime.now().year - int(obj.rok))


def kw_h():
    """Kwerenda wybiera imię, nazwisko, stanowisko, siedzibę pracownika"""
    query = (Pracownik
            .select()
            .join(Premia))

    for obj in query:
        print(obj.imie, obj.nazwisko, obj.stanowisko.id, obj.id_dzial.siedziba)


def kw_i():
    """Kwerenda liczy liczbę pracowników zatrudnionych w każdym dziale"""
    query = (Pracownik
            .select(Pracownik.id_dzial, fn.count(Pracownik.id).alias('ilu'))
            .join(Dzial)
            .group_by(Dzial.siedziba))

    for obj in query:
        print(obj.id_dzial.siedziba, obj.ilu)
