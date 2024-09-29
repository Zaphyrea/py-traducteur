from dto.connexion import Connexion
from model.prompt import Prompt
from model.utilisateur import Utilisateur
from model.latence import Latence

import time
import requests
class Service_Traducteur(Connexion):

    @classmethod
    def sauvegarder_prompt(cls, prompt:Prompt):
        try :
            cls.ouvrir_connexion()
            query = "INSERT INTO prompts (text_in, text_out, version, utilisateur) VALUES (%s, %s, %s, %s)"
            values = [prompt.atraduire, prompt.traduction, prompt.version, prompt.utilisateur]
            
            cls.cursor.execute(query, values)
            cls.bdd.commit()
            cls.fermer_connexion()
        except Exception as e:
            print(f"Une erreur inattendue est survenue :{e}")

    @classmethod
    def verifier_login(cls, utilisateur:Utilisateur):
        try:
            cls.ouvrir_connexion()
            query = "SELECT id, login, mdp FROM utilisateurs WHERE login=%s AND mdp=%s"
            values = [utilisateur.login, utilisateur.mdp]
            cls.cursor.execute(query, values)
            result = cls.cursor.fetchone()

            if result :
                utilisateur.id = result['id']
                utilisateur.authentifie = True

        except Exception as e:
                print(f"Une erreur inattendue est survenue :{e}")
        
        finally:
            cls.fermer_connexion()

    @classmethod
    def lister_prompts(cls, utilisateur:int):
        prompts=[]

        cls.ouvrir_connexion()
        query = "SELECT * FROM prompts WHERE utilisateur=%s"
        values=[utilisateur]
        cls.cursor.execute(query, values)
            
        for prompt_lu in cls.cursor :
            prompt = Prompt(atraduire=prompt_lu["text_in"], traduction=prompt_lu["text_out"], version=prompt_lu["version"], utilisateur=prompt_lu["utilisateur"])
            prompts.append(prompt)

        cls.fermer_connexion()
        
        return prompts

    @classmethod

    def appeler_modele_traduction(cls, data):
        start_time = time.time()  # Commence le chronométrage

        response = requests.post(cls.URL_TRADUCTEUR, json=data)
        
        end_time = time.time()  # Fin du chronométrage
        latence_ms = int((end_time - start_time) * 1000)  # Latence en millisecondes

        # Enregistrer la latence
        latence = Latence(utilisateur_id=data['utilisateur'], latence_ms=latence_ms, version=data['version'], statut_code=response.status_code)
        cls.sauvegarder_latence(latence)

        return response

    @classmethod
    def sauvegarder_latence(cls, latence: Latence):
        try:
            cls.ouvrir_connexion()
            query = "INSERT INTO latences (utilisateur_id, latence_ms, version, statut_code) VALUES (%s, %s, %s, %s)"
            values = [latence.utilisateur_id, latence.latence_ms, latence.version, latence.statut_code]
            cls.cursor.execute(query, values)
            cls.bdd.commit()
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la latence : {e}")
        finally:
            cls.fermer_connexion()             

    @classmethod
    def lister_latences(cls):
        latences = []
        try:
            cls.ouvrir_connexion()
            query = "SELECT * FROM latences"
            cls.cursor.execute(query)
            for latence_lue in cls.cursor:
                latence = Latence(utilisateur_id=latence_lue["utilisateur_id"], latence_ms=latence_lue["latence_ms"], version=latence_lue["version"], statut_code=latence_lue["statut_code"])
                latences.append(latence)
        except Exception as e:
            print(f"Erreur lors de la récupération des latences : {e}")
        finally:
            cls.fermer_connexion()
        return latences
