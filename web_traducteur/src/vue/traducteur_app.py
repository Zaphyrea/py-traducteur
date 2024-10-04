# traducteur_app.py
import streamlit as st
import pandas as pd
import requests
import time

from streamlit_chat import message
from config.parametres import URL_TRADUCTEUR, URL_VERSIONS, URL_LOGIN, URL_TRADUCTIONS
from vue.dashboard_app import DashboardApp


class TraducteurApp:
    def __init__(self):
        self.URL_TRADUCTEUR = URL_TRADUCTEUR
        self.URL_VERSIONS = URL_VERSIONS
        self.URL_LOGIN = URL_LOGIN
        self.URL_TRADUCTIONS = URL_TRADUCTIONS
        self.titre = "Traducteur"

        # st.set_page_config(
        #     page_title="Traducteur",
        #     page_icon="🤖",
        #     layout="wide",
        #     initial_sidebar_state="expanded",
        # )

        if "logged_in" not in st.session_state:
            st.session_state["logged_in"] = None

        # self.show_login_form()
        self.show_app()

    def show_login_form(self):
    # Afficher le formulaire de connexion uniquement si l'utilisateur n'est pas connecté
        if st.session_state["logged_in"] is None:
            st.sidebar.title("Connexion")
            username = st.sidebar.text_input("Nom d'utilisateur", key="login_username")
            password = st.sidebar.text_input("Mot de passe", type="password", key="login_password")

            def login(username, password):

                data = {
                    "login": username,
                    "mdp": password
                }

                response = requests.post(self.URL_LOGIN, json=data)

                if response.status_code == 200:
                    response_login = response.json()

                    if response_login["authentifié"] :
                        st.session_state["logged_in"] = response_login["id"]
                
                if not st.session_state["logged_in"]:
                    st.sidebar.error("Nom d'utilisateur ou mot de passe incorrect")

            st.sidebar.button("Se connecter", on_click=login,  args=(username, password), key="login_button")
        else:
            # Si l'utilisateur est connecté, afficher un message de succès et le bouton de déconnexion
            st.sidebar.success(f"Connecté en tant que {st.session_state['logged_in']}")
            self.show_logout_button()

    def show_index(self) :
        st.title(self.titre)
        st.write("Veuillez vous connecter pour accéder aux fonctionnalités sécurisées.")
        
    def show_logout_button(self):
        def logout() :
            st.session_state["logged_in"] = None
            st.rerun() # Recharge la page pour mettre à jour l'interface

        # st.sidebar.title("Déconnexion")
        st.sidebar.button("Se déconnecter", on_click=logout, key="logout_button")    

    def show_app(self):
        # Ajout de la navigation dans la sidebar
        page = st.sidebar.radio("Navigation", ["Traduction", "Dashboard"])

        # Vérifier si l'utilisateur est connecté
        if st.session_state["logged_in"] is not None:
            # Si l'utilisateur est connecté, afficher les possibilités de traduction
            if page == "Traduction":
                st.title(self.titre)
                versions = self.get_versions()

                option = st.sidebar.selectbox(
                    "Choisissez la traduction à réaliser :",
                    versions
                )

                self.add_form(option)
                self.add_chat()

            elif page == "Dashboard":
                self.show_dashboard()

        # Afficher page de connexion si l'utilisateur n'est pas connecté
        else:
            self.show_login_form()

    def show_dashboard(self):
        dashboard = DashboardApp()  
        dashboard.show() 


    # def show_dashboard(self):
    #     st.title("Suivi de la latence du modèle de traduction")
    #     latences = self.get_metrics_data()

    #     if latences:
    #         df = pd.DataFrame(latences, columns=["Latence (s)"])
    #         st.line_chart(df)
    #         st.write(f"Latence moyenne : {df['Latence (s)'].mean():.2f} secondes")
    #         st.write(f"Latence maximale : {df['Latence (s)'].max():.2f} secondes")
    #         st.write(f"Latence minimale : {df['Latence (s)'].min():.2f} secondes")
    #     else:
    #         st.write("Aucune donnée de latence disponible.")


    def get_versions(self):
        versions = ["Aucune langue détectée !"]
        response = requests.get(self.URL_VERSIONS)

        if response.status_code == 200:
            versions = response.json()
        else:
            st.error(f"Erreur : {response.status_code}")
        return versions


    def add_form(self, option):
        st.subheader(option)
        atraduire = st.text_input("Texte à traduire")

        if st.button("Traduire"):
            word_count = len(atraduire.split())  
            data = {
                "atraduire": atraduire,
                "version": option,
                "utilisateur": st.session_state["logged_in"]
            }

            # Mesurer le temps de début
            start_time = time.time()

            # Appel à l'API de traduction
            response = requests.post(self.URL_TRADUCTEUR, json=data)

            # Mesurer la latence en secondes
            latence = time.time() - start_time

            # Enregistrer latence et nombre de mots dans un fichier de log
            self.log_latence(latence, word_count)

            if response.status_code == 200:
                st.success("Voici votre traduction !")
                response_data = response.json()
                reponse = response_data['traduction'] if isinstance(response_data['traduction'], str) else None
     
                # # Afficher la réponse complète pour voir sa structure
                # st.json(response_data)

                if reponse:
                    st.write(reponse)
                else:
                    st.error("Format de traduction inattendu.")
            else:
                st.error(f"Erreur : {response.status_code}")
                st.json(response.json())

    def add_chat(self):
        url = f"{self.URL_TRADUCTIONS}{st.session_state.logged_in}"
        chat = requests.get(url)

        if chat.status_code == 200:
            chat_messages = chat.json()

            # Historique des 5 derniers messages
            last_five_messages = chat_messages[-5:]

            for i, prompt in enumerate(last_five_messages):
                message(prompt["atraduire"], is_user=True, key=f"user_message_{i}") # ajout de clé pour pouvoir avoir plusieurs messages similaires
                message(prompt["traduction"], key=f"bot_message_{i}")
        else :
            st.error(f"Erreur : {chat.status_code}")

    def get_metrics_data(self):
        try:
            with open('latence_log.txt', 'r') as f:
                latences = [float(line.strip()) for line in f.readlines()]
            return latences
        except FileNotFoundError:
            st.write("Aucune donnée de latence disponible.")
            return []

    def log_latence(self, latence, nombre_mots):
        """
        Enregistre la latence et le nombre de mots dans un fichier CSV.

        Args:
            latence (float): La latence en secondes.
            nombre_mots (int): Le nombre de mots dans le texte traduit.
        """
        try:
            # max_time = self.get_max_translation_time(nombre_mots)
            # if latence > max_time:
            #     self.enregistrer_alerte(latence, nombre_mots, max_time)
        
            with open('latence_log.csv', 'a') as f:  # Ouvre le fichier en mode ajout ('a') pour enregistrer chaque latence
                f.write(f"{latence}, {nombre_mots}\n") 
        except Exception as e:
            st.error(f"Erreur lors de l'enregistrement de la latence : {e}")