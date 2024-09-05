from transformers import pipeline
from config.parametres import VERSIONS
from model.prompt import Prompt

def traduire(prompt:Prompt) :
    try :
        if prompt.version == VERSIONS[0] : # vérifier si le prompt correspond à la version fr à en
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-fr-en")

        else:
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-fr")

        result = translator(prompt.atraduire)        
        prompt.traduction = result[0]['translation_text']

    except Exception as e:
        print(f"An error occurred during translation: {e}")
        prompt.traduction = None 

    return(prompt)