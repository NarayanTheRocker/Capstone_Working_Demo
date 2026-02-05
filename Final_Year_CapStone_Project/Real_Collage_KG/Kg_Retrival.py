import networkx as nx

# ==========================
# Load KG
# ==========================
G = nx.read_graphml("student_kg.graphml")

print("KG loaded successfully")
print("Total Nodes:", len(G.nodes()))
print("Total Edges:", len(G.edges()))
print("-" * 60)

# ==========================
# Debug: show sample nodes
# ==========================
print("Sample nodes (first 10):")
for n in list(G.nodes())[:10]:
    print(" ", n)
print("-" * 60)

# ==========================
# Detect a student node safely
# ==========================
student_id = None
for n in G.nodes():
    # student nodes connect to multiple courses
    neighbors = list(G.neighbors(n))
    if len(neighbors) >= 3:
        student_id = n
        break

if student_id is None:
    print("❌ No student node detected")
    exit()

print("Detected student:", student_id)

# ==========================
# Query 1: courses of student
# ==========================
courses = []
for nbr in G.neighbors(student_id):
    courses.append(nbr)

print("\nCourses taken by student:")
for c in courses:
    print(" ", c)

# ==========================
# Detect a course node safely
# ==========================
course_id = None
for n in G.nodes():
    neighbors = list(G.neighbors(n))
    if 10 <= len(neighbors) <= 40:  # courses connect to many students
        course_id = n
        break

if course_id is None:
    print("\n❌ No course node detected")
    exit()

print("\nDetected course:", course_id)

# ==========================
# Query 2: students of course
# ==========================
students = list(G.neighbors(course_id))

print("\nStudents enrolled in course:")
for s in students:
    print(" ", s)

# ==========================
# Query 3: students with grade A
# ==========================
students_A = []

for u, v, data in G.edges(data=True):
    if (u == course_id or v == course_id) and data.get("grade") == "A":
        student = u if v == course_id else v
        students_A.append(student)

print("\nStudents with grade A:")
for s in students_A:
    print(" ", s)

print("\n✅ Queries completed successfully")
