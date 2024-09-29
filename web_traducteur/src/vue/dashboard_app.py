import streamlit as st
import pandas as pd
import os

class DashboardApp:
    def __init__(self):
        self.titre = "Suivi des métriques"
        st.set_page_config(
            page_title=self.titre,
            page_icon="📊",
            layout="wide",
            initial_sidebar_state="expanded",
        )

    def show(self):
        st.title(self.titre)
        st.sidebar.button("Rafraîchir les données", on_click=self.show_metrics)  
        self.show_metrics()

    def load_latence_data(self, max_entries=100):
        file_path = 'latence_log.txt'
        if not os.path.exists(file_path):
            st.write("Aucune donnée de latence disponible.")
            return []

        try:
            with open(file_path, 'r') as f:
                latences = [float(line.strip()) for line in f.readlines()[-max_entries:]]  # Ne prendre que les 100 dernières lignes
            return latences
        except Exception as e:
            st.error(f"Erreur lors du chargement des données de latence : {e}")
            return []

    def show_metrics(self):
        latences = self.load_latence_data()

        if latences:
            df = pd.DataFrame(latences, columns=["Latence (s)"])
            
            # Afficher les graphiques et statistiques
            st.line_chart(df)
            st.write(f"Latence moyenne : {df['Latence (s)'].mean():.2f} secondes")
            st.write(f"Latence maximale : {df['Latence (s)'].max():.2f} secondes")
            st.write(f"Latence minimale : {df['Latence (s)'].min():.2f} secondes")


            if st.checkbox("Afficher l'histogramme des latences"):
                st.bar_chart(df["Latence (s)"].value_counts().sort_index())
        else:
            st.write("Aucune donnée de latence disponible.")


