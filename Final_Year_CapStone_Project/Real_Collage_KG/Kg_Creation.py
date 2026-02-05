import pandas as pd
import networkx as nx
import random

# ==========================
# Load new realistic dataset
# ==========================
students = pd.read_csv("students.csv")
courses = pd.read_csv("courses.csv")
profs = pd.read_csv("professors.csv")
regs = pd.read_csv("registrations.csv")

G = nx.Graph()

# ==========================
# Add Department nodes
# ==========================
departments = set(students["department"]).union(courses["department"]).union(profs["department"])

for d in departments:
    G.add_node(d, label="Department", name=d)

# ==========================
# Add Student nodes
# ==========================
for _, row in students.iterrows():
    G.add_node(
        row["student_id"],
        label="Student",
        name=row["name"],
        year=row["year"]
    )
    G.add_edge(row["student_id"], row["department"], relation="BELONGS_TO")

# ==========================
# Add Course nodes
# ==========================
for _, row in courses.iterrows():
    G.add_node(
        row["course_id"],
        label="Course",
        name=row["course_name"]
    )
    G.add_edge(row["course_id"], row["department"], relation="OFFERED_BY")

# ==========================
# Add Professor nodes
# ==========================
for _, row in profs.iterrows():
    G.add_node(
        row["prof_id"],
        label="Professor",
        name=row["name"]
    )
    G.add_edge(row["prof_id"], row["department"], relation="WORKS_IN")

# ==========================
# Student -> Course (registrations)
# ==========================
for _, row in regs.iterrows():
    G.add_edge(
        row["student_id"],
        row["course_id"],
        relation="REGISTERED_FOR",
        semester=row["semester"],
        grade=row["grade"]
    )

# ==========================
# Course -> Professor (teaching)
# ==========================
for _, course in courses.iterrows():
    prof = profs[profs["department"] == course["department"]].sample(1).iloc[0]
    G.add_edge(
        course["course_id"],
        prof["prof_id"],
        relation="TAUGHT_BY"
    )

# ==========================
# Save KG offline
# ==========================
nx.write_graphml(G, "student_kg.graphml")
print("✅ New college KG built and saved successfully!")
print("Nodes:", len(G.nodes()))
print("Edges:", len(G.edges()))
