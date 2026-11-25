# Imports that will be used 
import os,sys,time
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
SYSTEM_PROMPT = ""


def askGemini(message):
    try:
        with genai.Client(api_key=GEMINI_KEY) as client:
            resp = client.models.generate_content(
                model=GEMINI_MODEL,
                config={
                    "system_instruction":SYSTEM_PROMPT,
                    "response_schema":Extracted
                    },
                contents = message 
            )
            return resp.parsed       

    except errors.ServerError as err:
        if err.code == 503:
            print(f"Server Unavailable.Retrying.........\n{err.details}",file=sys.stderr)
    except errors.APIError as err:
        if err.code in [401,403]:
            return "Invalid API key was provided, provide a valid API key"
   


def extract(messyText = " ",tries = 3):

    for i in range(tries):
        try:
            extracted = askGemini(messyText)
            return Extracted.model_validate_json(extracted)
        except ValidationError as err:
            print("Validation Error occured. Retrying........",file = sys.stderr)
            message = f"""Data is not validate properly {err}.
            Correct the response and provide valid json for {extract}"""

        
def generateSystemPrompt():
    try:
        with open(f"{PROMPTPATH}/extract.txt",'r') as input:
            SYSTEM_PROMPT = input.read()
    except FileNotFoundError as err:
        print("Invalid file path.File not found.\n Process can not be continued without system prompt.")
        sys.exit(1)

def main():
    while(True):
        messyText = input("Enter Messy text of job post:")
        extractedText = extract(messyText)
        print(extractedText.model_dump_json)

if __name__ == "__main__":
    generateSystemPrompt()
    main()
