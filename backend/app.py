import os
import logging
from dotenv import load_dotenv
from pathlib import Path
from groq import Groq

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PromptGenerator:
    def __init__(self, text: str):
        self.text = text

    def summarize(self) -> str:
        return (
            f"Summarize the following text in 5 bullet points: {self.text}. "
            f"Do not answer anything else just give the summary."
        )
    
    def get_sentiment(self) -> str:
        return (
            f"What is the sentiment of the following text? Positive, Neutral, or Negative, and why? {self.text}. "
            f"Do not answer anything else just answer the question."
        )
    
    def get_insights(self) -> str:
        return (
            f"List 3 key insights or takeaways from this text: {self.text}. "
            f"Do not answer anything else just answer the question."
        )

class ChatClient:
    def __init__(self, api_key: str):
        self.client = Groq(
        api_key=api_key,
    )

    def get_chat_completion(self, text: str, model: str = "llama-3.3-70b-versatile", max_tokens: int = 512) -> str:
        try:
            logging.info("Sending request to chat model...")
            completion = self.client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": text}],
                max_tokens=max_tokens,
            )
            response = completion.choices[0].message.content
            logging.info("Received response from chat model.")
            return response
        except Exception as e:
            logging.exception("Unexpected error during chat completion.")
            return "Error: An unexpected error occurred."

class App:
    def __init__(self):
        dotenv_path = Path('../.env')
        if not dotenv_path.exists():
            logging.warning(f".env file not found at {dotenv_path}")
        load_dotenv(dotenv_path=dotenv_path)

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")
        
        self.chat_client = ChatClient(
            api_key=api_key
        )

    def run(self, text: str):
        prompt_summarize = PromptGenerator(text).summarize()
        prompt_sentiment = PromptGenerator(text).get_sentiment()
        prompt_insights = PromptGenerator(text).get_insights()
        logging.info(f"Generated prompt to summarize: {prompt_summarize}")
        logging.info(f"Generated prompt to get sentiment: {prompt_sentiment}")
        logging.info(f"Generated prompt to get insights: {prompt_insights}")
        summary = self.chat_client.get_chat_completion(prompt_summarize)
        sentiment = self.chat_client.get_chat_completion(prompt_sentiment)
        insights = self.chat_client.get_chat_completion(prompt_insights)
        return summary, sentiment, insights