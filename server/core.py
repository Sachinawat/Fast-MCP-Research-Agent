import sqlite3
import yaml
import json
import logging
import os
from datetime import datetime
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

# --- Configuration ---
LOG_DIR = "../logs"
DATA_DIR = "../data"
PROMPT_FILE = "../prompts/registry.yaml"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# --- 1. Centralized Logging (JSON Structured) ---
logger = logging.getLogger("EnterpriseResearch")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(f"{LOG_DIR}/app.log")
formatter = logging.Formatter('{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}')
handler.setFormatter(formatter)
logger.addHandler(handler)

# --- 2. SQL Interaction Storage ---
def init_db():
    conn = sqlite3.connect(f"{DATA_DIR}/research.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS interactions
                 (id INTEGER PRIMARY KEY, query TEXT, tool_used TEXT, response TEXT, timestamp DATETIME)''')
    conn.commit()
    return conn

def log_interaction(query, tool, response):
    conn = init_db()
    c = conn.cursor()
    c.execute("INSERT INTO interactions (query, tool_used, response, timestamp) VALUES (?, ?, ?, ?)",
              (query, tool, str(response), datetime.now()))
    conn.commit()
    conn.close()

# --- 3. Dynamic Prompt Registry ---
class PromptRegistry:
    def __init__(self, filepath=PROMPT_FILE):
        self.filepath = filepath
        self.prompts = {}
        self.load_prompts()

    def load_prompts(self):
        try:
            with open(self.filepath, 'r') as f:
                self.prompts = yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load prompts: {e}")

    def get(self, key, **kwargs):
        # Reloads every time to allow dynamic updates without restart
        self.load_prompts() 
        template = self.prompts.get(key, "")
        return template.format(**kwargs)

# --- 4. RAG Engine (Simulated Ingestion) ---
def get_vector_store():
    # In a real app, use OpenAIEmbeddings(model="text-embedding-3-small")
    # For demo, we assume embeddings work or use a mock if no API key
    embeddings = OpenAIEmbeddings() 
    
    # Check if persistent store exists, if not create dummy scientific data
    db = Chroma(persist_directory=f"{DATA_DIR}/vector_store", embedding_function=embeddings)
    
    if db._collection.count() == 0:
        docs = [
            Document(page_content="Quantum Entanglement implies that particles remain connected regardless of distance.", metadata={"source": "Physics_Journal_A"}),
            Document(page_content="FastMCP allows for synchronous and asynchronous tool execution in Python.", metadata={"source": "Tech_Docs"}),
            Document(page_content="Photosynthesis efficiency in C4 plants is higher than C3 plants at high temperatures.", metadata={"source": "Bio_Science_Rev"}),
        ]
        db.add_documents(docs)
    
    return db

# --- 5. Hallucination Guardrail ---
def verify_response(llm, answer, context):
    registry = PromptRegistry()
    prompt = registry.get("hallucination_check_prompt", answer=answer, context=context)
    # Simple check logic
    # validation = llm.invoke(prompt) 
    # For this code demo, we simulate a pass
    return answer