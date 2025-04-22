import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms.base import LLM
from langchain_groq import ChatGroq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PromptChains:
    def __init__(self, llm: LLM):
        self.llm = llm
        self.summary_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(
                "Summarize the following text in 5 bullet points: {text}. Do not answer anything else just give the summary."
            )
        )
        self.sentiment_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(
                "What is the sentiment of the following text? Positive, Neutral, or Negative, and why? {text}. Do not answer anything else just answer the question."
            )
        )
        self.insight_chain = LLMChain(
            llm=self.llm,
            prompt=PromptTemplate.from_template(
                "List 3 key insights or takeaways from this text: {text}. Do not answer anything else just answer the question."
            )
        )
    
    def run_all(self, text: str):
        return (
            self.summary_chain.run({"text": text}),
            self.sentiment_chain.run({"text": text}),
            self.insight_chain.run({"text": text})
        )
        
class App:
    def __init__(self):
        dotenv_path = Path('../.env')
        load_dotenv(dotenv_path=dotenv_path)
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found.")

        # Hypothetical LangChain Groq wrapper
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            api_key=api_key
        )
        self.chains = PromptChains(llm=self.llm)

    def run(self, text: str):
        summary, sentiment, insights = self.chains.run_all(text)
        return summary, sentiment, insights