# AI Chatbot

A Streamlit chat application powered by LangGraph and OpenAI. Conversations are
kept in memory for the current application process and can be reset from the
sidebar.

## Features

- Streaming responses in a simple chat interface
- Selectable OpenAI model and response temperature
- Per-session conversation memory
- New-chat control for starting a fresh thread

## Requirements

- Python 3.10 or newer
- An OpenAI API key

## Setup

1. Create and activate a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

3. Create a local environment file and add your key:

   ```powershell
   Copy-Item .env.example .env
   ```

   Then set `OPENAI_API_KEY` in `.env`.

4. Start the application:

   ```powershell
   streamlit run app.py
   ```

The application opens at `http://localhost:8501`.

## Security

Never commit `.env` or paste an API key into source code. If a key has been
shared publicly or committed accidentally, revoke it in the OpenAI dashboard
and create a replacement immediately.

## Project structure

```text
app.py             Streamlit application
requirements.txt   Python dependencies
.env.example       Safe environment variable template
```
