-- INSERT DATA INTO TABLES
-- Insert data into the 'Hotel' table
INSERT INTO Hotel (id_Hotel,Ville, Pays, code_postal) VALUES
(1, 'Paris', 'France', 75001),
(2, 'Lyon', 'France', 69002);

-- Insert data into the 'Type_Chambre' table
INSERT INTO Type_Chambre (id_Type, Type, Tarif) VALUES
(1, 'Simple', 80),
(2, 'Double', 120);

-- Insert data into the 'Chambre' table
INSERT INTO Chambre (id_Chambre,Numéro, Etage, fumeur, id_Hotel, id_Type) VALUES
(1, 201, 2, 0, 1, 1),
(2, 502, 5, 1, 1, 2),
(3, 305, 3, 0, 2, 1),
(4, 410, 4, 0, 2, 2),
(5, 104, 1, 1, 2, 2),
(6, 202, 2, 0, 1, 1),
(7, 307, 3, 1, 1, 2),
(8, 101, 1, 0, 1, 1);
-- Insert data into the 'Client' table
INSERT INTO Client (id_Client, Adresse, Ville, Code_postal, Email, num_telephone, Nom_Complet) VALUES
(1, '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr',
'00612345678', 'Jean Dupont'),

(2, '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr',
'00623456789', 'Marie Leroy'),

(3, '8 Boulevard Saint-Michel', 'Marseille', 13005,
'paul.moreau@email.fr', '00634567890', 'Paul Moreau'),

(4, '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr',
'00645678901', 'Lucie Martin'),

(5, '3 Rue des Fleurs', 'Nice', 06000, 'emma.giraud@email.fr',
'00656789012', 'Emma Giraud');

-- Insert data into the 'Reservation' table
INSERT INTO Reservation (id_Reservation, Date_arrivée, Date_dépat, id_Client) VALUES
-- Client 1 (Jean Dupont)
(1, '2025-06-15', '2025-06-18', 1),
-- Client 2 (Marie Leroy)
(2, '2025-07-01', '2025-07-05', 2),
(7, '2025-11-12', '2025-11-14', 2),
(10, '2026-02-01', '2026-02-05', 2),

-- Client 3 (Paul Moreau)
(3, '2025-08-10', '2025-08-14', 3),

-- Client 4 (Lucie Martin)
(4, '2025-09-05', '2025-09-07', 4),
(9, '2026-01-15', '2026-01-18', 4),

-- Client 5 (Emma Giraud)
(5, '2025-09-20', '2025-09-25', 5);

-- Insert data into the ' Evaluation' table
INSERT INTO Evaluation ( id_Evaluation, Date_arrivée, Note, Commentaire, id_Client) VALUES
(1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.',1),

(2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),

(3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),

(4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),

(5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5);

