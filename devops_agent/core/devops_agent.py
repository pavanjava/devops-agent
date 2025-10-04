import asyncio
import os

from agno.agent import Agent
from agno.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google.gemini import Gemini
from agno.vectordb.qdrant import Qdrant
from agno.knowledge.embedder.fastembed import FastEmbedEmbedder
from qdrant_client.http.models import VectorParams, Distance
from rich.console import Console
from rich.panel import Panel

from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml
from qdrant_client.qdrant_client import QdrantClient

devops_prompt = prompt_from_poml('devops.poml')

# qclient = QdrantClient(url=os.environ.get('QDRANT_URL'), api_key=os.environ.get('QDRANT_API_KEY'))
# if not qclient.collection_exists("devops-memory"):
#     qclient.create_collection(collection_name="devops-memory", vectors_config=VectorParams(size=768, distance=Distance.COSINE))
#
# vector_db = Qdrant(collection="devops-memory", url=os.environ.get('QDRANT_URL'),
#                    api_key=os.environ.get('QDRANT_API_KEY'),
#                    embedder=FastEmbedEmbedder(id="snowflake/snowflake-arctic-embed-m"))
#
# # Create knowledge base
# knowledge = Knowledge(vector_db=vector_db)

console = Console()

def execute_devops_agent(provider: str, user_query: str = None) -> Agent:
    console.print(Panel.fit(
        "[bold cyan]DevOps Agent Executing...[/bold cyan]",
        border_style="cyan"
    ))
    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id="gpt-5-mini", api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id="claude-sonnet-4-5-20250929", temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id="gemini-2.5-flash", temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    else:
        model = OpenAIChat(id="gpt-5-mini"), #default

    devops_assist = Agent(
        name="DevOps Agent",
        model=model,
        description="You help answer questions about the devops domain.",
        instructions=devops_prompt,
        # knowledge=knowledge,
        # stream_intermediate_steps=True,
        # add_knowledge_to_context=True,
        # add_datetime_to_context=True,
        # add_session_summary_to_context=True,
        markdown=True,
    )

    # response = devops_assist.run(user_query, stream_intermediate_steps=True, retry=3)
    #
    # asyncio.run(
    #     knowledge.add_content_async(text_content=response.content, metadata={"agent_id": response.agent_id, "session_id": response.session_id})
    # )
    # return response.content

    return devops_assist