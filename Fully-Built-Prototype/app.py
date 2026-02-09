# import os
# import re
# import json
# import pandas as pd
# import networkx as nx
# from flask import Flask, render_template, request, jsonify
# from groq import Groq

# app = Flask(__name__)

# # ==================================================
# # 1. SETUP & DATA LOADING
# # ==================================================

# # ⚠️ Set your API Key here or in Environment Variables
# api_key = os.environ.get("GROQ_API_KEY", "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")
# client = Groq(api_key=api_key)

# # Global variables for data
# G = None
# kg_lookup = {}
# df = pd.DataFrame()

# def load_data():
#     global G, kg_lookup, df
    
#     # --- Load Knowledge Graph ---
#     try:
#         G = nx.read_graphml("student_kg.graphml")
#         # Build Lookup for Search
#         for node, data in G.nodes(data=True):
#             kg_lookup[str(node).lower().strip()] = node
#             if "name" in data:
#                 kg_lookup[str(data["name"]).lower().strip()] = node
#         print(f"✅ KG Loaded: {len(G.nodes())} nodes")
#     except Exception as e:
#         print(f"❌ Error loading KG: {e}")
#         G = nx.DiGraph()

#     # --- Load CSV ---
#     try:
#         df = pd.read_csv("registration.csv")
#         df = df.astype(str)
#         print(f"✅ CSV Loaded: {len(df)} rows")
#     except Exception as e:
#         print(f"❌ Error loading CSV: {e}")

# # Load data immediately on startup
# load_data()

# # ==================================================
# # 2. HELPER FUNCTIONS (Your Logic)
# # ==================================================

# def extract_entity(user_query):
#     # Regex for Roll Number (Priority 1)
#     roll_match = re.search(r"\b(VU[A-Z0-9]+)\b", user_query, re.IGNORECASE)
#     if roll_match:
#         return roll_match.group(1).upper()

#     # LLM for Name Extraction (Priority 2)
#     try:
#         extraction = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": "Extract the main Entity (Person Name, Course Name, ID) from the text. Return ONLY the string."},
#                 {"role": "user", "content": user_query}
#             ],
#             temperature=0
#         )
#         return extraction.choices[0].message.content.strip().replace('"', '').replace("'", "")
#     except:
#         return user_query # Fallback

# def get_context(entity_str):
#     context_data = []
#     search_key = entity_str.lower().strip()

#     # --- Graph Search ---
#     node_id = kg_lookup.get(search_key)
#     # Fuzzy match fallback
#     if not node_id:
#         for name, nid in kg_lookup.items():
#             if search_key in name:
#                 node_id = nid
#                 break
    
#     if node_id:
#         # Search neighbors (Undirected to capture all flows)
#         for nbr in G.to_undirected().neighbors(node_id):
#             rel = "CONNECTED"
#             if G.has_edge(node_id, nbr): rel = G[node_id][nbr].get("relation", rel)
#             elif G.has_edge(nbr, node_id): rel = G[nbr][node_id].get("relation", rel)
            
#             target_name = G.nodes[nbr].get("name", nbr)
#             context_data.append(f"Graph: {entity_str} --[{rel}]--> {target_name}")

#     # --- CSV Search ---
#     if not df.empty:
#         mask = df.apply(lambda row: row.astype(str).str.contains(entity_str, case=False).any(), axis=1)
#         for _, row in df[mask].iterrows():
#             row_str = ", ".join([f"{col}: {val}" for col, val in row.items()])
#             context_data.append(f"CSV: [{row_str}]")

#     return "\n".join(context_data) if context_data else None

# # ==================================================
# # 3. FLASK ROUTES
# # ==================================================

# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/get_sidebar_info", methods=["GET"])
# def get_sidebar_info():
#     """Extracts unique Faculty and Courses for the UI Sidebar"""
#     faculty = set()
#     courses = set()
    
#     # We iterate through nodes and guess type based on attributes or relationships
#     # Adjust logic based on your specific GraphML structure
#     for n, data in G.nodes(data=True):
#         label = data.get("label", "").lower()
#         name = data.get("name", str(n))
        
#         if "course" in label or "subject" in label:
#             courses.add(name)
#         elif "prof" in label or "faculty" in label or "teacher" in label:
#             faculty.add(name)
#         elif "dr." in name.lower() or "mr." in name.lower(): # Heuristic fallback
#             faculty.add(name)
            
#     return jsonify({
#         "faculty": list(faculty),
#         "courses": list(courses)
#     })

# @app.route("/chat", methods=["POST"])
# def chat():
#     user_message = request.json.get("message", "")
    
#     # 1. Extract Entity
#     entity = extract_entity(user_message)
    
#     # 2. Get Context
#     context = get_context(entity)
    
#     if not context:
#         system_prompt = "You are a helpful university assistant. The user asked a question, but no specific records were found in the database. Answer generally if possible, or politely state you don't have that info."
#         db_context = "No specific database records found."
#     else:
#         system_prompt = "You are a helpful university assistant. Answer ONLY using the provided Database Context."
#         db_context = context

#     # 3. Generate Answer
#     try:
#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": f"Question: {user_message}\n\nDatabase Context:\n{db_context}"}
#             ],
#             temperature=0.3
#         )
#         bot_reply = response.choices[0].message.content
#     except Exception as e:
#         bot_reply = f"Error communicating with AI: {str(e)}"

#     return jsonify({"reply": bot_reply})

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)














import os
import re
import json
import pandas as pd
import networkx as nx
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# ==================================================
# 1. SETUP & DATA LOADING
# ==================================================
# ⚠️ Set your API Key
api_key = os.environ.get("GROQ_API_KEY", "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")
client = Groq(api_key=api_key)

G = None
kg_lookup = {}
df = pd.DataFrame()

def load_data():
    global G, kg_lookup, df
    
    # --- Load Knowledge Graph ---
    try:
        G = nx.read_graphml("student_kg.graphml")
        # Build Lookup for Search (Names & IDs)
        for node, data in G.nodes(data=True):
            kg_lookup[str(node).lower().strip()] = node
            if "name" in data:
                kg_lookup[str(data["name"]).lower().strip()] = node
        print(f"✅ KG Loaded: {len(G.nodes())} nodes")
    except Exception as e:
        print(f"❌ Error loading KG: {e}")
        G = nx.DiGraph()

    # --- Load CSV ---
    try:
        df = pd.read_csv("registration.csv")
        df = df.astype(str)
        print(f"✅ CSV Loaded: {len(df)} rows")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")

load_data()

# ==================================================
# 2. INTELLIGENT RETRIEVAL (The Fix)
# ==================================================

def extract_entity(user_query):
    # 1. Regex for Roll Number (Priority 1)
    roll_match = re.search(r"\b(VU[A-Z0-9]+)\b", user_query, re.IGNORECASE)
    if roll_match:
        return roll_match.group(1).upper()

    # 2. LLM for Name Extraction (Priority 2)
    try:
        # We ask LLM to be very precise to avoid extracting 'Subject' or 'Course' as the name
        extraction = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "Extract the specific Entity (Person Name, Student ID, or Specific Course Name) from the text. Return ONLY the string. Do not include words like 'subject' or 'prof'."},
                {"role": "user", "content": user_query}
            ],
            temperature=0
        )
        cleaned_entity = extraction.choices[0].message.content.strip().replace('"', '').replace("'", "")
        return cleaned_entity
    except:
        return user_query

def get_context(entity_str):
    context_data = set() # Use set to avoid duplicates
    search_key = entity_str.lower().strip()

    # --- 1. Graph Search (2-HOP LOGIC) ---
    node_id = kg_lookup.get(search_key)
    
    # Fuzzy match fallback
    if not node_id:
        for name, nid in kg_lookup.items():
            if search_key in name:
                node_id = nid
                break
    
    if node_id:
        # HOP 1: Get immediate neighbors (e.g., Neha -> Thermodynamics)
        # We use to_undirected() to ensure we follow arrows both ways
        neighbors_hop1 = list(G.to_undirected().neighbors(node_id))
        
        for n1 in neighbors_hop1:
            # Add Hop 1 Relationship
            rel = "CONNECTED"
            if G.has_edge(node_id, n1): rel = G[node_id][n1].get("relation", rel)
            elif G.has_edge(n1, node_id): rel = G[n1][node_id].get("relation", rel)
            
            n1_name = G.nodes[n1].get("name", n1)
            context_data.add(f"Graph: {entity_str} --[{rel}]--> {n1_name}")

            # HOP 2: Get neighbors of the neighbor (e.g., Thermodynamics -> Dr. Sharma)
            # This is CRITICAL for "Who teaches my courses?"
            for n2 in G.to_undirected().neighbors(n1):
                if n2 == node_id: continue # Don't go back to start
                
                rel2 = "CONNECTED"
                if G.has_edge(n1, n2): rel2 = G[n1][n2].get("relation", rel2)
                elif G.has_edge(n2, n1): rel2 = G[n2][n1].get("relation", rel2)
                
                n2_name = G.nodes[n2].get("name", n2)
                
                # OPTIMIZATION: Only add Hop 2 if it looks like faculty/course info
                # (You can remove this 'if' to get everything, but it might be noisy)
                context_data.add(f"Graph: {n1_name} --[{rel2}]--> {n2_name}")

    # --- 2. CSV Search ---
    if not df.empty:
        mask = df.apply(lambda row: row.astype(str).str.contains(entity_str, case=False).any(), axis=1)
        for _, row in df[mask].iterrows():
            row_str = ", ".join([f"{col}: {val}" for col, val in row.items()])
            context_data.add(f"CSV: [{row_str}]")

    return "\n".join(list(context_data)) if context_data else None

# ==================================================
# 3. FLASK ROUTES
# ==================================================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_sidebar_info", methods=["GET"])
def get_sidebar_info():
    faculty = set()
    courses = set()
    for n, data in G.nodes(data=True):
        label = data.get("label", "").lower()
        name = data.get("name", str(n))
        if "course" in label or "subject" in label: courses.add(name)
        elif "prof" in label or "faculty" in label: faculty.add(name)
        elif "dr." in name.lower(): faculty.add(name)
            
    return jsonify({"faculty": list(faculty), "courses": list(courses)})

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    
    # 1. Extract Entity
    entity = extract_entity(user_message)
    
    # 2. Get Context (Deep Search)
    context = get_context(entity)
    
    # 3. System Prompt
    if not context:
        system_prompt = "You are a university assistant. The user asked a question but no database records were found. Politely explain that you lack specific data for that query."
        db_context = "No Data Found."
    else:
        # We explicitly tell the LLM to look for 2nd-order connections
        system_prompt = "You are a university assistant. Answer using the Context. Note: If a student is connected to a Course, and that Course is connected to a Professor, that Professor teaches the student."
        db_context = context

    # 4. Generate Answer
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Question: {user_message}\n\nGraph Context:\n{db_context}"}
            ],
            temperature=0.3
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        bot_reply = f"Error: {str(e)}"

    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)