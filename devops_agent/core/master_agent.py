import asyncio
import os
from pathlib import Path
from typing import Any

from agno.knowledge import Knowledge
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google.gemini import Gemini
from agno.team import Team
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.qdrant import Qdrant
from agno.db.in_memory import InMemoryDb
from agno.knowledge.embedder.fastembed import FastEmbedEmbedder
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance

from devops_agent.core.devops_agent import execute_devops_agent
from devops_agent.core.kubernetes_agent import execute_k8s_agent
from devops_agent.core.terraform_agent import execute_terraform_agent

from rich.console import Console

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

console = Console()

qclient = QdrantClient(url=os.environ.get('QDRANT_URL'), api_key=os.environ.get('QDRANT_API_KEY'))
if not qclient.collection_exists("devops-memory"):
    qclient.create_collection(collection_name="devops-memory",
                              vectors_config=VectorParams(size=768, distance=Distance.COSINE))

vector_db = Qdrant(collection="devops-memory", url=os.environ.get('QDRANT_URL'),
                   api_key=os.environ.get('QDRANT_API_KEY'),
                   embedder=FastEmbedEmbedder(id="snowflake/snowflake-arctic-embed-m"))

# Create knowledge base
knowledge = Knowledge(vector_db=vector_db)


def execute_master_agent(provider: str, user_query: str = None, log_file: Path = None) -> str:
    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id="gpt-5-mini", api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id="claude-sonnet-4-5-20250929", temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id="gemini-2.5-flash", temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    else:
        model = OpenAIChat(id="gpt-5-mini"),  # default

    devops_team = Team(
        name="Multi Cloud and Devops Team",
        model=model,
        members=[
            execute_devops_agent(provider=provider),
            execute_k8s_agent(provider=provider),
            execute_terraform_agent(provider=provider)
        ],
        instructions=[
            "You are a intelligent router that directs questions to the appropriate agent.",
            "If the user asks in a non devops or k8s question whose agent is not a team member, respond in English with:",
            "'I can only answer in the following technologies: Devops, terraform & Kubernetes Architecture on Multiple clouds. Please ask your question in one of these technologies.'",
            "Always check the technology or domain of the user's input before routing to an agent.",
            "For unsupported technologies like coding, flowcharts, analytics etc respond in English with the above message.",
        ],
        tools=[ReasoningTools()],  # Enable reasoning capabilities
        knowledge=knowledge,
        db=InMemoryDb(),
        respond_directly=True,  # if set to true the member response is directly given to user
        determine_input_for_members=False,
        delegate_task_to_all_members=False,
        stream_intermediate_steps=True,
        add_knowledge_to_context=True,
        add_datetime_to_context=True,
        add_session_summary_to_context=True,
        show_members_responses=True,
        share_member_interactions=True,
        enable_agentic_memory=True,
        markdown=True
    )
    response = devops_team.run(user_query, stream_intermediate_steps=True, retry=3)

    # saved the response to knowledge in async mode
    asyncio.run(
        knowledge.add_content_async(text_content=f"question: {user_query}, Assistant: {response.content}",
                                    skip_if_exists=False,
                                    metadata={"agent_id": response.team_id, "session_id": response.session_id,
                                              "run_id": response.run_id})
    )

    return response.content
