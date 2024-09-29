import streamlit as st
from vue.traducteur_app import TraducteurApp

from vue.traducteur_app import TraducteurApp
from vue.dashboard_app import DashboardApp  

def main():
    st.sidebar.title("Navigation")
    pages = {
        "Traducteur": TraducteurApp,
        "Suivi des métriques": DashboardApp 
    }
    
    # Sélectionner la page à afficher
    selection = st.sidebar.radio("Aller à", list(pages.keys()))
    
    # Afficher la page sélectionnée
    page = pages[selection]()
    page.show()  

if __name__ == "__main__":
    TraducteurApp()
