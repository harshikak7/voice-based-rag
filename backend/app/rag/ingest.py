import os

import requests

import chromadb

from pypdf import PdfReader

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from app.config import (
    OLLAMA_URL,
    EMBEDDING_MODEL,
    CHROMA_PATH,
    COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP
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
# CREATE EMBEDDING
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
            "Ollama did not return an embedding."
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
# EXTRACT PDF TEXT
# =========================================================

def extract_pdf_text(
    file_path: str
):

    reader = PdfReader(
        file_path
    )


    pages = []


    for page_number, page in enumerate(
        reader.pages,
        start=1
    ):

        text = page.extract_text()


        if text:

            pages.append(
                f"""
[Page {page_number}]

{text}
"""
            )


    return "\n".join(
        pages
    )


# =========================================================
# CREATE CHUNKS
# =========================================================

def create_chunks(
    text: str
):

    splitter = (
        RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )
    )


    return splitter.split_text(
        text
    )


# =========================================================
# INGEST PDF
# =========================================================

def ingest_pdf(
    file_path: str
):

    filename = os.path.basename(
        file_path
    )


    print(
        f"Reading PDF: {filename}"
    )


    # Extract text
    text = extract_pdf_text(
        file_path
    )


    if not text.strip():

        raise ValueError(
            "No readable text found in PDF."
        )


    # Create chunks
    chunks = create_chunks(
        text
    )


    if not chunks:

        raise ValueError(
            "Could not create document chunks."
        )


    ids = []

    embeddings = []

    documents = []

    metadatas = []


    # Create embeddings
    for index, chunk in enumerate(
        chunks
    ):

        print(
            f"Embedding chunk "
            f"{index + 1}/{len(chunks)}"
        )


        chunk_id = (
            f"{filename}-{index}"
        )


        embedding = create_embedding(
            chunk
        )


        ids.append(
            chunk_id
        )


        embeddings.append(
            embedding
        )


        documents.append(
            chunk
        )


        metadatas.append({
            "source": filename,
            "chunk": index
        })


    # Store in ChromaDB
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas
    )


    print(
        f"Successfully indexed "
        f"{len(chunks)} chunks."
    )


    return {
        "filename": filename,
        "chunks": len(chunks)
    }