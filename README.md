Most RAG systems use simple vector similarity, which often lacks logic. I built a GraphRAG system where the agent actually understands the relationships between data points. I used Phidata to create a multi-agent team where a 'Manager' agent routes tasks to specialized 'Expert' agents, all running in a Dockerized environment for scalability.

Architecture: 

tech-stack used | Python, Phidata, Neo4j, Docker, Groq, Cypher
Orchestration Layer (Phidata) ->It identifies the intent and routes the task to specialized agents.

Infrastructure Layer / DevOps (Docker,venv)->container where Neo4j daatbase and phidata workspace live in private network. For high reproducibility and seamless deployment

Knowledge Layer (Neo4j & GraphRAG):
Neo4j: store data in form of nodes, using Cypher Query Language
GraphRAG Logic to reduce hallucinations compared to traditional vector only RAG.
