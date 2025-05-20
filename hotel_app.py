# hotel_app.py
import streamlit as st
import mysql.connector
from datetime import datetime

def create_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password=" ",
            database="database_project"
        )
    except mysql.connector.Error as e:
        st.error(f"Database connection error: {e}")
        return None

def view_reservations(conn):
    st.subheader("Liste des Réservations")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
        SELECT r.id_Reservation, 
           c.Nom_Complet AS Client_Name,
           c.Ville AS Hotel_City,
           r.Date_arrivée AS Arrival_Date,
           r.Date_dépat AS Departure_Date
        FROM Reservation r
        JOIN Client c ON r.id_Client = c.id_Client
        order by r.id_Reservation
        ''')
        st.table(cursor.fetchall())
    except mysql.connector.Error as e:
        st.error(f"Query error: {e}")

def view_clients(conn):
    st.subheader("Liste des Clients")
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
        SELECT 
            c.id_Client,
            c.Nom_Complet,
            c.Adresse,
            c.Ville,
            c.Code_Postal,
            c.Email,    
            c.num_telephone
        FROM Client c
        order by c.id_Client
        ''')
        st.table(cursor.fetchall())
    except mysql.connector.Error as e:
        st.error(f"Query error: {e}")

def view_available_rooms(conn):
    st.subheader("Chambres Disponibles")

    with st.form("dates_form"):
        start = st.date_input("Date d'arrivée")
        end = st.date_input("Date de départ")

        if st.form_submit_button("Rechercher"):
            if start >= end:
                st.error("La date d'arrivée doit être antérieure à la date de départ.")
                return

            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute('''
                    SELECT c.Numéro, c.Etage, c.fumeur, tc.Type
                    FROM Chambre c
                    JOIN Type_Chambre tc ON c.id_Type = tc.id_Type
                    WHERE c.id_Chambre NOT IN (
                        SELECT rc.id_Chambre
                        FROM Reservation r
                        JOIN Concerner co ON r.id_Reservation = co.id_Reservation
                        JOIN Chambre rc ON rc.id_Type = co.id_Type
                        WHERE (r.Date_arrivée < %s AND r.Date_dépat > %s)
                    )
                ''', (start,end ))

                results = cursor.fetchall()

                if results:
                    st.success(f"{len(results)} chambre(s) disponible(s).")
                    st.table(results)
                else:
                    st.warning("Aucune chambre disponible pour cette période.")

            except mysql.connector.Error as e:
                st.error(f"Erreur SQL : {e}")

def add_client(conn):
    st.subheader("Ajouter un Client")
    with st.form("client_form"):
        idclient = st.number_input("id_Client", min_value=0)
        nom = st.text_input("Nom Complet")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        cp = st.number_input("Code Postal", min_value=0)
        email = st.text_input("Email")
        tel = st.text_input("Téléphone")
        if st.form_submit_button("Enregistrer"):
            try:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO Client (id_Client,Nom_Complet, Adresse, Ville, Code_postal, Email, num_telephone)
                    VALUES ( %s, %s, %s,%s, %s, %s, %s)
                ''', (idclient,nom, adresse,  ville, cp, email, tel))
                conn.commit()
                st.success("Client ajouté!")
            except mysql.connector.Error as e:
                st.error(f"Insert error: {e}")

def main():
    st.title("Gestion Hôtelière")
    conn = create_connection()
    if not conn:
        return
    
    menu = ["Liste des Réservations", "Liste des Clients", "Chambres Disponibiles", "Ajouter Client"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Liste des Réservations":
        view_reservations(conn)
    elif choice == "Liste des Clients":
        view_clients(conn)
    elif choice == "Chambres Disponibiles":
        view_available_rooms(conn)
    elif choice == "Ajouter Client":
        add_client(conn)
    
    conn.close()

if __name__ == "__main__":
    main()