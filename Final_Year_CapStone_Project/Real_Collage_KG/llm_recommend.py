# import os
# import json
# import networkx as nx
# from groq import Groq

# # ==========================
# # Load KG
# # ==========================
# G = nx.read_graphml("student_kg.graphml")

# # ==========================
# # LLM client
# # ==========================
# client = Groq(api_key="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")

# # ==========================
# # KG TOOL
# # ==========================
# def query_kg(query_type, entity=None):
#     if query_type == "popular_courses":
#         counts = {}
#         for u, v, d in G.edges(data=True):
#             if d.get("relation") == "REGISTERED_FOR":
#                 course = v if G.nodes[v].get("label") == "Course" else u
#                 counts[course] = counts.get(course, 0) + 1
#         top = sorted(counts, key=counts.get, reverse=True)[:5]
#         return [{"course": G.nodes[c]["name"], "count": counts[c]} for c in top]

#     if query_type == "student_courses":
#         result = []
#         for nbr in G.neighbors(entity):
#             e = G.get_edge_data(entity, nbr)
#             if e.get("relation") == "REGISTERED_FOR":
#                 result.append(G.nodes[nbr]["name"])
#         return result

#     return []

# # ==========================
# # AGENT LOOP
# # ==========================
# while True:
#     user_question = input("\nAsk me anything (or type exit): ")

#     if user_question.lower() == "exit":
#         break

#     # Step 1: LLM decides what to retrieve
#     planning = client.chat.completions.create(
#         model="openai/gpt-oss-20b",
#         messages=[
#             {
#                 "role": "system",
#                 "content": """
# You are a university guidance agent.
# Decide what knowledge you need from the KG.

# Return ONLY JSON like:
# {
#   "query_type": "...",
#   "entity": "..."
# }

# Possible query_type:
# - popular_courses
# - student_courses
# """
#             },
#             {"role": "user", "content": user_question}
#         ],
#         temperature=0
#     )

#     plan = json.loads(planning.choices[0].message.content)

#     # Step 2: Query KG
#     facts = query_kg(plan["query_type"], plan.get("entity"))

#     # Step 3: LLM explains + justifies
#     answer = client.chat.completions.create(
#         model="openai/gpt-oss-20b",
#         messages=[
#             {
#                 "role": "system",
#                 "content": "You are a helpful university mentor. Explain answers with reasons."
#             },
#             {
#                 "role": "user",
#                 "content": f"""
# Question: {user_question}

# Facts from knowledge graph:
# {facts}

# Answer the question and explain WHY this is the best choice.
# """
#             }
#         ],
#         temperature=0.4
#     )

#     print("\nAnswer:\n")
#     print(answer.choices[0].message.content)




import os
import json
import networkx as nx
from groq import Groq
import re

# ==========================
# 1. Load KG & Build Lookup
# ==========================
# Ensure you have your .graphml file ready
try:
    G = nx.read_graphml("student_kg.graphml")
except FileNotFoundError:
    print("Error: 'student_kg.graphml' not found. Please ensure the file exists.")
    exit()

# FIX: Create a mapping from 'Name' to 'Node ID'
# This ensures that if the user says "Alice", we find the node "s101"
name_to_id = {}
for node, data in G.nodes(data=True):
    if "name" in data:
        # Store as lowercase for case-insensitive matching
        name_to_id[data["name"].lower()] = node

# ==========================
# 2. LLM Client
# ==========================
# Replace with your NEW API Key (Revoke the old one!)
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "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"))

# ==========================
# 3. Helper: Clean JSON
# ==========================
def parse_llm_json(content):
    """
    Strips markdown backticks and ensures valid JSON parsing.
    """
    try:
        # Remove ```json and ``` if present
        content = re.sub(r"```json\s*", "", content)
        content = re.sub(r"```", "", content)
        return json.loads(content)
    except json.JSONDecodeError:
        print("Error: LLM did not return valid JSON.")
        return {}

# ==========================
# 4. KG Tool Logic
# ==========================
def query_kg(query_type, entity_name=None):
    if query_type == "popular_courses":
        counts = {}
        for u, v, d in G.edges(data=True):
            # Check for relation type (case-insensitive safety)
            if d.get("relation") == "REGISTERED_FOR":
                # Determine which node is the course
                target = v if G.nodes[v].get("label") == "Course" else u
                counts[target] = counts.get(target, 0) + 1
        
        # Sort and take top 5
        top = sorted(counts, key=counts.get, reverse=True)[:5]
        return [{"course": G.nodes[c].get("name", c), "count": counts[c]} for c in top]

    if query_type == "student_courses":
        if not entity_name:
            return "Error: No student name provided."
        
        # FIX: Resolve Name to ID
        entity_id = name_to_id.get(entity_name.lower())
        
        if not entity_id:
            return f"Error: Student '{entity_name}' not found in the database."

        result = []
        try:
            for nbr in G.neighbors(entity_id):
                e = G.get_edge_data(entity_id, nbr)
                if e.get("relation") == "REGISTERED_FOR":
                    course_name = G.nodes[nbr].get("name", nbr)
                    result.append(course_name)
        except Exception as e:
            return f"Error traversing graph: {str(e)}"
            
        return result

    return []

# ==========================
# 5. Agent Loop
# ==========================
print("University Agent Ready. (Type 'exit' to quit)")

while True:
    user_question = input("\nAsk me anything: ")
    if user_question.lower() in ["exit", "quit"]:
        break

    # --- Step 1: Planning ---
    # We use Llama3-70b for better reasoning
    planning_prompt = """
    You are a Knowledge Graph Query Agent.
    Based on the user's question, output which tool to use.
    
    1. If asking about a specific student's classes, use "student_courses" and extract the student's name as "entity".
    2. If asking about popular/trending classes generally, use "popular_courses".
    
    Return ONLY valid JSON. No markdown. No comments.
    Format:
    {
      "query_type": "student_courses" | "popular_courses",
      "entity": "Name or null"
    }
    """

    try:
        planning = client.chat.completions.create(
             model="llama-3.3-70b-versatile",  # Valid Groq Model
            messages=[
                {"role": "system", "content": planning_prompt},
                {"role": "user", "content": user_question}
            ],
            temperature=0,
            response_format={"type": "json_object"} # Forces JSON mode if supported
        )

        plan_content = planning.choices[0].message.content
        plan = parse_llm_json(plan_content)
        
        print(f"DEBUG: Plan -> {plan}") # Helpful for debugging

        # --- Step 2: Execution ---
        facts = query_kg(plan.get("query_type"), plan.get("entity"))
        
        # --- Step 3: Synthesis ---
        answer = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a helpful university mentor. Use the provided KG Facts to answer the user. If the facts indicate an error, apologize and explain."
                },
                {
                    "role": "user", 
                    "content": f"User Question: {user_question}\n\nKG Facts: {facts}"
                }
            ],
            temperature=0.5
        )

        print("\nAnswer:")
        print(answer.choices[0].message.content)

    except Exception as e:
        print(f"An error occurred: {e}")