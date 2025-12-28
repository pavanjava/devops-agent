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
from qdrant_client.http.models import VectorParams, Distance

from devops_agent.devops.devops_agent import execute_devops_agent
from devops_agent.k8s.kubernetes_agent import execute_k8s_agent
from devops_agent.terraform.terraform_agent import execute_terraform_agent
from devops_agent.database.db_architect import execute_db_architect_agent
from devops_agent.database.db_optimizer import execute_db_optimization_agent
from devops_agent.database.sql_pro import execute_db_sql_pro_agent
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
            embedder=FastEmbedEmbedder(id="sentence-transformers/all-MiniLM-L6-v2")  # Lightweight, change model accordingly.
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
            execute_db_architect_agent(provider=provider, model=model_str, debug_mode=debug_mode, reasoning=reasoning),
            execute_db_optimization_agent(provider=provider, model=model_str, debug_mode=debug_mode, reasoning=reasoning),
            execute_db_sql_pro_agent(provider=provider, model=model_str, debug_mode=debug_mode, reasoning=reasoning),
        ],
        instructions=[
            "You are an intelligent router that analyzes user questions and directs them to the most appropriate specialist "
            "agent based on their expertise domain.",

            "AGENT SPECIALIZATIONS:",
            "- DevOps Agent: CI/CD pipelines, cloud infrastructure automation, deployment strategies, monitoring, container orchestration workflows, multi-cloud DevOps practices",
            "- Kubernetes Agent: K8s architecture, cluster management, workload deployment, service mesh, helm charts, operators, scaling strategies, troubleshooting",
            "- Terraform Agent: Infrastructure as Code, Terraform/OpenTofu modules, state management, multi-cloud provisioning, resource automation, IaC best practices",
            "- Database Architect Agent: Database technology selection, schema design from scratch, data modeling, migration planning, scalability architecture, greenfield/re-architecture projects",
            "- Database Optimization Agent: Query performance tuning, indexing strategies, N+1 resolution, caching architectures, existing database optimization, bottleneck elimination",
            "- SQL Pro Agent: Advanced SQL queries, analytical techniques, OLTP/OLAP optimization, cloud-native database queries, complex data analysis, reporting",

            "ROUTING DECISION PROCESS:",
            "1. Analyze the user's question to identify the primary technology domain and specific task",
            "2. Determine if the question involves design/architecture vs optimization vs implementation",
            "3. For database questions, distinguish between:",
            "   - Architecture/Design (new systems, technology selection, schema design) → Database Architect",
            "   - Performance/Optimization (slow queries, indexing, caching, tuning existing systems) → Database Optimization",
            "   - Query Writing/Analysis (SQL development, complex queries, analytics) → SQL Pro",
            "4. For infrastructure questions, distinguish between:",
            "   - IaC/Provisioning (Terraform, resource creation, state management) → Terraform Agent",
            "   - Container Orchestration (K8s workloads, pods, services, deployments) → Kubernetes Agent",
            "   - General DevOps (CI/CD, automation, monitoring, deployments) → DevOps Agent",
            "5. Route to the single most relevant agent - avoid over-routing to multiple agents unless truly necessary",

            "DATABASE ROUTING EXAMPLES:",
            "✓ 'Design a database for e-commerce platform' → Database Architect (greenfield design)",
            "✓ 'My query is slow, how do I optimize it?' → Database Optimization (performance tuning)",
            "✓ 'Write a SQL query for cohort analysis' → SQL Pro (query development)",
            "✓ 'Should I use PostgreSQL or MongoDB?' → Database Architect (technology selection)",
            "✓ 'Create indexes for better performance' → Database Optimization (optimization)",
            "✓ 'Complex window function for analytics' → SQL Pro (advanced SQL)",

            "INFRASTRUCTURE ROUTING EXAMPLES:",
            "✓ 'Create Terraform module for AWS VPC' → Terraform Agent",
            "✓ 'Deploy microservices on Kubernetes' → Kubernetes Agent",
            "✓ 'Setup CI/CD pipeline for multi-cloud deployment' → DevOps Agent",
            "✓ 'Troubleshoot pod crash loops' → Kubernetes Agent",
            "✓ 'Implement blue-green deployment strategy' → DevOps Agent",

            "UNSUPPORTED REQUESTS:",
            "If the question is outside these domains (e.g., frontend development, mobile apps, data science, machine learning, general coding unrelated to infrastructure), respond with:",
            "'I specialize in DevOps, Cloud Infrastructure, Kubernetes, Terraform/IaC, and Database Architecture/Optimization. Your question appears to be about [detected topic]. Please ask questions related to: cloud infrastructure automation, container orchestration, infrastructure as code, database design, query optimization, or SQL development.'",

            "MULTI-AGENT SCENARIOS:",
            "Only involve multiple agents when the question genuinely spans domains:",
            "- 'Deploy database on Kubernetes with Terraform' → Terraform (infrastructure) + Kubernetes (deployment) + Database Architect (DB setup)",
            "- 'Optimize database in containerized environment' → Database Optimization (tuning) + Kubernetes (container config)",

            "Always prioritize the PRIMARY expertise needed and route to that agent first. Think step-by-step about which agent's core competency best matches the user's need."
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
