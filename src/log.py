import os
import streamlit as st

def log(message):

    # find which log file to write to
    if not os.path.isdir("logs"):
        os.mkdir("logs")

    num = st.session_state.get("log", 0)

    # Log to a file
    with open(f"logs/log{num}.txt", "a") as f:
        print(message, file=f)

