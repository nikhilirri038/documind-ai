
import os
import time

import streamlit as st
import pymupdf
from dotenv import load_dotenv
from google import genai
from google.genai import errors

# Load API key from .env
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DocuMind AI",
    page_icon="📄",
    layout="wide"
)

st.title("📄 DocuMind AI")
st.write("Upload a PDF and chat with its content using Gemini AI.")

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Gemini model
MODEL_NAME = "gemini-3.8-flash"

# PDF uploader
uploaded_file = st.file_uploader(
    "Choose your PDF document",
    type=["pdf"]
)

if uploaded_file is None:
    st.info("Upload a PDF to start asking questions.")

else:
    try:
        # Extract text from PDF
        with pymupdf.open(
            stream=uploaded_file.getvalue(),
            filetype="pdf"
        ) as pdf:
            pages = [page.get_text() for page in pdf]

        text = "\n\n".join(pages)

        # Identify the currently uploaded PDF
        pdf_id = f"{uploaded_file.name}:{uploaded_file.size}"

        # Reset conversation when the PDF changes
        if st.session_state.get("pdf_id") != pdf_id:
            st.session_state.pdf_id = pdf_id
            st.session_state.messages = []
            st.session_state.pending_question = None

        if not text.strip():
            st.warning(
                "No readable text was found in this PDF. "
                "It may be a scanned document that needs OCR."
            )

        else:
            st.success(
                f"PDF uploaded successfully! Pages: {len(pages)}"
            )

            # Display extracted text
            with st.expander("View extracted text"):
                st.text_area(
                    "PDF content",
                    value=text[:10000],
                    height=250
                )

            st.divider()
            st.subheader("💬 Chat with your PDF")

            # Initialize session state
            if "messages" not in st.session_state:
                st.session_state.messages = []

            if "pending_question" not in st.session_state:
                st.session_state.pending_question = None

            # Display chat history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Ask a new question
            question = st.chat_input(
                "Ask a question about your PDF..."
            )

            # Save a submitted question for processing
            if question:
                st.session_state.pending_question = question

            # Process the current or retryable question
            if st.session_state.pending_question:
                current_question = (
                    st.session_state.pending_question
                )

                # Add the question to history only once
                if (
                    not st.session_state.messages
                    or st.session_state.messages[-1]["role"] != "user"
                    or st.session_state.messages[-1]["content"]
                    != current_question
                ):
                    st.session_state.messages.append({
                        "role": "user",
                        "content": current_question
                    })

                # Show the question if it is not already displayed
                # in the chat history on this run.
                with st.chat_message("user"):
                    st.markdown(current_question)

                if not api_key:
                    st.error(
                        "Gemini API key not found. "
                        "Check GEMINI_API_KEY in your .env file."
                    )
                    st.session_state.pending_question = None

                else:
                    # Prepare recent conversation history
                    previous_messages = [
                        message
                        for message in st.session_state.messages[:-1]
                    ][-10:]

                    history = "\n".join(
                        f'{message["role"]}: {message["content"]}'
                        for message in previous_messages
                    )

                    prompt = f"""
You are DocuMind AI, a helpful PDF assistant.

Answer the user's question using the PDF content.

Rules:
- Prefer information from the supplied PDF.
- If the answer is not in the PDF, say so clearly.
- Do not invent facts.
- Use simple, clear English.
- Use previous conversation to understand follow-up
  questions such as "What are its benefits?"
- Keep answers relevant to the user's question.

PDF CONTENT:
{text[:30000]}

PREVIOUS CONVERSATION:
{history}

LATEST USER QUESTION:
{current_question}
"""

                    answer = None
                    last_error = None

                    # Retry temporary server errors up to 3 times
                    for attempt in range(3):
                        try:
                            client = genai.Client(
                                api_key=api_key
                            )

                            with st.chat_message("assistant"):
                                with st.spinner(
                                    "Gemini is thinking..."
                                    if attempt == 0
                                    else f"Gemini is busy. Retrying "
                                         f"({attempt}/2)..."
                                ):
                                    response = (
                                        client.models.generate_content(
                                            model=MODEL_NAME,
                                            contents=prompt
                                        )
                                    )

                                answer = (
                                    response.text
                                    or "Gemini returned an empty answer."
                                )
                                st.markdown(answer)

                            # Request succeeded
                            break

                        except Exception as error:
                            last_error = error
                            error_message = str(error).upper()

                            is_temporary = any(
                                marker in error_message
                                for marker in [
                                    "503",
                                    "UNAVAILABLE",
                                    "429",
                                    "RESOURCE_EXHAUSTED",
                                    "500",
                                    "INTERNAL",
                                    "502",
                                    "504",
                                    "DEADLINE_EXCEEDED"
                                ]
                            )

                            # Do not retry non-temporary errors
                            if not is_temporary or attempt == 2:
                                break

                            # Wait before retrying
                            time.sleep(2 ** (attempt + 1))

                    if answer is not None:
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })
                        st.session_state.pending_question = None

                    else:
                        error_message = str(last_error).upper()

                        if (
                            "503" in error_message
                            or "UNAVAILABLE" in error_message
                            or "500" in error_message
                            or "502" in error_message
                            or "504" in error_message
                            or "INTERNAL" in error_message
                        ):
                            st.warning(
                                "Gemini is temporarily busy. "
                                "Your question is saved. Please click "
                                "'Retry question' in a moment."
                            )
                        elif (
                            "429" in error_message
                            or "RESOURCE_EXHAUSTED" in error_message
                        ):
                            st.warning(
                                "Gemini rate limit or quota reached. "
                                "Wait a little and try again. If this "
                                "continues, check your API quota."
                            )
                        else:
                            st.error(
                                f"Gemini API error: {last_error}"
                            )

                        # The question remains pending for retry
                        if st.button("🔄 Retry question"):
                            st.rerun()

            # Clear conversation
            if st.session_state.messages:
                if st.button("🗑️ Clear chat"):
                    st.session_state.messages = []
                    st.session_state.pending_question = None
                    st.rerun()

    except Exception as error:
        st.error(f"Could not read PDF: {error}")
