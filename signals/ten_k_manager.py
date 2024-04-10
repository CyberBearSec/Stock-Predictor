from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
from langchain_community.document_loaders import TextLoader
import logging
import os
import os.path
import requests
import streamlit as st
from utility.utilities import symbol_parts


def grab_10K_data(symbol: str) -> None:
    url = "https://last10k-company-v1.p.rapidapi.com/v1/company/items"
    querystring = {"ticker": symbol}
    headers = {
        "ticker": symbol,
        "X-RapidAPI-Key": os.environ["RAPID_API_KEY"],
        "X-RapidAPI-Host": "last10k-company-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    jsonDoc = response.json()
    with open(f"./signals/10k/{symbol}-10K.txt", "w", encoding="utf-8") as f:
        json.dump(jsonDoc, f, ensure_ascii=False, indent=4)


def load_10K_report(symbol: str):
    loader = TextLoader(f"./signals/10k/{symbol}-10K.txt", encoding='iso-8859-1')
    return loader.load()

def load_10K_report_as_json(symbol: str) -> json:
    with open(f"./signals/10k/{symbol}-10K.txt", encoding='iso-8859-1') as f:
        data = json.load(f)
    return data


def download_10k_reports(currentSymbols: [symbol_parts]):
    with st.spinner(f"Downloading 10K reports for each stock..."):
        loadSymbols = []
        for thisSymbol in currentSymbols:
            with st.spinner(f"Looking for the 10K report for {thisSymbol.symbol_name}..."):
                foundIt = False
                try:
                    # These are annual reports so we really do not need to check for a new one for 11 months
                    if os.path.exists(f"./signals/10k/{thisSymbol}-10K.txt"):
                        with open(f"./signals/10k/{thisSymbol}-10K.txt") as f:
                            jsonDoc = json.load(f)
                            fileDate = datetime.strptime(jsonDoc["data"]["filing"]["filingDate"], '%m/%d/%y')
                            if datetime.now() > (fileDate + relativedelta(months=11)):
                                grab_10K_data(thisSymbol.symbol_name)
                    else:
                        grab_10K_data(thisSymbol.symbol_name)
                    loadSymbols.append(thisSymbol.symbol_name)
                    foundIt = True
                except Exception as exc:
                    logging.error(f"Error retrieving {thisSymbol.symbol_name} 10K report.  Error: {exc.__traceback__}")
                    foundIt = False
                if not foundIt:
                    st.error(f"Unable to find 10K report for {thisSymbol.symbol_name}")
