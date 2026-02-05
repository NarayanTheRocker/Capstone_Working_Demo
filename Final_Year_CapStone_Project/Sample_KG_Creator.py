import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Load data
students = pd.read_csv("students.csv")
courses = pd.read_csv("courses.csv")
profs = pd.read_csv("professors.csv")
regs = pd.read_csv("registrations.csv")

G = nx.Graph()

# ---- Add Student nodes ----
for _, row in students.iterrows():
    G.add_node(row["student_id"], label="Student", name=row["name"])

# ---- Add Course nodes ----
# ---- Add Course -> Professor edges ----
for _, course in courses.iterrows():
    prof = profs.sample(1).iloc[0]  # random professor
    G.add_edge(
        course["course_id"],
        prof["prof_id"],
        relation="TAUGHT_BY"
    )


# ---- Add Professor nodes ----
for _, row in profs.iterrows():
    G.add_node(row["prof_id"], label="Professor", name=row["name"])

# ---- Add REGISTRATION edges ----
for _, row in regs.iterrows():
    G.add_edge(
        row["student_id"],
        row["course_id"],
        relation="REGISTERED_FOR",
        semester=row["semester"],
        grade=row["grade"]
    )

# ---- Visualize (small subset) ----
sub_nodes = list(G.nodes())[:25]
H = G.subgraph(sub_nodes)

plt.figure(figsize=(16, 16))

pos = nx.spring_layout(G, seed=42, k=1)

# Color by node type
colors = []
for n in G.nodes():
    label = G.nodes[n].get("label")
    if label == "Student":
        colors.append("skyblue")
    elif label == "Course":
        colors.append("lightgreen")
    elif label == "Professor":
        colors.append("orange")
    else:
        colors.append("gray")

nx.draw_networkx_nodes(G, pos, node_color=colors, node_size=800)
nx.draw_networkx_edges(G, pos, alpha=0.4)
nx.draw_networkx_labels(G, pos, font_size=7)
nx.write_graphml(G, "student_kg.graphml")
print("KG saved successfully!")

plt.show()

plt.show()


