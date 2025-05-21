import streamlit as st
import sqlite3
from datetime import datetime
from datetime import date

def create_connection():
    try:
        conn = sqlite3.connect("hotel.db")
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        st.error(f"Database connection error: {e}")
        return None

# Fonction pour afficher la liste des clients
def view_clients(conn):
    st.subheader("👥 Liste des Clients")
    try:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id_Client, Nom_Complet, Adresse, Ville, Code_postal, Email, num_telephone
            FROM Client
            ORDER BY id_Client
        ''')
        rows = cursor.fetchall()
        if rows:
            results = [dict(row) for row in rows]
            st.success(f"{len(results)} client(s) trouvé(s).")
            st.dataframe(results)  # Affiche tous les clients dans un tableau scrollable
        else:
            st.warning("Aucun client trouvé dans la base.")
    except sqlite3.Error as e:
        st.error(f"Erreur lors de la récupération des clients : {e}")

# Fonction pour afficher la liste des réservations
def view_reservations(conn):
    st.subheader("📋 Liste des Réservations :")
    try:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT r.id_Reservation, 
               c.Nom_Complet AS Client_Name,
                c.Ville AS Client_City,
               r.Date_arrivée AS Arrival_Date,
               r.Date_dépat AS Departure_Date
        FROM Reservation r
        JOIN Client c ON r.id_Client = c.id_Client
        ORDER BY r.id_Reservation
        ''')
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        st.table(results)
    except sqlite3.Error as e:
        st.error(f"Query error: {e}")

# Fonction pour afficher les chambres disponibles
def view_available_rooms(conn):
    st.subheader("🚪 Chambres Disponibles")

    with st.form("dates_form"):
        start = st.date_input("Date d'arrivée")
        end = st.date_input("Date de départ")

        if st.form_submit_button("Rechercher"):
            if start >= end:
                st.error("La date d'arrivée doit être antérieure à la date de départ.")
                return

            try:
                cursor = conn.cursor()
                cursor.execute('''
                SELECT c.Numéro, 
                       c.Etage,
                       CASE WHEN c.fumeur = 1 THEN 'Oui' ELSE 'Non' END AS Fumeur,
                       tc.Type
                FROM Chambre c
                JOIN Type_Chambre tc ON c.id_Type = tc.id_Type
                WHERE c.id_Type NOT IN (
                    SELECT co.id_Type
                    FROM Reservation r
                    JOIN Concerner co ON r.id_Reservation = co.id_Reservation
                    WHERE NOT (r.Date_dépat <= ? OR r.Date_arrivée >= ?)  -- Correction ici: Date_dépat
                )
                ORDER BY tc.Type, c.Etage, c.Numéro
                ''', (start.isoformat(), end.isoformat()))

                rows = cursor.fetchall()
                
                if rows:
                    st.success(f"{len(rows)} chambre(s) disponible(s) du {start.strftime('%d/%m/%Y')} au {end.strftime('%d/%m/%Y')}")
                    
                    # Afficher sous forme de tableau
                    import pandas as pd
                    df = pd.DataFrame(rows, columns=["Numéro", "Étage", "Fumeur", "Type"])
                    st.dataframe(df)
                else:
                    st.warning("Aucune chambre disponible pour les dates sélectionnées.")
                    
            except sqlite3.Error as e:
                st.error(f"Erreur de base de données : {e}")

# Fonction pour ajouter un client
def add_client(conn):
    st.subheader("👤 Ajouter un Client")
    with st.form("client_form"):
        nom = st.text_input("Nom Complet*", placeholder="Obligatoire")
        adresse = st.text_input("Adresse", placeholder="Optionnel")
        ville = st.text_input("Ville", placeholder="Optionnel")
        cp = st.text_input("Code Postal", placeholder="Optionnel")
        email = st.text_input("Email*", placeholder="Obligatoire")
        tel = st.text_input("Téléphone*", placeholder="Obligatoire")
        
        if st.form_submit_button("Enregistrer"):
            # Vérification des champs obligatoires
            if not nom.strip() or not email.strip() or not tel.strip():
                st.error("Veuillez remplir tous les champs obligatoires (*)")
            else:
                try:
                    cursor = conn.cursor()
                    cursor.execute('''
                        INSERT INTO Client (Nom_Complet, Adresse, Ville, Code_postal, Email, num_telephone)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (nom.strip(), 
                          adresse.strip() if adresse else None,
                          ville.strip() if ville else None,
                          cp.strip() if cp else None,
                          email.strip(),
                          tel.strip()))
                    conn.commit()
                    st.success("Client ajouté avec succès!")
                    st.balloons()
                except sqlite3.Error as e:
                    st.error(f"Erreur lors de l'ajout : {e}")

# Fonction pour ajouter une réservation
def add_reservation(conn):
    st.subheader("➕ Ajouter une Réservation")
    
    with st.form("reservation_form"):
        # Section Informations Client
        st.markdown("### Informations Client")
        nom_client = st.text_input("Nom complet*")
        adresse = st.text_input("Adresse*")
        ville = st.text_input("Ville*")
        code_postal = st.text_input("Code postal* (5 chiffres)", max_chars=5)
        email = st.text_input("Email*")
        telephone = st.text_input("Téléphone* (10 chiffres)", max_chars=10)
        
        # Section Réservation
        st.markdown("### Détails de la Réservation")
        col1, col2 = st.columns(2)
        with col1:
            date_arrivee = st.date_input("Date d'arrivée*", min_value=date.today())
        with col2:
            date_depart = st.date_input("Date de départ*", min_value=date.today())
        
        # Section Type de Chambre
        cursor = conn.cursor()
        cursor.execute("SELECT id_Type, Type FROM Type_Chambre")
        # Conversion des résultats en tuples pour éviter l'erreur de sérialisation
        types_chambres = [tuple(row) for row in cursor.fetchall()]
        
        type_chambre = st.selectbox(
            "Type de chambre*",
            options=types_chambres,
            format_func=lambda x: f"{x[0]} - {x[1]}" 
        )
        
        # Bouton de soumission correctement configuré
        submitted = st.form_submit_button("Enregistrer la Réservation")
        
        if submitted:
            # Validation des champs obligatoires
            if not all([nom_client, adresse, ville, code_postal, email, telephone]):
                st.error("Veuillez remplir tous les champs obligatoires (*)")
                return
            
            # Validation des formats
            if not code_postal.isdigit() or len(code_postal) != 5:
                st.error("Le code postal doit contenir exactement 5 chiffres")
                return
                
            if not telephone.isdigit() or len(telephone) != 10:
                st.error("Le téléphone doit contenir exactement 10 chiffres")
                return
                
            if "@" not in email or "." not in email:
                st.error("Veuillez entrer une adresse email valide")
                return
                
            if date_arrivee >= date_depart:
                st.error("La date d'arrivée doit être antérieure à la date de départ")
                return
            
            try:
                cursor = conn.cursor()
                
                # 1. Vérifier/Créer le client
                cursor.execute("SELECT id_Client FROM Client WHERE Nom_Complet = ?", (nom_client,))
                client = cursor.fetchone()
                
                if client:
                    id_client = client[0]
                    st.warning(f"Client existant trouvé (ID: {id_client})")
                else:
                    cursor.execute('''
                        INSERT INTO Client (Nom_Complet, Adresse, Ville, Code_postal, Email, num_telephone)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (nom_client, adresse, ville, code_postal, email, telephone))
                    id_client = cursor.lastrowid
                    st.success(f"Nouveau client enregistré (ID: {id_client})")
                
                # 2. Créer la réservation
                cursor.execute('''
                    INSERT INTO Reservation (Date_arrivée, Date_dépat, id_Client)
                    VALUES (?, ?, ?)
                ''', (date_arrivee.isoformat(), date_depart.isoformat(), id_client))
                id_reservation = cursor.lastrowid
                
                # 3. Lier au type de chambre
                cursor.execute('''
                    INSERT INTO Concerner (id_Type, id_Reservation)
                    VALUES (?, ?)
                ''', (type_chambre[0], id_reservation))
                
                conn.commit()
                st.success(f"✅ Réservation #{id_reservation} ajoutée avec succès!")
                st.balloons()
                
            except sqlite3.Error as e:
                conn.rollback()
                st.error(f"❌ Erreur lors de l'ajout de la réservation : {e}")

# Page d'accueil
def home():
    st.markdown("""
    <style>
    .welcome-text {
        font-size: 1.1rem;
        line-height: 1.6;
        text-align: justify;
        margin-bottom: 30px;
    }
    .welcome-title {
        font-size: 2rem;
        color: #2e86c1;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="welcome-title">🏨 Bienvenue au Système de Gestion Hôtelière</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="welcome-text">
        Notre plateforme intuitive vous permet de gérer facilement les réservations, les chambres et les clients. 
        Que vous souhaitiez vérifier la disponibilité des chambres, enregistrer un nouveau client ou consulter 
        les réservations à venir, tous les outils sont à portée de main. Commencez par sélectionner une option 
        dans le menu de gauche pour accéder aux différentes fonctionnalités.
    </div>
    """, unsafe_allow_html=True)
    
    st.image("https://images.unsplash.com/photo-1566073771259-6a8506099945?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", 
             caption="Votre hôtel, notre système - une gestion simplifiée")
    


def main():
    st.title("🏨 Gestion Hôtelière")
    conn = create_connection()
    if not conn:
        return

    menu = ["🌿🏠 Home" , "👥 Liste des Clients","📋 Liste des Réservations" , "🚪 Chambres Disponibles", "👤 Ajouter Client", "➕ Nouvelle Réservation"]
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "🌿🏠 Home":
        home()
    elif choice == "👥 Liste des Clients":
        view_clients(conn)
    elif choice == "📋 Liste des Réservations":
        view_reservations(conn)
    elif choice == "🚪 Chambres Disponibles":
        view_available_rooms(conn)
    elif choice == "👤 Ajouter Client":
        add_client(conn)
    elif choice == "➕ Nouvelle Réservation":
        add_reservation(conn)

    conn.close()

if __name__ == "__main__":
    main()
