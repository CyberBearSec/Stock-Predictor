import os

if "is_linux" in os.environ:
    __import__('pysqlite3')
    import sys

    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
from loggers.log_manager import logging
import openai
from nav.input_manager import create_stock_adding_screen
from nav.environment_manager import get_environmental_variables
from nav.model_manager import run_openai_as_stock_expert
from nav.output_manager import create_results_screen
from nav.signal_processor import create_report_processor
import streamlit as st
import traceback

def init_page():
    st.set_page_config(
        page_title="The Stock Predictor :brain:",
        page_icon=":chart_with_upwards_trend:"
    )
    st.sidebar.image("./FullLogo.png", width=300, use_column_width="always")
    if "radio_value" not in st.session_state:
        st.session_state["radio_value"] = 0
    st.title("The Stock Predictor")

    # ***NOTE: CHANGE LOGGING LEVEL HERE***
    st.session_state["logging_level"] = logging.INFO
    logging.basicConfig(level=st.session_state["logging_level"])


def main():
    try:
        init_page()
        if "OPENAI_API_KEY" not in os.environ.keys() or "RAPID_API_KEY" not in os.environ.keys() or "POLYGON_API_KEY" not in os.environ.keys():
            get_environmental_variables()
        else:
            selection = st.sidebar.radio("Menu",
                                         ["Enter Stock Symbols", "Retrieve Reports", "Analyze Results",
                                          "Show Buy/Sell"],
                                         index=st.session_state["radio_value"])
            if selection == "Enter Stock Symbols":
                create_stock_adding_screen()
            elif selection == "Retrieve Reports":
                create_report_processor()
            elif selection == "Analyze Results":
                run_openai_as_stock_expert()
            elif selection == "Show Buy/Sell":
                create_results_screen()
    except openai.APIConnectionError as e:
        logging.error(f"OpenAI API request failed to connect: {traceback.format_exc()}")
        st.error("There was an issue connecting to Chat GPT, please wait a minute and enter your question again")
    except openai.RateLimitError as e:
        logging.error(f"OpenAI API request exceeded rate limit: {traceback.format_exc()}")
        st.error("Your API rate limit has been reached!  Try increasing your compression and trying again later.")
    except openai.AuthenticationError as e:
        logging.error(f"OpenAI request was not authorized: {e.__cause__}")
        st.error("Your API Key does not support this application")
    except openai.PermissionDeniedError as e:
        logging.error(f"Permission was denied for this request: {traceback.format_exc()}")
        st.error("Your API Key does not support this application")
    except openai.APIStatusError as e:
        logging.error(f"OpenAI API returned an API Error: {traceback.format_exc()}")
        st.error("There was an issue connecting to Chat")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {traceback.format_exc()}")
        st.error("An unexpected error has occurred, please contact support.")
    finally:
        logging.info("Loaded the next page.")


if __name__ == "__main__":
    main()
