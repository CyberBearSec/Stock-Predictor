import logging
import os
import streamlit as st


def get_environmental_variables():
    st.markdown("<p>You need to set up the missing API keys and environment variables.</p>")
    if "OPENAI_API_KEY" not in os.environ.keys():
        st.markdown("We did not find an OPEN_API_KEY. Please go to the <a "
                    "href='https://platform.openai.com/account/api-keys' target='_new'>API key page</a>, and create "
                    "new secret key which is your OPEN_API_KEY.</p>",unsafe_allow_html=True)
    if "POLYGON_API_KEY" not in os.environ.keys():
        st.markdown("<p>We did not find a POLYGON_API_KEY.  To access real-time and historical stock market data with "
                    "Polygon please <a href='https://polygon.io/' target='_new'>create a Polygon account</a> and "
                    "then, once logged in, generate a new API key</p><p><b>NOTE: The free version of Polygon API only "
                    "supports previous day closes and only 5 per minute!</b></p>",unsafe_allow_html=True)
    if "RAPID_API_KEY" not in os.environ.keys():
        st.markdown("<p>We did not find a RAPID_API_KEY which we are using to access 10K reports.  Please go to <a "
                    "href='https://rapidapi.com/last10k/api/sec-filings/' target='_blank'>the Last 10K API</a>.  You "
                    "can sign up for a Rapid API Key and then subscribe to the Last 10K API page.  Your API key will "
                    "appear in the code sample at the bottom of the page.</p>",unsafe_allow_html=True)

    with st.form(key="frmEnvironment"):
        if "OPENAI_API_KEY" not in os.environ.keys():
            open_api_key = st.text_input("Please enter your Open API Key here", value=None)
        if "POLYGON_API_KEY" not in os.environ.keys():
            polygon_key = st.text_input("Please enter your Polygon IO Key here", value=None)
        if "RAPID_API_KEY" not in os.environ.keys():
            rapid_api_key = st.text_input("Please enter your Rapid API Key here", value=None)
        button_click = st.form_submit_button("Please Click Here to Set Your Environment")

    if button_click:
        if "OPENAI_API_KEY" not in os.environ.keys() and (not open_api_key or open_api_key == "" or "sk-" not in open_api_key):
            st.error("Please enter a valid Open AI Key as it is not set in your environment.")
        elif "POLYGON_API_KEY" not in os.environ.keys() and (not polygon_key or polygon_key == ""):
            st.error("Please enter a valid Polygon IO Key as it is not set in your environment.")
        elif "RAPID_API_KEY" not in os.environ.keys() and (not rapid_api_key or rapid_api_key == ""):
            st.error("Please enter a valid Rapid API Key for Last10K as it is not set in your environment.")

        if "OPENAI_API_KEY" not in os.environ.keys() and open_api_key and open_api_key != "":
            os.environ["OPENAI_API_KEY"] = open_api_key
            logging.info("Obtained Open API Key {}".format(open_api_key))

        if "POLYGON_API_KEY" not in os.environ.keys() and polygon_key and polygon_key != "":
            os.environ["POLYGON_API_KEY"] = polygon_key
            logging.info("Obtained Polygon API Key {}".format(polygon_key))

        if "RAPID_API_KEY" not in os.environ.keys() and rapid_api_key and rapid_api_key != "":
            os.environ["RAPID_API_KEY"] = rapid_api_key
            logging.info("Obtained Polygon API Key {}".format(rapid_api_key))
        st.rerun()
