import os
import anthropic
import chromadb
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_collection(name="littelfuse")

# Anthropic
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query", "").strip()
    
    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Search ChromaDB
    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    # Build context from results
    context = ""
    seen_urls = set()

    links = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        context += f"\nProduct {i+1}:\n{doc}\n"
        url = meta.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            links.append({
                "name": meta.get("subcategory") or meta.get("category"),
                "url": url,
                "category": meta.get("category"),
                "part_number": meta.get("part_number", "")
            })

    top_url = links[0]["url"] if links else "https://www.littelfuse.com/products/switches"
    top_name = links[0]["name"] if links else "Littelfuse Switches"

    prompt = f"""You are a Littelfuse switch expert assistant. You help engineers and customers with anything related to Littelfuse switches — product selection, technical questions, comparisons, wiring guidance, terminology, and more.

    Customer message: {query}

    Relevant Littelfuse products and information from the database:
    {context}

    Instructions:
    - First understand what type of question this is.

    - If it is a PRODUCT SELECTION question (customer needs a switch for an application): respond with this structure in plain text:

    1. RECOMMENDED PRODUCT
    [name, series, and direct link: {top_url}]

    2. WHY IT FITS
    [explanation]

    3. KEY SPECS
    [voltage, current, IP rating, certifications]

    4. INTEGRATION TIPS
    [2-3 practical numbered tips]

    - If it is a TECHNICAL or EDUCATIONAL question (what is X, how does X work, what does X mean): answer clearly and concisely in plain text, no forced structure. Always end with the most relevant product link from the database.

    - If it is a COMPARISON question (difference between X and Y): compare them clearly, mention relevant Littelfuse series, and end with links to both products.

    - If it is a HOW-TO question (how to wire, how to install, how to select): give practical step by step guidance, and end with the most relevant product link.

    Always base your answer on the Littelfuse product database provided. Be concise, technical but human. No markdown, no asterisks, no hashtags. Max 280 words. Never ask the customer for more information. Always give the best answer you can with what you have."""
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    recommendation = message.content[0].text

    return jsonify({
        "recommendation": recommendation,
        "links": links[:3]
    })

if __name__ == "__main__":
    app.run(debug=True)