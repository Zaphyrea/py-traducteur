from fastapi import FastAPI
import uvicorn

from config.parametres import VERSIONS
from model.nlp import traduire
from model.prompt import Prompt
from dto.service_traducteur import Service_Traducteur as st
from model.utilisateur import Utilisateur


tags =[
       {
         "name":"index",
         "description":"Index"     
       },
     {
          "name":"traduction",
          "description":"Traduction"
     },
     {
          "name":"authentification",
          "description":"authentification"
     }
]

app = FastAPI(
     title="Appli de traduction",
     description="API de traduction",
     version="1.0.0",
     openapi_tags = tags
)

@app.get("/versions", tags=["index"])
def versions():
        return VERSIONS

@app.post("/traductions", tags=["traduction"])
def traducteur(prompt:Prompt):
        traduire(prompt)
        st.sauvegarder_prompt(prompt)
        return prompt

@app.get("/traductions/auteur/{id}", tags=["traduction"])
def versions_par_auteur(id:int):
       return st.lister_prompts(id)

@app.post("/login", tags=["authentification"])
def authentifier(utilisateur:Utilisateur):
       st.verifier_login(utilisateur)
       return {"authentifié" : utilisateur.authentifie, "id":utilisateur.id}

if __name__ == "__main__" :
    uvicorn.run("api:app", host="0.0.0.0", port=8080)