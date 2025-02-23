import invocation_tree as invo_tree
import math 

def main():
    students = {'Ann':[7.5, 8.0], 
                'Bob':[4.5, 6.0], 
                'Coy':[7.5, 6.0]}
    averages = {student:compute_average(grades)
                for student, grades in students.items()}
    passing = passing_students(averages)
    print(passing)

def compute_average(grades):
    average = sum(grades)/len(grades)
    return my_round(average, 1)
    
def my_round(value, digits=0):
    shift = 10 ** digits
    return math.floor(value * shift + 0.5) / shift

def passing_students(avg):
    return [student 
            for student, average in avg.items() 
            if average >= 5.5]

if __name__ == '__main__':
    invo_tree.gif(filename="students.png")(main)
