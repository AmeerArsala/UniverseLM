import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
import torch


# Load .env file
load_dotenv()


if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print("Using CUDA")
else:
    DEVICE = torch.device("cpu")
    print("Using CPU")


# Options
# gpt-4-turbo-2024-04-09
# gpt-3.5-turbo-0125
# gpt-3.5-turbo-instruct
OPENAI_MODEL = "gpt-4-turbo-2024-04-09"
HF_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
TEMP = 0.75
K_NEIGHBORS = 5

OPENAI_EMBEDDINGS_MODEL = "text-embedding-ada-002"


# For semantic search; might not be needed but who gives af!!! I like it!
HF_ENCODER_REPO_ID = "all-MiniLM-L6-v2"
encoder = SentenceTransformer(HF_ENCODER_REPO_ID)
