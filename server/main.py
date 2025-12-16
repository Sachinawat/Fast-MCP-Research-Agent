from mcp.server.fastmcp import FastMCP
from core import log_interaction, get_vector_store, PromptRegistry, logger
import json

# Initialize FastMCP Server
mcp = FastMCP("EnterpriseResearchNode")

@mcp.tool()
def query_knowledge_base(query: str, domain: str = "general") -> str:
    """
    Primary Research Tool.
    Uses RAG (Retrieval Augmented Generation) to answer questions 
    about Physics, Math, Tech, or Social Science.
    """
    logger.info(json.dumps({"event": "tool_call", "tool": "query_knowledge_base", "query": query}))
    
    # 1. Retrieve Context (Top-K)
    vector_db = get_vector_store()
    # Fetch top 3 results
    docs = vector_db.similarity_search(query, k=3)
    context_str = "\n".join([d.page_content for d in docs])
    
    # 2. Load Dynamic Prompt
    registry = PromptRegistry()
    system_instruction = registry.get("research_system_prompt", domain=domain, context=context_str)
    
    # 3. Simulate LLM Generation (Replace with actual LangChain ChatOpenAI call)
    # response = chat_model.invoke([SystemMessage(content=system_instruction), HumanMessage(content=query)])
    
    # Mocking response for the example to run without API Key
    mock_response = f"Based on the analysis in domain '{domain}':\n\nContext found: {docs[0].page_content}\n\nConclusion: The research suggests positive correlation. (Verified)"
    
    # 4. Log to SQL
    log_interaction(query, "query_knowledge_base", mock_response)
    
    return mock_response

@mcp.tool()
def perform_complex_calculation(expression: str) -> str:
    """
    Executes Python math logic safely. 
    Useful for Physics/Math verifications.
    """
    logger.info(json.dumps({"event": "tool_call", "tool": "perform_complex_calculation", "expression": expression}))
    
    try:
        # Dangerous in prod: use specific math libraries (numpy/scipy) only
        # Here we use a safe eval subset or library
        import math
        allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        
        log_interaction(expression, "math_tool", result)
        return str(result)
    except Exception as e:
        return f"Calculation Error: {str(e)}"

@mcp.tool()
def get_interaction_history(limit: int = 5) -> str:
    """Retrieves past research logs for audit."""
    import sqlite3
    conn = sqlite3.connect("../data/research.db")
    c = conn.cursor()
    c.execute("SELECT * FROM interactions ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return json.dumps(rows, default=str)

if __name__ == "__main__":
    # Standard MCP execution
    mcp.run()