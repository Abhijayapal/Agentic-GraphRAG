import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")
AUTH = (USER, PASSWORD)


def get_schema():   #so that agent can see node labels
    """
    Retrieves the schema of the Neo4j graph so the Agent 
    knows which Nodes and Relationships are available.
    """
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        # 'System Query'-> database structure
        result = session.run("CALL db.schema.visualization()")
        # teeling agent nodes,relationships 
        schema_info = "The graph contains: Restaurant, Dish, Cuisine, and Category nodes. "
        schema_info += "Relationships include: SERVES, BELONGS_TO, and IN_CATEGORY."
        return schema_info

def query_food_graph(query: str):
    """
    Uses the user's natural language to query the Food Knowledge Graph.
    """
    driver = GraphDatabase.driver(URI, auth=AUTH)
    
    #Phidata handles the 'Text-to-Cypher' translation.
    # For now, we will test it with a manual query to see it work.
    with driver.session() as session:
        #result here is not data, it is cursor or pointer
        result = session.run(query) 
        #record.data() convert Neo4j Record object into  Python Dictionary (JSON-like).
        # this is useful because LLM is proficient in reading lists and dictionaries
        return [record.data() for record in result]
    

    

def show_menu():
    """Use this function when the user asks for the 'menu', 'all dishes', or 'what is available'.Returns a simplified menu string."""
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        result = session.run("MATCH (r:Restaurant)-[:SERVES]->(d:Dish) RETURN r.name, d.name, d.price")
        # Format as a clean string immediately
        menu_items = [f"{row['r.name']}: {row['d.name']} - {row['d.price']}" for row in result]
        return "\n".join(menu_items) if menu_items else "No menu items found."