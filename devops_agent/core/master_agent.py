import asyncio
import os

from agno.knowledge import Knowledge
from devops_agent.utils.model_provider import get_model
from agno.team import Team
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.qdrant import Qdrant
from agno.db.in_memory import InMemoryDb
from agno.db.sqlite import SqliteDb
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.fastembed import FastEmbedEmbedder
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, models

from devops_agent.core.devops_agent import execute_devops_agent
from devops_agent.core.kubernetes_agent import execute_k8s_agent
from devops_agent.core.terraform_agent import execute_terraform_agent
from rich.console import Console
from dotenv import load_dotenv, find_dotenv
from devops_agent.utils.stream_handler import StreamingResponseHandler

load_dotenv(find_dotenv())

console = Console()

try:
    qclient = QdrantClient(url=os.environ.get('QDRANT_URL'), api_key=os.environ.get('QDRANT_API_KEY'))
    if not qclient.collection_exists("devops-memory"):
        qclient.create_collection(collection_name="devops-memory",
                                  vectors_config=VectorParams(size=768, distance=Distance.COSINE))

    # Create vector_db with remote connection
    vector_db = Qdrant(collection="devops-memory",
                       url=os.environ.get('QDRANT_URL'),
                       api_key=os.environ.get('QDRANT_API_KEY'),
                       embedder=FastEmbedEmbedder(id="snowflake/snowflake-arctic-embed-m"))

    # Create knowledge base
    knowledge = Knowledge(vector_db=vector_db)

except Exception as e:
    console.print(f"[yellow]Warning: Could not connect to remote Qdrant, falling back to in-memory mode: {e}[/yellow]")

    # SQLite for content tracking
    contents_db = SqliteDb(db_file="my_knowledge.db")

    # Create Knowledge with SQLite contents DB and ChromaDB
    knowledge = Knowledge(
        name="Basic SDK Knowledge Base",
        description="Agno 2.0 Knowledge Implementation with ChromaDB",
        contents_db=contents_db,
        vector_db=ChromaDb(
            collection="vectors", path="tmp/chromadb", persistent_client=True,
            embedder=FastEmbedEmbedder(id="snowflake/snowflake-arctic-embed-m")
        ),
    )

def execute_master_agent(provider: str, model_str: str, user_query: str = None, debug_mode: bool=False,
                         reasoning:bool=False) -> str:
    # handle model provider uniquely at single place
    model = get_model(provider=provider, model_str=model_str)

    devops_team = Team(
        name="Multi Cloud and Devops Team",
        model=model,
        members=[
            execute_devops_agent(provider=provider, model=model_str, debug_mode=debug_mode, reasoning=reasoning),
            execute_k8s_agent(provider=provider, model=model_str, debug_mode=debug_mode, reasoning=reasoning),
            execute_terraform_agent(provider=provider, model=model_str, debug_mode=debug_mode, reasoning=reasoning),
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
    # response = devops_team.run(user_query, stream_intermediate_steps=True, retry=3)

    handler = StreamingResponseHandler(
        console=console,
        show_message=True,
        show_reasoning=True,
        show_tool_calls=True,
        show_member_responses=True,
        markdown=True
    )

    # Assuming you have a team object
    handler.handle_stream(devops_team, input=user_query)

    response = handler.response_content

    # saved the response to knowledge in async mode
    asyncio.run(
        knowledge.add_content_async(text_content=f"question: {user_query}, Assistant: {response}",
                                    skip_if_exists=True))
    return response
