import streamlit as st


def create_results_screen():
    st.markdown("<h2>Results</h2>", unsafe_allow_html=True)
    st.markdown("<p>Here are the insights obtained for each of your entered stocks.</p>", unsafe_allow_html=True)
    for thisSymbol in st.session_state["symbols"]:
        st.markdown(f"<h3>{thisSymbol.symbol_name}</h3><div>Fair Market Price:${thisSymbol.fair_value}</div>"
                    f"<div>Last Price:${thisSymbol.current_price}</div><p>", unsafe_allow_html=True)
        st.markdown(st.session_state["stock_replies"][thisSymbol.symbol_name] + "</p><hr/>",
                    unsafe_allow_html=True)
