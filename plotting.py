import matplotlib.pyplot as plt
from dataclasses import dataclass

scores1 = [45, 40, 38, 29, 36, 15, 49.5, 21, 22.5, 36]

plt.hist(scores1)
# plt.show()

@dataclass
class Student:
    name: str
    score: int

students = [Student("Ada", 96), Student("Babbage", 87),
            Student("Capn", 90), Student("Domino", 50),
            Student("Ellie", 100)]
scores = []
for student in students:
    scores.append(student.score)
plt.hist(scores)
# plt.show()

plt.plot([1,2,3])
plt.plot([1,2,3])
plt.show()