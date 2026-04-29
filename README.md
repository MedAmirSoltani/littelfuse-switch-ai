# Littelfuse Switch Selector AI

> Natural language switch selection powered by semantic search and LLM.

Give it an engineering problem. Get back the right Littelfuse switch — with specs, integration tips, and a direct link to the product page.

---

## Overview

Engineers and customers often struggle to navigate large switch catalogs. This tool lets you describe your application in plain language and instantly get a precise product recommendation grounded in the real Littelfuse catalog.

It handles more than just product selection — ask it technical questions, request comparisons between switch types, or get wiring guidance. It adapts its response format to the type of question.

---

## Demo

```
Query:    "I need a switch to safely disconnect a 1500V solar array"

Response: 1. RECOMMENDED PRODUCT
          1500 VDC Disconnect Switches — LS7R Series
          https://www.littelfuse.com/products/switches/dc-disconnect-switches/1500-vdc-disconnect-switches

          2. WHY IT FITS
          Purpose-built for solar PV disconnect at 1500 VDC. Patented
          arc-minimizing operation critical at this voltage level...

          3. KEY SPECS
          Voltage: 1500 VDC
          Current: 250A, 320A, 400A, 500A depending on model
          Arc management: Patented disconnect mechanism
          ...

          4. INTEGRATION TIPS
          1. Size to 125% of max string current per NEC 690...
          2. Install between PV array and inverter for code compliance...
          3. Coordinate with upstream overcurrent protection...
```

---

## How it works

```
User query (natural language)
        │
        ▼
   Flask API (app.py)
        │
        ▼
   ChromaDB ──── semantic search across 153 product entries
        │
        ▼
   Top 3 matches returned with metadata
        │
        ▼
   Claude API ── generates structured recommendation
        │
        ▼
   Response with product name, specs, tips, and clickable link
```

**RAG architecture** — Retrieval Augmented Generation. Instead of relying on the AI's memory, the system first retrieves relevant product data from the vector database, then uses Claude to reason over it. This ensures recommendations are always grounded in real Littelfuse catalog data.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Vector DB | ChromaDB |
| AI | Anthropic Claude API |
| Frontend | HTML, CSS, Vanilla JS |
| Data pipeline | BeautifulSoup, Pandas, LLM structuring |

---

## Knowledge base

**153 entries across 18 switch categories**, built from the full Littelfuse switch catalog.

| Category | Entries |
|---|---|
| DC Disconnect Switches | 5 subcategories + full specs |
| Tactile Switches | 72 real part numbers |
| Toggle Switches | 18 real part numbers |
| Detect Switches | 19 real part numbers |
| Slide Switches | 14 real part numbers |
| Push-Pull Switches | 5 real part numbers |
| + 12 other categories | Category-level data |

**Data collection pipeline:**
1. Product category pages scraped with **BeautifulSoup**
2. Part-level CSV exports parsed with **Pandas**
3. Raw data structured into unified JSON format using an **LLM pipeline**
4. Loaded into **ChromaDB** as vector embeddings for semantic search

---

## Project structure

```
littelfuse-switch-ai/
│
├── app.py                            # Flask backend + Claude API integration
├── load_db.py                        # Loads JSON knowledge base into ChromaDB
├── littelfuse_knowledge_base.json    # 153 product entries (18 categories)
├── requirements.txt
├── .env                              # API key — not committed
│
├── chroma_db/                        # Vector store — auto-generated on first run
│
├── templates/
│   └── index.html                    # Main UI
│
└── static/
    ├── css/style.css
    ├── js/main.js
    └── img/littelfuse_logo.png
```

---

## Setup

**Requirements:** Python 3.9+, an Anthropic API key

**1. Clone**
```bash
git clone https://github.com/MedAmirSoltani/littelfuse-switch-ai
cd littelfuse-switch-ai
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure environment**
```bash
# Create .env file
echo "ANTHROPIC_API_KEY=your_key_here" > .env
```

**4. Load the knowledge base**
```bash
python load_db.py
```

This creates the ChromaDB vector store from the JSON knowledge base. Run once.

**5. Start the app**
```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000)

---

## Requirements

```
flask
chromadb
anthropic
python-dotenv
```

---

*Built by [Mohamed Amir Soltani](https://medamirsoltani.github.io/)*