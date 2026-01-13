"""Configuration de l'application Khôlleur AI."""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR
EXERCICES_DIR = DATA_DIR / "exercices"
CHROMA_DIR = BASE_DIR / "chroma_db"

# Files
QUESTIONS_FILE = DATA_DIR / "questions_cours_kholle_mpsi_final.json"
GRAPH_FILE = DATA_DIR / "graph.json"
COURS_DIR = DATA_DIR / "cours"

# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ChromaDB Collections
COLLECTION_QUESTIONS = "questions_cours"
COLLECTION_EXERCICES = "exercices"
COLLECTION_COURS = "cours_chunks"

# Gemini Model
GEMINI_MODEL = "gemini-3-flash-preview"
EMBEDDING_MODEL = "models/text-embedding-004"

