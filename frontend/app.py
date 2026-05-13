import streamlit as st
import requests

st.set_page_config(page_title="TailorTalk AI")

st.title("📁 TailorTalk AI")
st.write("Search files in Google Drive using AI")

user_input = st.chat_input("Ask something...")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"message": user_input}
    )

    data = response.json()

    with st.chat_message("assistant"):
        st.write(data["result"])