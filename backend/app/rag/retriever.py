import requests

import chromadb

from app.config import (
    OLLAMA_URL,
    EMBEDDING_MODEL,
    CHROMA_PATH,
    COLLECTION_NAME,
    TOP_K
)


# =========================================================
# CHROMADB
# =========================================================

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = (
    chroma_client.get_or_create_collection(
        name=COLLECTION_NAME
    )
)


# =========================================================
# EMBEDDING
# =========================================================

def create_embedding(
    text: str
):

    response = requests.post(
        f"{OLLAMA_URL}/api/embed",
        json={
            "model": EMBEDDING_MODEL,
            "input": text
        },
        timeout=120
    )


    response.raise_for_status()


    data = response.json()


    embeddings = data.get(
        "embeddings"
    )

    if not embeddings:

        raise RuntimeError(
            "Ollama embedding failed."
        )

    embedding = embeddings[0]

    if len(embedding) != 768:

        raise RuntimeError(
            f"Expected 768-dimensional embedding "
            f"from {EMBEDDING_MODEL}, "
            f"but got {len(embedding)} dimensions."
        )

    return embedding


# =========================================================
# RETRIEVE DOCUMENTS
# =========================================================

def retrieve_documents(
    query: str,
    number_of_results: int = TOP_K
):

    # No documents
    if collection.count() == 0:

        return [], []


    # Convert query into embedding
    query_embedding = create_embedding(
        query
    )


    # Search ChromaDB
    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=number_of_results
    )


    documents = results.get(
        "documents",
        [[]]
    )[0]


    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]


    return (
        documents,
        metadatas
    )


# =========================================================
# BUILD CONTEXT
# =========================================================

def build_context(
    documents,
    metadatas
):

    context_parts = []


    for document, metadata in zip(
        documents,
        metadatas
    ):

        source = metadata.get(
            "source",
            "Unknown"
        )


        chunk = metadata.get(
            "chunk",
            "Unknown"
        )


        context_parts.append(
            f"""
SOURCE: {source}

CHUNK: {chunk}

{document}
"""
        )


    return "\n\n".join(
        context_parts
    )