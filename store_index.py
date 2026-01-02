from src.helper import load_data,text_spliter
from pinecone import Pinecone
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import time

load_dotenv()
my_api = os.getenv("my_key")
Pinecone_API_KEY = os.getenv("Pinecone_API_KEY")

data = load_data(r"C:\Data Sceience\PROJECTS\Medical-ChatBot-using-langchain\data")

text_chunks = text_spliter(data) 

pc = Pinecone(api_key=Pinecone_API_KEY)
index = pc.Index("embedding")

# Now we will create embeddings for our pinecone index
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004",api_key=my_api)

# Creating list of text(collect all text from chunks)
text_list = [chunk.page_content for chunk in text_chunks]

# Creating Embeddings
vectors = embeddings.embed_documents(text_list)

# Pair them back up with their IDs for Pinecone
data_to_upload = []
for i, vector in enumerate(vectors):
    data_to_upload.append({
        "id": str(chunks[i]["index"]), 
        "values": vector, 
        "metadata": {"text": chunks[i]["text"]}
    })

# we cannot upload all data at once so we will upload it in batches because we have 3426 chunks and pinecone has limit of 1000 so we can send 100 chunks at a time to prevent from error.

batch_size = 100 
total_chunks = len(data_to_upload)

print(f"Starting upload of {total_chunks} chunks to Pinecone...")

for i in range(0, total_chunks, batch_size):
    # Slice the list to get a batch of 100
    batch = data_to_upload[i : i + batch_size]
    
    try:
        # Upsert the batch
        index.upsert(vectors=batch)
        print(f"Uploaded: {min(i + batch_size, total_chunks)} / {total_chunks}")
        
    except Exception as e:
        print(f"Error at batch {i}: {e}")
        # Optional: brief pause before retrying
        time.sleep(1) 
        index.upsert(vectors=batch)