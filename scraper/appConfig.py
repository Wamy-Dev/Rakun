from dotenv import load_dotenv
import os
load_dotenv()


MONGODB_CONNECTION_URI = os.getenv("MONGODB_CONNECTION_URI")
MEILISEARCH_API_KEY = os.getenv("MEILISEARCH_API_KEY")
MEILISEARCH_HOST = os.getenv("MEILISEARCH_HOST")
