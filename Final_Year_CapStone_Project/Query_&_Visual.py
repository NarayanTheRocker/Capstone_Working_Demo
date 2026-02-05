# import networkx as nx
# import matplotlib.pyplot as plt
# from pyvis.network import Network

# # ==========================
# # 1. Load saved Knowledge Graph
# # ==========================
# G = nx.read_graphml("student_kg.graphml")

# print("KG loaded")
# print("Nodes:", len(G.nodes()))
# print("Edges:", len(G.edges()))

# # ==========================
# # 2. Query: get all students of a course
# # ==========================
# course_id = "C001"   # change this to test

# nodes = set([course_id])
# edges = []

# for u, v, data in G.edges(data=True):
#     if u == course_id or v == course_id:
#         nodes.add(u)
#         nodes.add(v)
#         edges.append((u, v, data))

# # ==========================
# # 3. Build subgraph
# # ==========================
# H = nx.Graph()

# for n in nodes:
#     H.add_node(n, **G.nodes[n])

# for u, v, data in edges:
#     H.add_edge(u, v, **data)

# print("Subgraph created")
# print("Subgraph nodes:", len(H.nodes()))
# print("Subgraph edges:", len(H.edges()))

# # ==========================
# # 4. VISUALIZE (STATIC)
# # ==========================
# plt.figure(figsize=(8, 8))
# pos = nx.spring_layout(H, seed=42)

# colors = []
# for n in H.nodes():
#     label = H.nodes[n].get("label")
#     if label == "Student":
#         colors.append("skyblue")
#     elif label == "Course":
#         colors.append("lightgreen")
#     elif label == "Professor":
#         colors.append("orange")
#     else:
#         colors.append("gray")

# nx.draw_networkx_nodes(H, pos, node_color=colors, node_size=1200)
# nx.draw_networkx_edges(H, pos)
# nx.draw_networkx_labels(H, pos, font_size=9)

# plt.title(f"Students registered in {course_id}")
# plt.axis("off")
# plt.show()

# # ==========================
# # 5. INTERACTIVE VISUALIZATION
# # ==========================
# net = Network(height="600px", width="100%")
# net.from_nx(H)
# net.show("query_result.html")



import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network

# ==========================
# 1. Load KG
# ==========================
G = nx.read_graphml("student_kg.graphml")

prof_id = "P01"   # change to test different professors

nodes = set([prof_id])
edges = []

# ==========================
# 2. 2-hop traversal
# ==========================
for u, v, data in G.edges(data=True):

    # Course -> Professor
    if u == prof_id or v == prof_id:
        course = v if u == prof_id else u
        nodes.add(course)
        edges.append((u, v, data))

        # Student -> Course
        for x, y, d2 in G.edges(course, data=True):
            student = y if x == course else x
            if G.nodes[student].get("label") == "Student":
                nodes.add(student)
                edges.append((x, y, d2))

# ==========================
# 3. Build subgraph
# ==========================
H = nx.Graph()

for n in nodes:
    H.add_node(n, **G.nodes[n])

for u, v, d in edges:
    H.add_edge(u, v, **d)

print("Nodes:", H.nodes())
print("Edges:", H.edges())

# ==========================
# 4. STATIC visualization
# ==========================
plt.figure(figsize=(10, 10))
pos = nx.spring_layout(H, seed=42)

colors = []
for n in H.nodes():
    label = H.nodes[n].get("label")
    if label == "Student":
        colors.append("skyblue")
    elif label == "Course":
        colors.append("lightgreen")
    elif label == "Professor":
        colors.append("orange")
    else:
        colors.append("gray")

nx.draw_networkx_nodes(H, pos, node_color=colors, node_size=1200)
nx.draw_networkx_edges(H, pos)
nx.draw_networkx_labels(H, pos, font_size=9)

plt.title(f"Students taught by {prof_id}")
plt.axis("off")
plt.show()

# ==========================
# 5. INTERACTIVE visualization
# ==========================
net = Network(height="700px", width="100%")
net.from_nx(H)
net.show("complex_query.html")
