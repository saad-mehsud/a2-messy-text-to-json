# Messy Text to JSON

This project extracts structured job-posting details from unstructured text using Google Gemini. It validates the returned data against a Pydantic model and prints it as JSON.

## Requirements

- Python 3.14 or newer
- A Google Gemini API key
- [uv](https://docs.astral.sh/uv/) for dependency management

## Setup

From the project directory, install the dependencies:

```bash
uv sync
```

Create a `.env` file in the project root:

```dotenv
GEMINI_API_KEY=your_api_key_here
GEMINI_MODELS=your_gemini_model_name
```

Keep `.env` private. `.env.example` can be used as a template.

## Run

Start the extractor:

```bash
uv run python extract.py
```

Paste or pipe the messy job-posting text, then end input with `Ctrl-D` on Linux/macOS or `Ctrl-Z` followed by Enter on Windows.

You can also process one of the included sample posts:

```bash
cat samples/hn_00.txt | uv run python extract.py
```

The program reads text from standard input and prints a single JSON object when extraction succeeds. It retries validation up to three times and retries temporary Gemini server errors.

## Sample Input

`samples/hn_00.txt` contains a text post for a DevOps Engineer position at Simple Analytics. It includes an informal introduction, the role details, location, salary, and technology stack.

## Sample Output

```json
{"title":"DevOps Engineer","company":"Simple Analytics","salary":"€5,000/month (full-time)","location":"REMOTE (worldwide, any timezone)","skills":["Ansible","OpenTofu","Docker Compose","Grafana","GitHub Actions","TypeScript"],"message":null}
```

Some fields may be `null` or contain empty lists when the source text does not clearly provide that information. The output is intentionally based only on evidence in the input rather than guessed data.

## What I Learned

- How to turn unstructured text into a consistent JSON shape using an AI model.
- How Pydantic schemas help validate model output and catch malformed responses.
- How prompting and structured generation work together to reduce extra prose in LLM responses.
- How to handle API failures, validation failures, and retries safely in a command-line Python application.
- How standard input and environment variables make a small command-line tool easy to configure and automate.