from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.playground import Playground, serve_playground_app
from specialized_tools import get_schema, query_food_graph,show_menu
load_dotenv()

low_model="llama-3.1-8b-instant"
best_model="llama-3.3-70b-versatile"

# menu-specialist agent
menu_agent = Agent(
    
    name="waiter",
    model=Groq(id=best_model),
    tools=[get_schema, query_food_graph,show_menu],
    tool_choice="auto",
    instructions=[
        "Use show_menu ONLY ONCE to get the list of food.",
        "After you get the menu from the tool, summarize it for the user and STOP.",
        "Do not call tools again once you have the data."
        "Use get_schema to understand the Neo4j graph.",
        "Use query_food_graph to find data.",
        
        ],
    
    # 🛑 Prevents the loop by force-stopping after 2 calls
    tool_call_limit=2,
    show_tool_calls=True, 
    markdown=True 
    
)
app = Playground(agents=[menu_agent]).get_app(use_async=False)
if __name__ == "__main__":
    
    serve_playground_app("playground:app", reload=True,port=10000)