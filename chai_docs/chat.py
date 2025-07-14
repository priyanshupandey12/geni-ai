from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI


load_dotenv()

client = OpenAI()

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="chai_docs",
    embedding=embedding_model
)

# Take User Query
query = input("Chai aur docs ke doubt me apka swagat hain : ")

search_results = vector_db.similarity_search(
    query=query
)

context = "\n\n".join(
    f"[{doc.metadata.get('source', 'unknown')}]\n{doc.page_content}" for doc in search_results
)



SYSTEM_PROMPT = f"""
You are a helpful AI Assistant who answers user queries based on the available context
retrieved from ChaiCode documentation website.

Instructions:
1. Use ONLY the context below to answer the question
2. Provide a comprehensive answer if the information is available
3. If the exact answer is not found, provide any related information you can find
4. If no relevant information is found, clearly state this
5. Always be helpful and cite sources when possible

Context:
{context}
"""

chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        { "role": "system", "content": SYSTEM_PROMPT },
        { "role": "user", "content": query },
    ],
    temperature=0.1
)

