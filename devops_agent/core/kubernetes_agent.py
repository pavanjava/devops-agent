import asyncio
import os
from textwrap import dedent

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

k8s_prompt = prompt_from_poml('kubernetes.poml')

# qclient = QdrantClient(url=os.environ.get('QDRANT_URL'), api_key=os.environ.get('QDRANT_API_KEY'))
# if not qclient.collection_exists("devops-memory"):
#     qclient.create_collection(collection_name="devops-memory",
#                               vectors_config=VectorParams(size=768, distance=Distance.COSINE))
#
# vector_db = Qdrant(collection="devops-memory", url=os.environ.get('QDRANT_URL'),
#                    api_key=os.environ.get('QDRANT_API_KEY'),
#                    embedder=FastEmbedEmbedder(id="snowflake/snowflake-arctic-embed-m"))
#
# # Create knowledge base
# knowledge = Knowledge(vector_db=vector_db)

console = Console()

def execute_k8s_agent(provider: str, user_query: str = None) -> Agent:

    console.print(Panel.fit(
        "[bold cyan]Kubernetes Agent Invoking...[/bold cyan]",
        border_style="cyan"
    ))

    llm_provider = provider.lower().strip()
    if llm_provider == 'openai':
        model = OpenAIChat(id="gpt-4o", api_key=os.environ.get('OPENAI_API_KEY'))
    elif llm_provider == 'anthropic':
        model = Claude(id="claude-sonnet-4-5-20250929", temperature=0.6, api_key=os.environ.get('ANTHROPIC_API_KEY'))
    elif llm_provider == 'google':
        model = Gemini(id="gemini-2.5-flash", temperature=0.6, api_key=os.environ.get('GEMINI_API_KEY'))
    else:
        model = OpenAIChat(id="gpt-5-mini"),  # default

    k8s_assist = Agent(
        name="Kubernetes Agent",
        model=model,
        description="You help answer questions about the application with kubernetes design and implementation domain of any infrastructure like Azure(AKS), AWS(EKS), and GCP(GKS)",
        instructions=k8s_prompt,
        additional_input=dedent("""\
        Instruction: You should always answer scenarios like below (few examples as below).
        - Design a multi-cluster Kubernetes platform with GitOps for a financial services company
        - Implement progressive delivery with Argo Rollouts and service mesh traffic splitting
        - Create a secure multi-tenant Kubernetes platform with namespace isolation and RBAC
        - Design disaster recovery for stateful applications across multiple Kubernetes clusters
        - Optimize Kubernetes costs while maintaining performance and availability SLAs
        - Implement observability stack with Prometheus, Grafana, and OpenTelemetry for microservices
        - Create CI/CD pipeline with GitOps for container applications with security scanning
        - Design Kubernetes operator for custom application lifecycle management
        """),
        stream_intermediate_steps=True,
        markdown=True,
    )

    # response = k8s_assist.run(user_query, stream_intermediate_steps=True, retry=3)
    #
    # asyncio.run(
    #     knowledge.add_content_async(text_content=response.content,
    #                                 metadata={"agent_id": response.agent_id, "session_id": response.session_id})
    # )
    # return response.content

    return k8s_assist
