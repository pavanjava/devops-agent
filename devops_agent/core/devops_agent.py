from devops_agent.utils.prompt_generator_from_poml import prompt_from_poml

devops_prompt = prompt_from_poml('devops.poml')

def execute_devops_agent(user_query: str) -> str:
    pass