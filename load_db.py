import json
import chromadb

# Load JSON
with open("littelfuse_knowledge_base.json", "r", encoding="utf-8") as f:
    knowledge_base = json.load(f)

# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")

# Delete collection if exists (fresh load)
try:
    chroma_client.delete_collection(name="littelfuse")
    print("Existing collection deleted.")
except:
    pass

collection = chroma_client.create_collection(name="littelfuse")

# Prepare data
ids = []
documents = []
metadatas = []

for entry in knowledge_base:
    ids.append(entry["id"])
    documents.append(entry["document"])
    # ChromaDB metadata values must be str, int, float, or bool
    clean_meta = {}
    for k, v in entry["metadata"].items():
        if isinstance(v, (str, int, float, bool)):
            clean_meta[k] = v
        else:
            clean_meta[k] = str(v)
    metadatas.append(clean_meta)

# Load into ChromaDB in batches of 50
batch_size = 50
for i in range(0, len(ids), batch_size):
    collection.add(
        ids=ids[i:i+batch_size],
        documents=documents[i:i+batch_size],
        metadatas=metadatas[i:i+batch_size]
    )
    print(f"Loaded {min(i+batch_size, len(ids))}/{len(ids)} entries...")

print(f"\nDone. {collection.count()} entries in ChromaDB.")