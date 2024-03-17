from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.llms import Ollama
import box
import yaml
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def load_embedding_model(model_name, normalize_embedding=True, device='cpu'):
    """
    Loads a Hugging Face embedding model.

    Args:
        model_name (str): Name of the Hugging Face model to load (e.g., "sentence-transformers/all-mpnet-base-v2").
        normalize_embedding (bool, optional): Whether to normalize the embeddings during encoding. Defaults to True.
        device (str, optional): Device to use for model inference (e.g., "cpu" or "cuda"). Defaults to "cpu".

    Returns:
        HuggingFaceEmbeddings: The loaded embedding model.
    """

    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs={'device': device},
        encode_kwargs={
            'normalize_embeddings': normalize_embedding
        }
    )


def load_retriever(embeddings, store_path, collection_name, vector_space, num_results=1):
    """
    Loads a retriever from a Chroma vector store.

    Args:
        embeddings (HuggingFaceEmbeddings): The embedding model to use for encoding documents.
        store_path (str): Path to the directory where the vector store persists data.
        collection_name (str): Name of the collection within the vector store.
        vector_space (str): Type of vector space used in the collection (e.g., "hnsw").
        num_results (int, optional): Number of documents to retrieve for each query. Defaults to 1.

    Returns:
        RetrievalQA: The loaded retriever.
    """

    vector_store = Chroma(collection_name=collection_name,
                          persist_directory=store_path,
                          collection_metadata={"hnsw:space": vector_space},
                          embedding_function=embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": num_results})

    return retriever


def load_prompt_template():
    """
    Loads a PromptTemplate object for guiding the large language model during retrieval-based QA.

    Returns:
        PromptTemplate: The loaded prompt template.
    """

    template = """Use the following pieces of information to answer the user's question.
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    Context: {context}
    Question: {question}

    Only return the helpful answer below and nothing else.
    Helpful answer:
    """

    prompt = PromptTemplate.from_template(template)

    return prompt


def load_qa_chain(retriever, llm, prompt):
    """
    Loads a RetrievalQA chain for performing retrieval-based question answering.

    Args:
        retriever (RetrievalQA): The retriever to use for retrieving relevant documents.
        llm (Ollama): The large language model to use for answering the question.
        prompt (PromptTemplate): The prompt template to guide the LLM.

    Returns:
        RetrievalQA: The loaded QA chain.
    """
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
        return_source_documents=True,
        chain_type_kwargs={'prompt': prompt}
    )


def build_rag_pipeline():
    
    # Import config vars
    with open('config.yml', 'r', encoding='utf8') as ymlfile:
        cfg = box.Box(yaml.safe_load(ymlfile))

    print("Loading embedding model...")
    embeddings = load_embedding_model(model_name=cfg.EMBEDDINGS,
                                      normalize_embedding=cfg.NORMALIZE_EMBEDDINGS,
                                      device=cfg.DEVICE)

    print("Loading vector store and retriever...")
    retriever = load_retriever(embeddings,
                               cfg.VECTOR_DB,
                               cfg.COLLECTION_NAME,
                               cfg.VECTOR_SPACE,
                               cfg.NUM_RESULTS)

    print("Loading prompt template...")
    prompt = load_prompt_template()

    print("Loading Ollama...")
    llm = Ollama(model=cfg.LLM, verbose=False, temperature=0)

    print("Loading QA chain...")
    qa_chain = load_qa_chain(retriever, llm, prompt)

    return qa_chain


