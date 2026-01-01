from datasets import Dataset
import json

# Load your JSONL file
data = []
with open('dataset.jsonl', 'r') as f:
    for line in f:
        data.append(json.loads(line))

# Create a Dataset object
dataset = Dataset.from_list(data)

# Push to Hugging Face
dataset.push_to_hub("pavanmantha/devops-v1")