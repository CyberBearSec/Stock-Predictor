from signals.ten_k_manager import download_10k_reports
import streamlit as st


def create_report_processor():
    st.markdown("The first signal being captured are 10K reports.")
    st.session_state["10K-reports"] = download_10k_reports(st.session_state["symbols"])
    st.session_state["radio_value"] = 2
    st.rerun()
