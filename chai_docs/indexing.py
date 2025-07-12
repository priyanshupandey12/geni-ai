from dotenv import load_dotenv
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from bs4 import BeautifulSoup
import requests
from langchain.schema import Document
import os


load_dotenv()

BASE_URL = "https://docs.chaicode.com"
START_PAGE = "/youtube/getting-started/"
headers = {
    "User-Agent": os.getenv("USER_AGENT", "Mozilla/5.0 LangChainBot/1.0")
}


res = requests.get(BASE_URL + START_PAGE,headers=headers)
soup = BeautifulSoup(res.text, "html.parser")


sidebar_links = set()


for tag in soup.find_all("a", href=True):
    href = tag["href"]
    if href.startswith("/youtube/"):
        full_url = BASE_URL + href
        sidebar_links.add(full_url)

sidebar_links = list(sidebar_links)



documents = []

for url in sidebar_links:
    try:
        page = requests.get(url, headers=headers)
        page_soup = BeautifulSoup(page.text, "html.parser")

       
        main_content = page_soup.find("main") or page_soup.find("article") or page_soup.body
        if not main_content:
            print(f"⚠️ No readable section found in {url}")
            continue

      
        text = main_content.get_text(separator="\n", strip=True)

        if len(text.strip()) > 50:  # Skip very short/empty pages
            documents.append(Document(page_content=text, metadata={"source": url}))
            print(f" Loaded: {url}")
        else:
            print(f" Skipped empty page: {url}")

    except Exception as e:
        print(f" Failed to load {url}: {e}")



# Step 4: Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200
)

split_docs = splitter.split_documents(documents)





# Vector embedding

embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

#Using [embedding_model] create embeddings of [split_docs] and store in DB

vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="chai_docs",
    embedding=embedding_model
)

print("Indexing of Documents Done...")
