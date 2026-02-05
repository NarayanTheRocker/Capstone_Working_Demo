import networkx as nx
from pyvis.network import Network
import matplotlib.pyplot as plt

# Load KG
G = nx.read_graphml("student_kg.graphml")

print("KG loaded")
print("Nodes:", len(G.nodes()))
print("Edges:", len(G.edges()))



# Get all courses of a student
def get_courses_of_student(student_id):
    courses = []
    for nbr in G.neighbors(student_id):
        if G.nodes[nbr].get("label") == "Course":
            courses.append(G.nodes[nbr].get("name"))
    return courses

print(get_courses_of_student("S001"))

# Get all students of a course
def get_students_of_course(course_id):
    students = []
    for nbr in G.neighbors(course_id):
        if G.nodes[nbr].get("label") == "Student":
            students.append(nbr)
    return students

print(get_students_of_course("C001"))

# Filter by grade (edge property)
def students_with_grade(course_id, grade):
    result = []
    for u, v, data in G.edges(data=True):
        if v == course_id and data.get("grade") == grade:
            result.append(u)
    return result

print(students_with_grade("C001", "A"))


