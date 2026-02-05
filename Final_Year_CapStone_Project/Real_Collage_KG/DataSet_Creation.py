import pandas as pd
import random

# ==========================
# Students
# ==========================
students = []
departments = ["CSE", "MECH"]

for i in range(1, 101):
    dept = random.choice(departments)
    student_id = f"VU22{dept}N03{str(i).zfill(5)}"
    students.append([
        student_id,
        random.choice(["Aman", "Riya", "Karan", "Neha", "Arjun", "Pooja", "Rahul", "Anjali"]),
        dept,
        random.choice([1, 2, 3, 4])
    ])

df_students = pd.DataFrame(students, columns=["student_id", "name", "department", "year"])

# ==========================
# Courses
# ==========================
courses = [
    ("CSE1001", "Programming in C", "CSE"),
    ("CSE1002", "Object Oriented Programming", "CSE"),
    ("CSE2001", "Data Structures", "CSE"),
    ("CSE2002", "Operating Systems", "CSE"),
    ("CSE2003", "Database Management Systems", "CSE"),
    ("CSE3001", "Machine Learning", "CSE"),
    ("CSE3002", "Computer Networks", "CSE"),
    ("CSE3003", "Software Engineering", "CSE"),
    ("CSE4001", "Cloud Computing", "CSE"),
    ("CSE4002", "Artificial Intelligence", "CSE"),
    ("MECH1001", "Engineering Mechanics", "MECH"),
    ("MECH2001", "Thermodynamics", "MECH"),
    ("MECH2002", "Fluid Mechanics", "MECH"),
    ("MECH3001", "Machine Design", "MECH"),
    ("MECH4001", "Robotics", "MECH"),
]

df_courses = pd.DataFrame(courses, columns=["course_id", "course_name", "department"])

# ==========================
# Professors
# ==========================
profs = [
    ("P01", "Dr. Sharma", "CSE"),
    ("P02", "Dr. Rao", "CSE"),
    ("P03", "Dr. Mehta", "MECH"),
    ("P04", "Dr. Singh", "MECH"),
]

df_profs = pd.DataFrame(profs, columns=["prof_id", "name", "department"])

# ==========================
# Registrations
# ==========================
regs = []

for s in df_students["student_id"]:
    enrolled = random.sample(list(df_courses["course_id"]), 4)
    for c in enrolled:
        regs.append([s, c, "2024-Spring", random.choice(["A", "B", "C"])])

df_regs = pd.DataFrame(regs, columns=["student_id", "course_id", "semester", "grade"])

# ==========================
# Save
# ==========================
df_students.to_csv("students.csv", index=False)
df_courses.to_csv("courses.csv", index=False)
df_profs.to_csv("professors.csv", index=False)
df_regs.to_csv("registrations.csv", index=False)

print("Realistic college dataset created!")
