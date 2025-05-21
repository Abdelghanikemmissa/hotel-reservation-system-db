--Question a
SELECT Reservation.id_Reservation, Client., Reservation.Date_arrivée, Reservation.Date_dépat 
FROM Reservation
inner join Client on Reservation.id_Client = Client.id_Client;

--Question b
SELECT * 
FROM Client
where Ville = 'Paris';

--Question c
SELECT Client.id_Client, Client.Nom_Complet, COUNT(Reservation.id_Reservation) AS 'nombre de réservation'
FROM Client
inner join Reservation on Client.id_Client = Reservation.id_Client 
GROUP BY Client.id_Client;
--Question d

