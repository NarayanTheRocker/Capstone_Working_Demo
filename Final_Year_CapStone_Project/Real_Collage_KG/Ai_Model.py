# 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

import os
import json
import networkx as nx
from groq import Groq

# ==========================
# 1. SETUP & SAFETY
# ==========================
# ⚠️ I removed your API key. Please use environment variables or paste a NEW key below.
api_key = os.environ.get("GROQ_API_KEY", "")

if not api_key:
    raise ValueError("❌ Please set GROQ_API_KEY environment variable or paste it in the script.")

client = Groq(api_key=api_key)

# ==========================
# 2. LOAD GRAPH
# ==========================
try:
    G = nx.read_graphml("student_kg.graphml")
    # Optimize: Create a lowercase mapping for easy searching
    # e.g. "dr. sharma" -> "T_102"
    name_lookup = {data.get("name", "").lower(): node for node, data in G.nodes(data=True)}
    print(f"✅ KG loaded: {len(G.nodes())} nodes found.")
except FileNotFoundError:
    print("❌ Error: 'student_kg.graphml' not found.")
    exit()

# ==========================
# 3. HELPER: UNIVERSAL SEARCH
# ==========================
def retrieve_node_context(search_query):
    """
    Finds a node by name and returns ALL its connections (in & out).
    """
    search_query = search_query.lower().strip()
    
    # 1. Direct Lookup
    node_id = name_lookup.get(search_query)
    
    # 2. Fuzzy/Partial Match (if direct fails)
    if not node_id:
        for name, nid in name_lookup.items():
            if search_query in name:
                node_id = nid
                break
    
    if not node_id:
        return None, f"Could not find any entity named '{search_query}' in the graph."

    # 3. Retrieve Connections (Both Incoming and Outgoing)
    # We use G.to_undirected() temporarily to get ALL neighbors easily
    # or manually check both in_edges and out_edges if it's a DiGraph.
    connections = []
    
    # Get outgoing edges (Node -> Neighbor)
    for neighbor in G.successors(node_id) if G.is_directed() else G.neighbors(node_id):
        edge_data = G.get_edge_data(node_id, neighbor)
        neighbor_name = G.nodes[neighbor].get("name", neighbor)
        relation = edge_data.get("relation", "CONNECTED_TO")
        connections.append(f"{search_query} --[{relation}]--> {neighbor_name}")

    # Get incoming edges (Neighbor -> Node)
    if G.is_directed():
        for neighbor in G.predecessors(node_id):
            edge_data = G.get_edge_data(neighbor, node_id)
            neighbor_name = G.nodes[neighbor].get("name", neighbor)
            relation = edge_data.get("relation", "CONNECTED_TO")
            connections.append(f"{neighbor_name} --[{relation}]--> {search_query}")

    return node_id, connections

# ==========================
# 4. MAIN EXECUTION
# ==========================
while True:
    user_question = input("\n Question: ")
    if user_question.lower() == "exit":
        break

    # --- Step A: Use LLM to extract the TARGET ENTITY ---
    # We ask the LLM: "Who or what is this question about?"
    extraction = client.chat.completions.create(
         model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system", 
                "content": "Extract the main Entity name from the user's question. Return ONLY the name. Nothing else."
            },
            {"role": "user", "content": user_question}
        ],
        temperature=0
    )
    
    target_entity = extraction.choices[0].message.content.strip().replace('"', '').replace("'", "")
    print(f"   (Searching KG for: '{target_entity}')")

    # --- Step B: Retrieve Context from KG ---
    node_id, context_list = retrieve_node_context(target_entity)

    if not node_id:
        print(f"⚠️  Graph Error: {context_list}")
        continue

    facts_text = "\n".join(context_list)
    print(f"   (Found {len(context_list)} connections)")

    # --- Step C: Final Answer ---
    answer = client.chat.completions.create(
         model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant. Use the Knowledge Graph Facts to answer the user's question accurately."
            },
            {
                "role": "user",
                "content": f"""
Question: {user_question}

Knowledge Graph Facts:
{facts_text}

Answer:
"""
            }
        ],
        temperature=0.3
    )

    print("\n📝 Answer:")

    print(answer.choices[0].message.content)
