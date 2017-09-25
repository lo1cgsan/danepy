DROP TABLE IF EXISTS dzial;
CREATE TABLE IF NOT EXISTS dzial (
    id INTEGER PRIMARY KEY,
    nazwa varchar(20) NOT NULL,
    siedziba varchar(20) NOT NULL
);

DROP TABLE IF EXISTS premia;
CREATE TABLE IF NOT EXISTS premia (
    id varchar(20) PRIMARY KEY,
    premia NUMERIC
);

DROP TABLE IF EXISTS pracownicy;
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
);