n = int(input())
if 2 <= n <= 5:
    students = []
    for i in range(n):
        name = input().strip()
        grade = float(input().strip())
        students.append([name, grade])
    second_grade = sorted(set(student[1] for student in students))
    if len(second_grade) < 2:
        print("Error")
    else:
        grade = second_grade[1]
        result = sorted([student[0] for student in students if student[1] == grade])
        for i in result:
            print(i)
else:
    print("Error")