import streamlit as st
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI
import uuid
import os

# Load .env variables
load_dotenv()
client = OpenAI()

# Page Config
st.set_page_config(page_title="📘 PDF Chat App", layout="centered")

# Title
st.title("📘 Chat with Your PDF")
st.markdown("""
Upload any PDF, click **Prepare this PDF**, and instantly start chatting with it.  
No more endless scrolling — ask your document anything!
""")

# Session state
if 'ready' not in st.session_state:
    st.session_state.ready = False
if 'collection_name' not in st.session_state:
    st.session_state.collection_name = ""

# Upload PDF
uploaded_pdf = st.file_uploader("📤 Upload a PDF", type=["pdf"])

# Prepare button
if uploaded_pdf and st.button("🚀 Prepare this PDF"):
    with st.spinner("Processing PDF..."):
        # Save PDF temporarily
        temp_path = Path("temp") / uploaded_pdf.name
        temp_path.parent.mkdir(exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_pdf.read())

        # Load and split PDF
        loader = PyPDFLoader(str(temp_path))
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)

        # Embed
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
        collection_name = uploaded_pdf.name.replace(".pdf", "").replace(" ", "_") + "_" + str(uuid.uuid4())[:6]
        st.session_state.collection_name = collection_name

        # Store in Qdrant
        QdrantVectorStore.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=collection_name,
            url="http://localhost:6333"
        )

        st.session_state.ready = True
        st.success("✅ Ready for Chatting!")

# Chat interface
if st.session_state.ready:
    user_query = st.chat_input("💬 Ask a question about the PDF")

    if user_query:
        with st.spinner("Searching and responding..."):
            vector_store = QdrantVectorStore.from_existing_collection(
                embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
                collection_name=st.session_state.collection_name,
                url="http://localhost:6333"
            )

            results = vector_store.similarity_search(user_query, k=4)

            context = "\n\n\n".join([
                f"Page Content: {doc.page_content}\nPage Number: {doc.metadata.get('page_label', 'N/A')}"
                for doc in results
            ])

            system_prompt = f"""
            You are a helpful AI assistant. Only answer the user's question based on the context below, 
            and refer to page numbers if needed.

            Context:
            {context}
            """

            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ]
            )

            st.chat_message("user").markdown(user_query)
            st.chat_message("assistant").markdown(response.choices[0].message.content)

            with st.expander("📄 Show Context Used"):
                st.markdown(context)
