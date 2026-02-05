import random
import pandas as pd

# ----- Basic data -----
students = [f"S{i:03}" for i in range(1, 51)]
courses = [f"C{i:03}" for i in range(1, 11)]
professors = [f"P{i:02}" for i in range(1, 6)]

student_names = ["Aman", "Riya", "Karan", "Neha", "Arjun", "Pooja", "Rahul", "Simran", "Rohit", "Anjali"]
course_names = ["AI", "ML", "DBMS", "OS", "CN", "DSA", "Cloud", "IoT", "CyberSec", "Robotics"]
departments = ["CSE", "ECE", "ME", "IT"]

# ----- Students table -----
students_data = []
for s in students:
    students_data.append([
        s,
        random.choice(student_names),
        random.choice(departments),
        random.choice([1, 2, 3, 4])
    ])

df_students = pd.DataFrame(students_data, columns=["student_id", "name", "department", "year"])

# ----- Courses table -----
courses_data = []
for i, c in enumerate(courses):
    courses_data.append([
        c,
        course_names[i],
        random.choice([3, 4]),
        random.choice(departments)
    ])

df_courses = pd.DataFrame(courses_data, columns=["course_id", "course_name", "credits", "department"])

# ----- Professors table -----
profs_data = []
for p in professors:
    profs_data.append([
        p,
        random.choice(["Dr. Sharma", "Dr. Mehta", "Dr. Rao", "Dr. Singh", "Dr. Das"]),
        random.choice(departments)
    ])

df_profs = pd.DataFrame(profs_data, columns=["prof_id", "name", "department"])

# ----- Registrations (100 rows) -----
registrations = []
for _ in range(100):
    registrations.append([
        random.choice(students),
        random.choice(courses),
        random.choice(["2023-Fall", "2024-Spring"]),
        random.choice(["A", "B", "C", "D"])
    ])

df_reg = pd.DataFrame(registrations, columns=["student_id", "course_id", "semester", "grade"])

# ----- Save CSVs -----
df_students.to_csv("students.csv", index=False)
df_courses.to_csv("courses.csv", index=False)
df_profs.to_csv("professors.csv", index=False)
df_reg.to_csv("registrations.csv", index=False)

print("Dataset created successfully!")
