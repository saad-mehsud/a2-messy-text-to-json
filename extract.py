import os
import dotenv as env
from google.genai import types
from groq import Groq
from pydantic import BaseModel,ValidationError
from typing import Optional

#Global constant and environments variable
PATH = os.path.dirname(os.path.abspath(__file__))
ENVPATH = f"{PATH}/.env"
env.load_dotenv()
GEMINI_KEY = env.get_key(ENVPATH,key_to_get="GEMINI_API_KEY")
GEMINI_MODEL = env.get_key(ENVPATH,key_to_get="GEMINI_MODELS")
GROQ_KEY = env.get_key(ENVPATH,key_to_get="GROQ_API_KEY")
GROQ_MODEL = env.get_key(ENVPATH,key_to_get="GROQ_MODELS")


def extract():
    pass

def main():
    pass

if __name__ == "__main__":
    main()
