from loggers.log_manager import get_logger
import logging
from io import StringIO
from signals.polygon_manager import get_previous_close
import streamlit as st
from utility.utilities import symbol_parts


def create_stock_adding_screen():
    logger = get_logger("RESTClient")
    logger.setLevel(st.session_state["logging_level"])
    st.markdown("<p>Please enter a stock symbol and a fair market value and then click Add Stock.  When you are done "
                "adding stocks, click Done Adding Stocks.</p><p>If you have a CSV file in the form Stock Name, Fair "
                "Price then you can upload that instead.</p><p><b>NOTE: The free version of Polygon API only supports "
                "prior day closes and only 5 requests per minute!</b></p>", unsafe_allow_html=True)
    with(st.form(key="frmGetStocks", clear_on_submit=True)):
        stock_symbol = st.text_input("Enter a stock symbol", value=None)
        stock_value = st.number_input("Enter the Fair Market Value (number only, no $ signs)", value=None)
        stock_file = st.file_uploader("Optionally choose a CSV file", type=['csv', 'txt'])
        symbol_click = st.form_submit_button("Add Stock(s)")
    done_click = st.button("Done Adding Stocks")
    if "symbols" not in st.session_state:
        st.session_state["symbols"] = []
    if symbol_click:
        if stock_file is not None:
            logging.info("Uploading a file...")
            with st.spinner("Processing your stocks now..."):
                symbolsLoaded = 0
                stringio = StringIO(stock_file.read().decode("utf-8"))
                for stock_line in stringio.readlines():
                    logging.info(f"Current stock line is: {stock_line}")
                    if "," in stock_line:
                        stock_parts = stock_line.split(",")
                        thisSymbol = symbol_parts()
                        thisSymbol.symbol_name = stock_parts[0].strip()
                        thisSymbol.fair_value = stock_parts[1].strip().replace("$", "")
                        with st.spinner(f"Working on {stock_parts[0].strip()}"):
                            thisSymbol.current_price = get_previous_close(stock_parts[0].strip())
                            logging.info(f"The completed stock entry is: {thisSymbol.symbol_name} \n    "
                                         f"Fair Value: {thisSymbol.fair_value} \n    Market Price: {thisSymbol.current_price}")
                            st.session_state["symbols"].append(thisSymbol)
                            symbolsLoaded += 1
                st.write(f"Loaded {symbolsLoaded} Stocks")
                logging.info(f"Loaded {symbolsLoaded} Stocks")
        elif stock_symbol is not None and stock_symbol.strip() != "":
            logging.info("Manually entering a stock")
            with st.spinner("Processing your stock now..."):
                thisSymbol = symbol_parts()
                thisSymbol.symbol_name = stock_symbol.strip()
                thisSymbol.fair_value = stock_value
                thisSymbol.current_price = get_previous_close(stock_symbol.strip())
                st.session_state["symbols"].append(thisSymbol)
        else:
            logging.info("Nothing here")
        st.write(f"Stock loaded, you have a total of {len(st.session_state['symbols'])} stocks loaded.")
        logging.info(f"Stock loaded, you have a total of {len(st.session_state['symbols'])} stocks loaded.")
    if done_click:
        logging.info("Moving to Create Report Processor")
        st.session_state["radio_value"] = 1
        st.rerun()
