from poml import poml
import os

def prompt_from_poml(poml_file: str) -> str:
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the path to the prompts directory
    prompts_path = os.path.join(script_dir, '..', 'prompts', poml_file)

    with open(prompts_path, 'r') as f:
        markup = f.read()

    devops_prompt = poml(markup=markup, format="message_dict", chat=True)

    # === Step 2: Extract prompt text ===
    if isinstance(devops_prompt, list):
        full_prompt = "\n".join([msg.get("content", "") for msg in devops_prompt])
    else:
        full_prompt = str(devops_prompt)

    return full_prompt

