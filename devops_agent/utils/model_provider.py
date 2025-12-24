from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


def get_model(provider: str, model_str: str):
    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id=model_str, api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id=model_str, temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id=model_str, temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    else:
        model = OpenAIChat(id=model_str, api_key=os.environ.get('OPENAI_API_KEY')),  # default

    return model