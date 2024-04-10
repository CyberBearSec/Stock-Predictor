import os
import google.generativeai as genai

def retrieve_10k_from_gemini(symbol: str) -> str:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Provide just the URL for the latest 10k report from SEC.gov for AAPL")
    return response.text