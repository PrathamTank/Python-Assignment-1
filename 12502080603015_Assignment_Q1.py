n = int(input("Enter number of students: "))
k = int(input("Enter value of K (top K students): "))
m = int(input("Enter number of subjects: "))

students = []
semester_students = {}

subject_max = [-1] * m
subject_toppers = [[] for _ in range(m)]

print("\nEnter student details:")
print("Format: enrollment name semester CPI mark1 mark2 ... markM")

for i in range(n):
    print(f"\nStudent {i + 1}:")
    
    data = input("Enter details: ").split()

    enrollment = data[0]
    name = data[1]
    semester = int(data[2])
    cpi = float(data[3])
    marks = list(map(int, data[4:]))

    avg_marks = sum(marks) / m

    # Store record as tuple
    student = (enrollment, name, semester, cpi, marks, avg_marks)
    students.append(student)

    if semester not in semester_students:
        semester_students[semester] = []

    semester_students[semester].append(student)

    for i in range(m):
        if marks[i] > subject_max[i]:
            subject_max[i] = marks[i]
            subject_toppers[i] = [enrollment]

        elif marks[i] == subject_max[i]:
            subject_toppers[i].append(enrollment)

print("\n--- Semester-wise Top K Students ---")

for semester in sorted(semester_students):

    group = semester_students[semester]
    group.sort(key=lambda x: (-x[3], -x[5], x[0]))
    top_k = group[:k]
    enrollments = [student[0] for student in top_k]
    print(f"Semester {semester}: {' '.join(enrollments)}")

print("\n--- Subject-wise Toppers ---")

for i in range(m):
    subject_toppers[i].sort()
    print(f"S{i + 1}: {' '.join(subject_toppers[i])}")