import os
import dotenv as env
from google import genai
from groq import Groq
from pydantic import BaseModel,ValidationError
from typing import Optional
from schema import Extracted
#Global constant and environments variable
PATH = os.path.dirname(os.path.abspath(__file__))
ENVPATH = f"{PATH}/.env"
PROMPTPATH = f"{PATH}/prompts"
SAMPLESPATH = f"{PATH}/samples"
env.load_dotenv()
GEMINI_KEY = env.get_key(ENVPATH,key_to_get="GEMINI_API_KEY")
GEMINI_MODEL = env.get_key(ENVPATH,key_to_get="GEMINI_MODELS")
GROQ_KEY = env.get_key(ENVPATH,key_to_get="GROQ_API_KEY")
GROQ_MODEL = env.get_key(ENVPATH,key_to_get="GROQ_MODELS")


def extract():
    
    with genai.Client(api_key=GEMINI_KEY) as client:
        userPrompt = readSample+readPrompt()
        resp = client.models.generate_content(
            model=GEMINI_MODEL,
            contents = userPrompt if userPrompt  is not None else " ",
            config={"response_schema":Extracted}
        )
        print(resp)

def readPrompt():
    try:
        with open(f"{PROMPTPATH}/extract.txt",'r') as input:
            userPrompt = input.read()
            return userPrompt
    except FileNotFoundError as err:
        print("Invalid file path.File not found")
def readSample():
    try:
        with open(f"{SAMPLESPATH}/hn_00.txt") as sample:
            sampleText = input.read()
            return sampleText
    except FileNotFoundError as err:
        print("Invalid file path. File not found")
def main():
    readPrompt()

if __name__ == "__main__":
    main()
