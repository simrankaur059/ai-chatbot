# AI Chatbot

A conversational web app built with **Streamlit**, **LangGraph** and **LangChain**, powered by OpenAI models. It streams replies token by token, remembers each conversation, and lets you change the model and temperature from a sidebar.

**Author:** Simranpreet Kaur (UID: 26MCA20040, Class: 26MCA 1B)
**Faculty:** Munish Kumar (E16513)

## Features

- **Chat interface**: chat bubbles and an input box ("Say something...").
- **Live streaming**: answers appear as tokens arrive (`st.write_stream`).
- **Conversation memory**: each chat has its own `thread_id`, stored by LangGraph's `MemorySaver`.
- **New chat**: one click starts a fresh conversation.
- **Model selection**: `gpt-4o-mini` (default), `gpt-4o`, `gpt-4.1-mini`, `gpt-4.1`.
- **Temperature control**: slider from 0.0 to 1.5 (default 0.7).
- **Safe configuration**: the API key is read from `.env`; the app stops with a clear error if it is missing.

## How it works

The chatbot is a LangGraph state graph with a single node:

```
START → chatbot → END
```

The `chatbot` node adds the system prompt ("You are a helpful, concise assistant.") to the conversation history and calls `ChatOpenAI`. A cached `MemorySaver` checkpointer stores the messages per `thread_id`, so history is kept even when you change the model or temperature. Memory is in-memory only, so it is lost when the server restarts.

## Project structure

```
AI_proj/
├── app.py             # Streamlit app + LangGraph chatbot
├── requirements.txt   # Python dependencies
└── .env               # OPENAI_API_KEY (not committed)
```

## Requirements

- Python 3 (developed on Python 3.14)
- An OpenAI API key
- Internet connection

Dependencies (`requirements.txt`): `streamlit`, `python-dotenv`, `langchain-core`, `langchain-openai`, `langgraph`.

## Setup and run

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key to a .env file in the project folder
echo OPENAI_API_KEY=your_openai_api_key_here > .env

# 4. Start the app
streamlit run app.py
```

Streamlit opens the app in your browser, by default at http://localhost:8501.

## Security note

Never commit your `.env` file or the `.venv` folder. Add them to `.gitignore`:

```
.env
.venv/
```

## Future work

- Persistent memory (SQLite/PostgreSQL checkpointer)
- User accounts and saved chat history
- Retrieval-augmented generation over uploaded documents
- Tools and agents (web search, calculator, etc.)
- Editable system prompt / personas
- Better error handling for API failures and rate limits
