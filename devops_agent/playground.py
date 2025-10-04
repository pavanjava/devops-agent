from devops_agent.core.master_agent import execute_master_agent
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

if __name__ == '__main__':
    execute_master_agent(provider="openai", user_query="Analyze distributed tracing data to identify performance bottleneck in microservices architecture")