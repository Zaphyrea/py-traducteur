import streamlit as st
import pandas as pd
import os
import plotly.express as px

class DashboardApp:
    def __init__(self):
        self.titre = "Suivi des métriques"
        # st.set_page_config(
        #     page_title=self.titre,
        #     page_icon="📊",
        #     layout="wide",
        #     initial_sidebar_state="expanded",
        # )

    def show(self):
        st.title(self.titre)
        st.sidebar.button("Rafraîchir les données", on_click=self.show_metrics)  
        self.show_metrics()
        self.show_correlation()

    def load_latence_data(self, max_entries=100):
        file_path = 'latence_log.csv'
        if not os.path.exists(file_path):
            st.write("Aucune donnée de latence disponible.")
            return pd.DataFrame()

        try:
            df = pd.read_csv(file_path, names=["Latence (s)", "Nombre de mots"])
            return df.tail(max_entries)

        except Exception as e:
            st.error(f"Erreur lors du chargement des données de latence : {e}")
            return pd.DataFrame()
        
    def show_correlation(self):
        latences = self.load_latence_data()

        if not latences.empty:
            st.write("Corrélation entre la latence et le nombre de mots :")
            fig = px.scatter(latences, x='Nombre de mots', y='Latence (s)', title='Latence en fonction du nombre de mots')
            st.plotly_chart(fig)
        else:
            st.write("Aucune donnée de latence disponible.")

    def show_metrics(self):
        latences = self.load_latence_data()

        if not latences.empty:  # Check if DataFrame is not empty
            df = pd.DataFrame(latences, columns=["Latence (s)"])
            
            # # Display charts and statistics
            # st.line_chart(df)
            # st.write(f"Latence moyenne : {df['Latence (s)'].mean():.2f} secondes")
            # st.write(f"Latence maximale : {df['Latence (s)'].max():.2f} secondes")
            # st.write(f"Latence minimale : {df['Latence (s)'].min():.2f} secondes")

            # if st.checkbox("Afficher l'histogramme des latences"):
            #     st.bar_chart(df["Latence (s)"].value_counts().sort_index())
        else:
            st.write("Aucune donnée de latence disponible.")
