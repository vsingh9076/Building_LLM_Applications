"""
This script ingests text documents into a vector store for efficient retrieval and semantic search.

It leverages the LangChain library for text splitting, embedding generation, and vector store creation.
"""

import shutil
import box
import yaml
import warnings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings

warnings.filterwarnings("ignore", category=DeprecationWarning)  # Ignore deprecated warnings


def run_ingest(documents):
    """
    Ingests the provided documents into a LangChain vector store.

    Args:
        documents: A list of text documents to be ingested.
    """

    # Load configuration variables from a YAML file
    with open('config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))

    # Split text into manageable chunks for embedding generation
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=cfg.CHUNK_SIZE,
        chunk_overlap=cfg.CHUNK_OVERLAP
    )
    splits = text_splitter.split_text(documents)
    texts = text_splitter.create_documents(splits)
    print(f"Loaded {len(texts)} splits")

    # Create embeddings using a Hugging Face model
    embeddings = HuggingFaceEmbeddings(
        model_name=cfg.EMBEDDINGS,
        model_kwargs={'device': cfg.DEVICE},
        encode_kwargs={'normalize_embeddings': cfg.NORMALIZE_EMBEDDINGS}
    )

    # Create or clear the vector store directory
    shutil.rmtree(cfg.VECTOR_DB, ignore_errors=True)
    print(f'{cfg.VECTOR_DB} : Folder Deleted')

    # Build the vector store using LangChain's Chroma
    vector_store = Chroma.from_documents(
        texts,
        embeddings,
        collection_name=cfg.COLLECTION_NAME,
        collection_metadata={"hnsw:space": cfg.VECTOR_SPACE},  # Configure HNSW indexing
        persist_directory=cfg.VECTOR_DB
    )

    print(f"Vector store created at {cfg.VECTOR_DB}")


if __name__ == "__main__":
    # Run the ingestion process when executed as a script
    run_ingest()


