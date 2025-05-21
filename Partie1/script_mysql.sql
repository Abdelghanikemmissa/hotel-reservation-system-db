CREATE DATABASE IF NOT EXISTS database_project;
USE database_project;

-- Table Hotel
CREATE TABLE IF NOT EXISTS Hotel (
    id_Hotel INT AUTO_INCREMENT PRIMARY KEY,
    Ville TEXT NOT NULL,
    Pays TEXT NOT NULL,
    code_postal NUMERIC(5,0) NOT NULL
);

-- Table Type_Chambre
CREATE TABLE IF NOT EXISTS Type_Chambre (
    id_Type INT AUTO_INCREMENT PRIMARY KEY,
    Nom_Type TEXT NOT NULL,
    Tarif NUMERIC(5,0) NOT NULL
);

-- Table Chambre
CREATE TABLE IF NOT EXISTS Chambre (
    id_Chambre INT AUTO_INCREMENT PRIMARY KEY,
    Numero NUMERIC(3,0) NOT NULL,
    Etage NUMERIC(2,0) NOT NULL,
    fumeur BOOLEAN NOT NULL,
    id_Hotel INT,
    id_Type INT,
    FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel),
    FOREIGN KEY (id_Type) REFERENCES Type_Chambre(id_Type)
);

-- Table Client
CREATE TABLE IF NOT EXISTS Client (
    id_Client INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Nom_Complet TEXT NOT NULL,
    Adresse TEXT NOT NULL,
    Ville TEXT NOT NULL,
    Code_postal NUMERIC(5,0) NOT NULL,
    Email TEXT NOT NULL,
    num_telephone VARCHAR(15) NOT NULL
);

-- Table Reservation
CREATE TABLE IF NOT EXISTS Reservation (
    id_Reservation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivee DATE NOT NULL,
    Date_depart DATE NOT NULL,
    id_Client INT,
    FOREIGN KEY (id_Client) REFERENCES Client(id_Client)
);

-- Table Concerner
CREATE TABLE IF NOT EXISTS Concerner (
    id_Type INT,
    id_Reservation INT,
    FOREIGN KEY (id_Type) REFERENCES Type_Chambre(id_Type),
    FOREIGN KEY (id_Reservation) REFERENCES Reservation(id_Reservation)
);

-- Table Prestation
CREATE TABLE IF NOT EXISTS Prestation (
    id_Prestation INT AUTO_INCREMENT PRIMARY KEY,
    Prix NUMERIC(5,0) NOT NULL
);

-- Table Offre
CREATE TABLE IF NOT EXISTS Offre (
    id_Hotel INT,
    id_Prestation INT,
    FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel),
    FOREIGN KEY (id_Prestation) REFERENCES Prestation(id_Prestation)
);

-- Table Evaluation
CREATE TABLE IF NOT EXISTS Evaluation (
    id_Evaluation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivee DATE NOT NULL,
    Note_Evaluation NUMERIC(1,0) NOT NULL,
    Commentaire TEXT NOT NULL,
    id_Client INT,
    id_Hotel INT,
    FOREIGN KEY (id_Client) REFERENCES Client(id_Client),
    FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel)
);

-- Insertions
INSERT INTO Hotel (id_Hotel, Ville, Pays, code_postal) VALUES
(1, 'Paris', 'France', 75001),
(2, 'Lyon', 'France', 69002);

INSERT INTO Type_Chambre (id_Type, Nom_Type, Tarif) VALUES
(1, 'Simple', 80),
(2, 'Double', 120);

INSERT INTO Chambre (id_Chambre, Numero, Etage, fumeur, id_Hotel, id_Type) VALUES
(1, 201, 2, 0, 1, 1),
(2, 502, 5, 1, 1, 2),
(3, 305, 3, 0, 2, 1),
(4, 410, 4, 0, 2, 2),
(5, 104, 1, 1, 2, 2),
(6, 202, 2, 0, 1, 1),
(7, 307, 3, 1, 1, 2),
(8, 101, 1, 0, 1, 1);

INSERT INTO Client (id_Client, Adresse, Ville, Code_postal, Email, num_telephone, Nom_Complet) VALUES
(1, '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '00612345678', 'Jean Dupont'),
(2, '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '00623456789', 'Marie Leroy'),
(3, '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', '00634567890', 'Paul Moreau'),
(4, '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', '00645678901', 'Lucie Martin'),
(5, '3 Rue des Fleurs', 'Nice', 06000, 'emma.giraud@email.fr', '00656789012', 'Emma Giraud');

INSERT INTO Reservation (id_Reservation, Date_arrivee, Date_depart, id_Client) VALUES
(1, '2025-06-15', '2025-06-18', 1),
(2, '2025-07-01', '2025-07-05', 2),
(7, '2025-11-12', '2025-11-14', 2),
(10, '2026-02-01', '2026-02-05', 2),
(3, '2025-08-10', '2025-08-14', 3),
(4, '2025-09-05', '2025-09-07', 4),
(9, '2026-01-15', '2026-01-18', 4),
(5, '2025-09-20', '2025-09-25', 5);

INSERT INTO Evaluation (id_Evaluation, Date_arrivee, Note_Evaluation, Commentaire, id_Client, id_Hotel) VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1, 1),
(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2, 1),
(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3, 2),
(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4, 2),
(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5, 2);
