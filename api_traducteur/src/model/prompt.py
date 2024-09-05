from pydantic import BaseModel

class Prompt(BaseModel) :
    atraduire : str
    traduction : str = None
    version : str
    utilisateur : int