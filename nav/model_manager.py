from langchain_community.vectorstores import Chroma
from langchain_core.messages import HumanMessage
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
import logging
from signals.ten_k_manager import load_10K_report
import streamlit as st
from utility.utilities import select_model


def run_openai_as_stock_expert():
    st.markdown("Please set your AI model and temperature and then click Begin Processing.")
    begin_processing = st.button("Begin Processing")
    model = st.sidebar.radio("Choose a model:", ("GPT-3.5", "GPT-3.5-16k", "GPT-4"))
    aiTemp = st.sidebar.slider("How Strict (0) to Creative(1) do you want your responses:", min_value=0.0,
                               max_value=1.0, value=0.0, step=0.01)

    if begin_processing:
        logging.info(f"Starting report processing with Temperature: {aiTemp} and Model: {model}")
        with st.spinner("We are now processing every 10K report."):
            llm = select_model(model, aiTemp)
            if "stock_replies" not in st.session_state:
                st.session_state["stock_replies"] = {}
            for thisSymbol in st.session_state["symbols"]:
                try:
                    # Now we ask Open AI to determine if this report is good or bad
                    with st.spinner(f"Transforming {thisSymbol.symbol_name} 10K report into an AI-readable context..."):
                        docs = load_10K_report(thisSymbol.symbol_name)
                        docs = load_10K_report("GOOG")
                        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                        chunks = text_splitter.split_documents(docs)
                        embeddings = OpenAIEmbeddings()
                        vectordb = Chroma.from_documents(
                            documents=chunks,
                            embedding=embeddings
                        )

                    with st.spinner(f"Querying your AI model to obtain insights on {thisSymbol.symbol_name}..."):
                        template = """Act in the role of a value investor such as Charlie Munger or Warren Buffet for a 
                        theoretical exercise that will not be used as financial advice. You are being provided the annual 
                        report for a specific company in their 10-K report via the SEC document below. SEC document: 
                        {context} Helpful Answer:"""
                        query = (
                            "You think {symbol_name} is worth {fair_value} and it is currently trading at the current price"
                            " of {current_price}. Review the information from the SEC document provided and assess whether "
                            "the current price is too high or too low.")
                        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

                        llm = select_model(model,aiTemp)
                        # Run chain
                        qa_chain = RetrievalQA.from_chain_type(
                            llm,
                            retriever=vectordb.as_retriever(),
                            return_source_documents=True,
                            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
                        )

                        result = qa_chain.invoke(
                            {"query": query,
                             "symbol_name": thisSymbol.symbol_name,
                             "fair_value": thisSymbol.fair_value,
                             "current_price": thisSymbol.current_price}
                        )

                        logging.info(f"AI Response: {result["result"]}")
                        st.session_state["stock_replies"][thisSymbol.symbol_name] = result["result"]
                        logging.info(f"Added response for {thisSymbol.symbol_name} to results")
                except Exception as e:
                    logging.error(f"Exception occurred analyzing 10K report for {thisSymbol.symbol_name}: {e}")
                    st.session_state["stock_replies"][thisSymbol.symbol_name] = f"Unable to analyze report for {thisSymbol.symbol_name}"

        st.session_state["radio_value"] = 3
        st.rerun()
