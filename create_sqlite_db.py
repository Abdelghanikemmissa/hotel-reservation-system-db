import sqlite3

def create_sqlite_db():
    conn = sqlite3.connect("hotel.db")
    cursor = conn.cursor()

    # Création des tables
    cursor.executescript('''
    DROP TABLE IF EXISTS Evaluation;
    DROP TABLE IF EXISTS Reservation;
    DROP TABLE IF EXISTS Concerner;
    DROP TABLE IF EXISTS Chambre;
    DROP TABLE IF EXISTS Type_Chambre;
    DROP TABLE IF EXISTS Prestation;
    DROP TABLE IF EXISTS Client;
    DROP TABLE IF EXISTS Hotel;

    CREATE TABLE Hotel (
        id_Hotel INTEGER PRIMARY KEY,
        Nom TEXT,
        Ville TEXT    );

    CREATE TABLE Client (
        id_Client INTEGER PRIMARY KEY,
        Nom_Complet TEXT,
        Adresse TEXT NULL,
        Ville TEXT NULL,
        Code_postal TEXT NULL,
        Email TEXT NULL,
        num_telephone TEXT NULL
    );

    CREATE TABLE Prestation (
        id_Prestation INTEGER PRIMARY KEY,
        Description TEXT
    );

    CREATE TABLE Type_Chambre (
        id_Type INTEGER PRIMARY KEY,
        Type TEXT
    );

    CREATE TABLE Chambre (
        id_Chambre INTEGER PRIMARY KEY,
        Numéro TEXT,
        Etage INTEGER,
        fumeur BOOLEAN,
        id_Type INTEGER,
        FOREIGN KEY(id_Type) REFERENCES Type_Chambre(id_Type)
    );

    CREATE TABLE Reservation (
        id_Reservation INTEGER PRIMARY KEY AUTOINCREMENT,
        Date_arrivée TEXT,
        Date_dépat TEXT,
        id_Client INTEGER,
        FOREIGN KEY(id_Client) REFERENCES Client(id_Client)
    );

    CREATE TABLE Concerner (
        id_Reservation INTEGER,
        id_Type INTEGER,
        FOREIGN KEY(id_Reservation) REFERENCES Reservation(id_Reservation),
        FOREIGN KEY(id_Type) REFERENCES Type_Chambre(id_Type)
    );

    CREATE TABLE Evaluation (
        id_Evaluation INTEGER PRIMARY KEY,
        Note INTEGER,
        Commentaire TEXT,
        id_Client INTEGER,
        FOREIGN KEY(id_Client) REFERENCES Client(id_Client)
    );
    ''')

    # Ajout données
    cursor.execute("INSERT INTO Hotel VALUES (1, 'Hotel de Paris', 'Paris')")

    # Clients
    cursor.executemany('''INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)''', [
        (1, 'Jean Dupont', '12 Rue de Paris', 'Paris', '75001', 'jean.dupont@email.fr', '0612345678'),
        (2, 'Marie Leroy', '5 Avenue Victor Hugo', 'Lyon', '69002', 'marie.leroy@email.fr', '0623456789'),
        (3, 'Paul Moreau', '8 Boulevard Saint-Michel', 'Marseille', '13005', 'paul.moreau@email.fr', '0634567890'),
        (4, 'Lucie Martin', '27 Rue Nationale', 'Lille', '59800', 'lucie.martin@email.fr', '0645678901'),
        (5, 'Emma Giraud', '3 Rue des Fleurs', 'Nice', '06000', 'emma.giraud@email.fr', '0656789012')
    ])

    # Types de chambre
    cursor.execute("INSERT INTO Type_Chambre VALUES (1, 'Simple')")

    # Chambre
    cursor.execute("INSERT INTO Chambre VALUES (1, '101', 1, 0, 1)")

    # Réservations
    cursor.executemany('''INSERT INTO Reservation (Date_arrivée, Date_dépat, id_Client) VALUES (?, ?, ?)''', [
        ('2025-06-15', '2025-06-18', 1),
        ('2025-07-01', '2025-07-05', 2),
        ('2025-11-12', '2025-11-14', 2),
        ('2026-02-01', '2026-02-05', 2),
        ('2025-08-10', '2025-08-14', 3),
        ('2025-09-05', '2025-09-07', 4),
        ('2026-01-15', '2026-01-18', 4),
        ('2025-09-20', '2025-09-25', 5)
    ])

    # Concerner
    cursor.execute("INSERT INTO Concerner VALUES (1, 1)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_sqlite_db()
