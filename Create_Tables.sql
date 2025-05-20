CREATE DATABASE IF NOT EXISTS database_project;
USE database_project;

-- Create the 'Hotel' table
CREATE TABLE IF NOT EXISTS Hotel (
    id_Hotel INT AUTO_INCREMENT PRIMARY KEY,
    Ville text NOT NULL,
    Pays text NOT NULL,
    code_postal Numeric(5,0) NOT NULL
);

-- Create the 'Type_Chambre' table
CREATE TABLE IF NOT EXISTS Type_Chambre (
    id_Type INT AUTO_INCREMENT PRIMARY KEY,
    Type text NOT NULL,
    Tarif Numeric(5,0) NOT NULL
);

-- Create the 'Chambre' table
CREATE TABLE IF NOT EXISTS Chambre (
    id_Chambre INT AUTO_INCREMENT PRIMARY KEY,
    Numéro Numeric(3,0) NOT NULL,
    Etage Numeric(2,0) NOT NULL,
    fumeur BOOLEAN NOT NULL,
    id_Hotel INT,
    id_Type INT,
    FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel),
    FOREIGN KEY (id_Type) REFERENCES Type_Chambre(id_Type)
);

-- Create the 'Client' table
CREATE TABLE IF NOT EXISTS Client (
    id_Client INT AUTO_INCREMENT PRIMARY KEY NOT NULL,
    Nom_Complet text NOT NULL,
    Adresse text NOT NULL,
    Ville text NOT NULL,
    Code_postal Numeric(5,0) NOT NULL,
    Email text NOT NULL,
    num_telephone Numeric(10,0) NOT NULL
);

-- Create the 'Reservation' table
CREATE TABLE IF NOT EXISTS Reservation (
    id_Reservation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivée DATE NOT NULL,
    Date_dépat DATE NOT NULL,
    id_Client INT,
    FOREIGN KEY (id_Client) REFERENCES Client(id_Client)
);

-- Create the 'Concerner' table
CREATE TABLE IF NOT EXISTS Concerner (
    id_Type INT,
    id_Reservation INT,
    FOREIGN KEY (id_Type) REFERENCES Type_Chambre(id_Type),
    FOREIGN KEY (id_Reservation) REFERENCES Reservation(id_Reservation)
);

-- Create the 'Prestation' table
CREATE TABLE IF NOT EXISTS Prestation (
    id_Prestation INT AUTO_INCREMENT PRIMARY KEY,
    Prix Numeric(5,0) NOT NULL
);

-- Create the 'Offre' table
CREATE TABLE IF NOT EXISTS Offre (
    id_Hotel INT,
    id_Prestation INT,
    FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel),
    FOREIGN KEY (id_Prestation) REFERENCES Prestation(id_Prestation)
);

-- Create the 'Evaluation' table
CREATE TABLE IF NOT EXISTS Evaluation (
    id_Evaluation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivée DATE NOT NULL,
    Note Numeric(1,0) NOT NULL,
    Commentaire text NOT NULL,
    id_Client INT,
    id_Hotel INT,
    FOREIGN KEY (id_Client) REFERENCES Client(id_Client),
    FOREIGN KEY (id_Hotel) REFERENCES Hotel(id_Hotel)
);