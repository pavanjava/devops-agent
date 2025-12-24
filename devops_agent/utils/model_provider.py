from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.openai import OpenAIChat, OpenAILike
from agno.models.ollama import Ollama
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


def get_model(provider: str, model_str: str, ollama_base_url: str = None, vllm_base_url: str = None, ):
    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id=model_str, api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id=model_str, temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id=model_str, temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    elif llm_provider == 'ollama':
        if os.environ.get('OLLAMA_API_KEY') is not None:
            model = Ollama(id=model_str, host=ollama_base_url, api_key=os.environ.get('OLLAMA_API_KEY'))
        else:
            model = Ollama(id=model_str, host=ollama_base_url)
    elif llm_provider == 'vllm':
        if os.environ.get('VLLM_API_KEY') is not None:
            model = OpenAILike(id=model_str, base_url=vllm_base_url, api_key=os.environ.get('VLLM_API_KEY'))
        else:
            model = OpenAILike(id=model_str, base_url=vllm_base_url)
    else:
        model = OpenAIChat(id=model_str, api_key=os.environ.get('OPENAI_API_KEY')),  # default

    return model