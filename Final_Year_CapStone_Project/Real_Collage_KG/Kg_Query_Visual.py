# import networkx as nx
# import matplotlib.pyplot as plt

# # ==========================
# # Load KG
# # ==========================
# G = nx.read_graphml("student_kg.graphml")

# print("KG loaded")
# print("Nodes:", len(G.nodes()))
# print("Edges:", len(G.edges()))
# print("=" * 50)

# # ==========================
# # Pick ONE student automatically
# # ==========================
# student_id = None
# for n, d in G.nodes(data=True):
#     if d.get("label") == "Student":
#         student_id = n
#         break

# # ==========================
# # Pick ONE course automatically
# # ==========================
# course_id = None
# for n, d in G.nodes(data=True):
#     if d.get("label") == "Course":
#         course_id = n
#         break

# print("Using student:", student_id)
# print("Using course:", course_id)

# # ==========================
# # Build subgraph (single-hop)
# # ==========================
# nodes = set()
# edges = []

# # Student -> Course
# for nbr in G.neighbors(student_id):
#     edge = G.get_edge_data(student_id, nbr)
#     if edge.get("relation") == "REGISTERED_FOR":
#         nodes.add(student_id)
#         nodes.add(nbr)
#         edges.append((student_id, nbr))

# # Course -> Professor
# for nbr in G.neighbors(course_id):
#     edge = G.get_edge_data(course_id, nbr)
#     if edge.get("relation") == "TAUGHT_BY":
#         nodes.add(course_id)
#         nodes.add(nbr)
#         edges.append((course_id, nbr))

# # ==========================
# # Create subgraph
# # ==========================
# H = nx.Graph()
# for n in nodes:
#     H.add_node(n, **G.nodes[n])
# for u, v in edges:
#     H.add_edge(u, v)

# print("Subgraph nodes:", H.nodes())
# print("Subgraph edges:", H.edges())

# # ==========================
# # Draw SIMPLE graph
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
# nx.draw_networkx_labels(H, pos, font_size=8)

# plt.title("Simple Single-Hop KG Query Map")
# plt.axis("off")
# plt.show()




import networkx as nx
import matplotlib.pyplot as plt

# ==========================
# Load KG
# ==========================
G = nx.read_graphml("student_kg.graphml")

print("KG loaded")
print("Nodes:", len(G.nodes()))
print("Edges:", len(G.edges()))
print("=" * 50)

# ==========================
# Pick one student automatically
# ==========================
student_id = None
for n, d in G.nodes(data=True):
    if d.get("label") == "Student":
        student_id = n
        break

print("Using student:", student_id)

# ==========================
# 2-hop traversal
# ==========================
nodes = set([student_id])
edges = []

for course in G.neighbors(student_id):
    e1 = G.get_edge_data(student_id, course)
    if e1.get("relation") != "REGISTERED_FOR":
        continue

    nodes.add(course)
    edges.append((student_id, course))

    # second hop: course -> professor
    for prof in G.neighbors(course):
        e2 = G.get_edge_data(course, prof)
        if e2.get("relation") == "TAUGHT_BY":
            nodes.add(prof)
            edges.append((course, prof))

# ==========================
# Build subgraph
# ==========================
H = nx.Graph()
for n in nodes:
    H.add_node(n, **G.nodes[n])
for u, v in edges:
    H.add_edge(u, v)

print("Subgraph nodes:", H.nodes())
print("Subgraph edges:", H.edges())

# ==========================
# Draw graph
# ==========================
plt.figure(figsize=(9, 9))
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
nx.draw_networkx_labels(H, pos, font_size=8)

plt.title("2-Hop KG Query: Student → Course → Professor")
plt.axis("off")
plt.show()
