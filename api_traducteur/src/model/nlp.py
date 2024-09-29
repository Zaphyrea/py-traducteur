import time 

from transformers import pipeline
from config.parametres import VERSIONS
from model.prompt import Prompt

def traduire(prompt:Prompt) :
    try :
        start_time = time.time()  # Mesure du temps de début
        if prompt.version == VERSIONS[0] : # vérifier si le prompt correspond à la version fr à en
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

        else:
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

        result = translator(prompt.atraduire)        
        prompt.traduction = result[0]['translation_text']

        end_time = time.time()  # Temps de fin
        latence = end_time - start_time  # Calculer la latence

        # Appeler une fonction pour enregistrer la latence
        save_latence(latence)

    except Exception as e:
        print(f"An error occurred during translation: {e}")
        prompt.traduction = None 

    return(prompt)

# Fonction pour sauvegarder la latence dans un fichier texte
def save_latence(latence):
    with open('latence_log.txt', 'a') as f:
        f.write(f"{latence}\n")