# Imports that will be used 
import os,sys
import dotenv as env
from google import genai
from google.genai import errors
from groq import Groq
from pydantic import BaseModel,ValidationError
from typing import Optional
from schema import Extracted


# Global constant and environments variable
PATH = os.path.dirname(os.path.abspath(__file__))
ENVPATH = f"{PATH}/.env"
PROMPTPATH = f"{PATH}/prompts"
SAMPLESPATH = f"{PATH}/samples"
env.load_dotenv()
GEMINI_KEY = env.get_key(ENVPATH,key_to_get="GEMINI_API_KEY")
GEMINI_MODEL = env.get_key(ENVPATH,key_to_get="GEMINI_MODELS")
GROQ_KEY = env.get_key(ENVPATH,key_to_get="GROQ_API_KEY")
GROQ_MODEL = env.get_key(ENVPATH,key_to_get="GROQ_MODELS")


def extract(messyText = " "):
    try:
        with genai.Client(api_key=GEMINI_KEY) as client:
            userPrompt = readPrompt()+messyText
            resp = client.models.generate_content(
                model=GEMINI_MODEL,
                contents = userPrompt if userPrompt  is not None else " ",
                config={"response_schema":Extracted}
            )
            Extracted.model_validate(resp.parsed)
            print("Parsed:",resp.parsed)
    except errors.ServerError as err:
        if err.code == '503':
            print("The server is currently unavailable kindly try again after 30 sec")
    except errors.APIError as err:
        if err.code in [401,403]:
            print("Invalid API key provided. Verify your auth key.")
    except ValidationError as verr:
        print(f"Validation error occured:{verr.json}")
def readPrompt():
    try:
        with open(f"{PROMPTPATH}/extract.txt",'r') as input:
            userPrompt = input.read()
            return userPrompt
    except FileNotFoundError as err:
        print("Invalid file path.File not found")
# def readSample():
#     try:
#         with open(f"{SAMPLESPATH}/hn_05.txt") as sample:
#             sampleText = sample.read()
#             return sampleText
#     except FileNotFoundError as err:
#         print("Invalid file path. File not found")
def main():
    messyText = sys.argv[1]
    extract(messyText)

if __name__ == "__main__":
    main()
