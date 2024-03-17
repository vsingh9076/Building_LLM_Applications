import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from rag.pipeline import build_rag_pipeline
from main import get_rag_response
import timeit
from htmlTemplates import css  # Assuming css contains CSS styles for formatting

from ingest import run_ingest


def get_pdf_text(pdf_docs: list[str]) -> str:
    """
    Extracts text content from a list of PDF documents.

    Args:
        pdf_docs: A list of file paths or data objects representing the PDF documents.

    Returns:
        A string containing the combined text content of all PDFs.
    """

    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def handle_userinput(user_question: str) -> None:
    """
    Processes user input and retrieves an answer using a RAG (Reader-Answer Generator) pipeline.

    Args:
        user_question: The user's question about the uploaded documents.

    Returns:
        None (modifies Streamlit app state with the answer and processing time).
    """

    start = timeit.default_timer()

    qa_chain = build_rag_pipeline()
    answer = get_rag_response(user_question, qa_chain)

    end = timeit.default_timer()

    st.write(answer)
    st.markdown(f"**Time to retrieve answer:** {end - start:.2f} seconds", unsafe_allow_html=True)


def main() -> None:
    """
    The main function of the Streamlit application.

    Loads environment variables, configures the Streamlit app layout,
    handles user interaction, and processes PDFs.
    """

    load_dotenv()
    st.set_page_config(page_title="Chat with PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)  # Apply CSS styles

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with PDFs :books:")
    user_question = st.text_input("Ask a question :")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Documents")
        pdf_docs = st.file_uploader(
            "Upload your PDFs here and click on 'Ingest'", accept_multiple_files=True)
        if st.button("Ingest"):
            with st.spinner("Processing"):
                # Process PDFs
                raw_text = get_pdf_text(pdf_docs)
                run_ingest(raw_text)


if __name__ == '__main__':
    main()

