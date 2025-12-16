import asyncio
import sys
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.table import Table

# Adjust path to find server modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need the mcp client libraries
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

console = Console()

async def run_client():
    console.print(Panel.fit("🧪 Enterprise Research OS \nPowered by FastMCP & LangChain", style="bold blue"))

    # Define server parameters - Pointing to the server/main.py
    server_script = os.path.abspath(os.path.join(os.path.dirname(__file__), '../server/main.py'))
    
    server_params = StdioServerParameters(
        command="python", # Or the path to your venv python
        args=[server_script],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Initialize connection
            await session.initialize()
            
            # List available tools
            tools = await session.list_tools()
            
            # --- Dashboard Visualization ---
            table = Table(title="Available Research Tools")
            table.add_column("Tool Name", style="cyan")
            table.add_column("Description", style="magenta")
            
            for tool in tools.tools:
                table.add_row(tool.name, tool.description)
            console.print(table)

            while True:
                console.print("\n[bold green]Enter Query (or 'exit'):[/bold green]")
                user_input = Prompt.ask("> ")
                
                if user_input.lower() in ['exit', 'quit']:
                    break

                # --- Router Logic (Simple Client-Side Router) ---
                # In a bigger app, this decision happens via an LLM Router Agent
                tool_name = "query_knowledge_base"
                tool_args = {"query": user_input, "domain": "general"}

                if "calculate" in user_input or "+" in user_input or "*" in user_input:
                    tool_name = "perform_complex_calculation"
                    # Simple extraction for demo
                    tool_args = {"expression": user_input.replace("calculate", "").strip()}
                
                elif "history" in user_input or "log" in user_input:
                    tool_name = "get_interaction_history"
                    tool_args = {}

                # --- Execution ---
                with console.status(f"[bold yellow]Running {tool_name}...[/bold yellow]", spinner="dots"):
                    try:
                        result = await session.call_tool(tool_name, arguments=tool_args)
                        
                        # --- Output Visualization ---
                        output_content = result.content[0].text
                        
                        console.print(Panel(
                            Markdown(output_content),
                            title=f"🔬 Result: {tool_name}",
                            border_style="green"
                        ))
                        
                    except Exception as e:
                        console.print(f"[bold red]Error executing tool:[/bold red] {e}")

if __name__ == "__main__":
    try:
        asyncio.run(run_client())
    except KeyboardInterrupt:
        console.print("\n[bold red]Shutting down Research OS...[/bold red]")