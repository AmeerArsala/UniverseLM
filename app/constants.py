from sentence_transformers import SentenceTransformer


# Options
# gpt-4-turbo-2024-04-09
# gpt-3.5-turbo-0125
# gpt-3.5-turbo-instruct
OPENAI_MODEL = "gpt-4-turbo-2024-04-09"
HF_MODEL = "mistralai/Mixtral-8x7B-Instruct-v0.1"
TEMP = 0.75
K_NEIGHBORS = 5


# For semantic search; might not be needed but who gives af!!! I like it!
encoder_repo_id: str = "all-MiniLM-L6-v2"
encoder = SentenceTransformer(encoder_repo_id)
