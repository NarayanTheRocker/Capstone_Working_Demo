import networkx as nx
import matplotlib.pyplot as plt

# ==========================
# Load KG
# ==========================
G = nx.read_graphml("student_kg.graphml")

print("KG loaded")
print("Total nodes:", len(G.nodes()))
print("Total edges:", len(G.edges()))

# ==========================
# Layout (slow but nice)
# ==========================
plt.figure(figsize=(18, 18))
pos = nx.spring_layout(G, seed=42, k=0.5)

# ==========================
# Color by node type
# ==========================
colors = []
for n in G.nodes():
    label = G.nodes[n].get("label")
    if label == "Student":
        colors.append("skyblue")
    elif label == "Course":
        colors.append("lightgreen")
    elif label == "Professor":
        colors.append("orange")
    elif label == "Department":
        colors.append("violet")
    else:
        colors.append("gray")

# ==========================
# Draw graph
# ==========================
nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=500)
nx.draw_networkx_edges(G, pos, alpha=0.3)
nx.draw_networkx_labels(G, pos, font_size=6)

plt.title("Complete College Knowledge Graph")
plt.axis("off")
plt.show()
