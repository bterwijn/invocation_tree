import invocation_tree as ivt
from decimal import Decimal, ROUND_HALF_UP

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
    return half_up_round(average, 1)
    
def half_up_round(value, digits=0):
    """ High-precision half-up rounding of 'value' to a specified number of 'digits'. """
    return float(Decimal(str(value)).quantize(Decimal(f"1e-{digits}"),
                                              rounding=ROUND_HALF_UP))

def passing_students(avg):
    return [student 
            for student, average in avg.items() 
            if average >= 5.5]

if __name__ == '__main__':
    ivt.gif(filename="students.png")(main)
