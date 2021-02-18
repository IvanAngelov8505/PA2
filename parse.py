grades = []
with open("test.txt", "r") as f:

    lines = f.readlines()
    counter = 0
    for i in range(25):
        current_grade = f"""('{lines[counter].strip()}', '{lines[counter+2].strip()}', {lines[counter+4].strip()}, '{lines[counter+6].strip()}', CURRENT_DATE, {lines[counter+8].strip()}),\n"""
        grades.append(current_grade)
        counter+=10

    with open("out.txt", "w") as f:
        f.writelines(grades)
