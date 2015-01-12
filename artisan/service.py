'''
Created on Dec 30, 2014

@author: lisong
'''

def getGrade(score):
    scoreGrade = (0, 1, 2, 4, 9, 15, 31, 58, 94, 147, 211, 286, 385, 508, 656, 829, 1026, 1307, 1644, 2037, 2486, 2991, 3608, 4337, 5178, 6131,7196)
    grade = len(scoreGrade) - 1
    while grade >= 0:
        if score >= scoreGrade[grade]:
            return grade
        grade -= 1
    return 0;

for x in range(11):
    print "%s:%s"  % (x, getGrade(x))
for x in range(0, 9000, 10):
    print "%s:%s"  % (x, getGrade(x))