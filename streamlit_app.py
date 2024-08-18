import streamlit as st
import random
import time
import asyncio
from websockets.sync.client import connect
import json
import secrets

websocket = connect("wss://araeyn-schoolquest.hf.space")

def response_generator(message):
    websocket.send(json.dumps({"token": st.session_state.session_id, "message": prompt, "response": prompt}))
    message = json.loads(websocket.recv())
    print(f"Received: {type(message)} || {message}")
    response = message["response"].replace("\n", "  \n")
    #for word in response.split():
    #    yield word + " "
    #    time.sleep(0.05)
    return response

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

st.title("School Quest 🏫 ")
st.caption("Get info about schools.")
if "session_id" not in st.session_state:
    st.session_state.session_id = secrets.token_urlsafe(16)

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # response = st.write_stream(response_generator(prompt))
        response = st.markdown(response_generator(prompt))
    st.session_state.messages.append({"role": "assistant", "content": response})
