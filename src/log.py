import os
import streamlit as st
import datetime

def log(message):

    # find which log file to write to
    if not os.path.isdir("logs"):
        os.makedirs("logs", exist_ok=True)

    logname = st.session_state.get("log", "logs/log.txt")
    
    # Log to a file
    with open(logname, 'a') as f:
        date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        print(f'[{date}] {message}', file=f)

