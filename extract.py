import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors
from pydantic import ValidationError

from schema import Extracted


base_path = os.path.dirname(os.path.abspath(__file__))
env_path = f"{base_path}/.env"
prompt_path = f"{base_path}/prompts"
load_dotenv(env_path)

gemini_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODELS")


def ask_gemini(
    client: genai.Client,
    message: str,
    system_prompt: str,
) -> str:
    for attempt in range(4):
        try:
            response = client.models.generate_content(
                model=gemini_model,
                config={
                    "system_instruction": system_prompt,
                    "response_schema": Extracted,
                    "response_mime_type": "application/json"
                },
                
                contents=message,
            )
        except errors.APIError as err:
            if err.code in (401, 403):
                print(
                    "Invalid API key was provided; provide a valid API key.",
                    file=sys.stderr,
                )
                raise SystemExit(1) from err
            if err.code != 503 or attempt == 3:
                raise

            delay = 2**attempt
            print(
                f"Server unavailable. Retrying in {delay}s.\n{err}",
                file=sys.stderr,
            )
            time.sleep(delay)
            continue

        if response.text is None:
            raise ValueError("Gemini returned no response text.")
        return response.text

    raise RuntimeError("Gemini request retry loop ended unexpectedly.")


def extract(
    client: genai.Client,
    original_text: str,
    system_prompt: str,
    tries: int = 3,
) -> Extracted | None:
    message = original_text
    for attempt in range(tries):
        try:
            response_text = ask_gemini(client, message, system_prompt)
            return Extracted.model_validate_json(response_text)
        except ValidationError as err:
            print(f"Validation error occurred:\n{err}", file=sys.stderr)
            if attempt + 1 < tries:
                message = (
                    f"{original_text}\n\n"
                    f"Validation error:\n{err}\n\n"
                    "Return valid JSON only."
                )

    return None


def generate_system_prompt() -> str:
    try:
        with open(f"{prompt_path}/extract.txt", "r") as prompt_file:
            return prompt_file.read()
    except FileNotFoundError:
        print(
            "Invalid file path. File not found.\n"
            "Process cannot be continued without system prompt.",
            file=sys.stderr,
        )
        raise SystemExit(1)


def main() -> None:
    system_prompt = generate_system_prompt()
    with genai.Client(api_key=gemini_key) as client:
        while True:
            print(
                "Enter messy text of job post (end with Ctrl-D / Ctrl-Z+Enter):",
                end="",
                flush=True,
            )
            messy_text = sys.stdin.read()
            print("Extraction Started")
            if not messy_text:
                break

            extracted_text = extract(client, messy_text, system_prompt)
            if extracted_text is None:
                print("Could not extract valid job data after all attempts.", file=sys.stderr)
                continue
            print(extracted_text.model_dump_json())


if __name__ == "__main__":
    main()
