import streamlit as st
import datetime

def log_history(alg, mode, input_text, result):
    if "history" not in st.session_state:
        st.session_state["history"] = []
    st.session_state["history"].append({
        "algoritma": alg,
        "mode": mode,
        "input": input_text,
        "hasil": result,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    st.session_state["last_result"] = result

