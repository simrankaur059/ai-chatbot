import os
import uuid

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, MessagesState, StateGraph

load_dotenv()  # reads OPENAI_API_KEY from .env

SYSTEM_PROMPT = "You are a helpful, concise assistant."

st.set_page_config(page_title="AI Chatbot", page_icon="💬")

if not os.getenv("OPENAI_API_KEY"):
    st.error("OPENAI_API_KEY not found. Add it to your .env file and restart.")
    st.stop()


@st.cache_resource
def get_checkpointer() -> MemorySaver:
    # Cached so conversation memory survives Streamlit reruns.
    return MemorySaver()


@st.cache_resource
def build_graph(model_name: str, temperature: float):
    llm = ChatOpenAI(model=model_name, temperature=temperature, streaming=True, api_key=os.getenv("OPENAI_API_KEY"))

    def chatbot(state: MessagesState):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + state["messages"]
        return {"messages": [llm.invoke(messages)]}

    builder = StateGraph(MessagesState)
    builder.add_node("chatbot", chatbot)
    builder.add_edge(START, "chatbot")
    builder.add_edge("chatbot", END)
    return builder.compile(checkpointer=get_checkpointer())


# ---------- Sidebar ----------
with st.sidebar:
    st.header("Settings")
    model_name = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"],
        index=0,
    )
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)
    if st.button("New chat", use_container_width=True):
        st.session_state.thread_id = str(uuid.uuid4())
        st.rerun()

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

graph = build_graph(model_name, temperature)
config = {"configurable": {"thread_id": st.session_state.thread_id}}

# ---------- Chat history ----------
st.title("💬 AI Chatbot")

state = graph.get_state(config)
for msg in state.values.get("messages", []):
    role = "user" if msg.type == "human" else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ---------- Input ----------
if prompt := st.chat_input("Say something..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    def token_stream():
        for chunk, metadata in graph.stream(
            {"messages": [HumanMessage(content=prompt)]},
            config,
            stream_mode="messages",
        ):
            if metadata.get("langgraph_node") == "chatbot" and chunk.content:
                yield chunk.content

    with st.chat_message("assistant"):
        st.write_stream(token_stream())