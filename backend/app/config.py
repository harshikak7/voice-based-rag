import os

from dotenv import load_dotenv


# Load .env
load_dotenv()


# =========================================================
# OLLAMA CONFIGURATION
# =========================================================

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "llama3.2"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "nomic-embed-text"
)


# =========================================================
# WHISPER CONFIGURATION
# =========================================================

WHISPER_MODEL = os.getenv(
    "WHISPER_MODEL",
    "base"
)

WHISPER_DEVICE = os.getenv(
    "WHISPER_DEVICE",
    "cpu"
)

WHISPER_COMPUTE_TYPE = os.getenv(
    "WHISPER_COMPUTE_TYPE",
    "int8"
)


# =========================================================
# CHROMADB
# =========================================================

CHROMA_PATH = os.getenv(
    "CHROMA_PATH",
    "./chroma_db"
)

COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "voice_rag_documents"
)


# =========================================================
# FOLDERS
# =========================================================

DOCUMENTS_PATH = os.getenv(
    "DOCUMENTS_PATH",
    "./documents"
)

TEMP_PATH = os.getenv(
    "TEMP_PATH",
    "./temp"
)


# =========================================================
# RAG SETTINGS
# =========================================================

CHUNK_SIZE = int(
    os.getenv(
        "CHUNK_SIZE",
        "1000"
    )
)

CHUNK_OVERLAP = int(
    os.getenv(
        "CHUNK_OVERLAP",
        "200"
    )
)

TOP_K = int(
    os.getenv(
        "TOP_K",
        "5"
    )
)