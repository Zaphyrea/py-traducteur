import streamlit as st
import pandas as pd
import os
import plotly.express as px

class DashboardApp:
    def __init__(self):
        self.titre = "Suivi des métriques"

    def show(self):
        st.title(self.titre)
        if st.sidebar.button("Rafraîchir les données"):
            self.refresh_data()
        else:
            self.show_metrics()
            self.show_correlation()
            self.show_alertes()

    def refresh_data(self):
        self.show_metrics()
        self.show_correlation()
        self.show_alertes()

    def load_latence_data(self, max_entries=100):
        file_path = 'latence_log.csv'
        if not os.path.exists(file_path):
            return pd.DataFrame()

        try:
            df = pd.read_csv(file_path, names=["Latence (s)", "Nombre de mots"])
            return df.tail(max_entries)

        except Exception as e:
            st.error(f"Erreur lors du chargement des données de latence : {e}")
            return pd.DataFrame()
        
    def show_correlation(self):
        latences = self.load_latence_data()
        if latences.empty:
            st.write("Aucune donnée de latence disponible.")
        else:
            st.write("Corrélation entre la latence et le nombre de mots :")
            fig = px.scatter(latences, x='Nombre de mots', y='Latence (s)', title='Latence en fonction du nombre de mots')
            st.plotly_chart(fig)

    def show_metrics(self):
        latences = self.load_latence_data()

        if not latences.empty: 
            df = pd.DataFrame(latences, columns=["Latence (s)"])
            
            # Display charts and statistics
            # st.line_chart(df)
            st.write(f"Latence moyenne : {df['Latence (s)'].mean():.2f} secondes")
            st.write(f"Latence maximale : {df['Latence (s)'].max():.2f} secondes")
            st.write(f"Latence minimale : {df['Latence (s)'].min():.2f} secondes")


    def load_alertes_data(self):
        file_path = 'alertes_log.csv'
        if not os.path.exists(file_path):
            return pd.DataFrame()

        try:
            df = pd.read_csv(file_path, names=["Date", "Heure", "Utilisateur", "Latence en secondes", "Nombre de mots", "Durée maximale autorisée"])
            return df
        except Exception as e:
            st.error(f"Erreur lors du chargement des alertes : {e}")
            return pd.DataFrame()

    def show_alertes(self):
        alertes = self.load_alertes_data()
        
        if alertes.empty:
            st.write("Aucune alerte disponible.")
        else:
            st.write("Tableau des alertes de latence")
            st.dataframe(alertes)
