from langchain_openai import ChatOpenAI
import streamlit as st

class symbol_parts:
    symbol_name: str
    fair_value: float
    current_price: float


def select_model(model, aiTemp):
    if model == "GPT-3.5":
        st.session_state["model_name"] = "gpt-3.5-turbo"
    elif model == "GPT-3.5-16k":
        st.session_state["model_name"] = "gpt-3.5-turbo-16k"
    else:
        st.session_state["model_name"] = "gpt-4"

    # 300: The number of tokens for instructions outside the main text
    return ChatOpenAI(temperature=aiTemp, model_name=st.session_state["model_name"])