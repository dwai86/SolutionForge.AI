'''
Given the names and grades for each student in a class of  students, store them in a nested list and print the name(s) of any student(s) having the second lowest grade.

Note: If there are multiple students with the second lowest grade, order their names alphabetically and print each name on a new line.
'''

if __name__ == '__main__':
    d ={}
    for _ in range(int(input())):
        name = input()
        score = float(input())
        d[name] = score
    
    l_scores = [i for i in d.values()]
    l_scores_sorted = sorted(l_scores, reverse = False)
    
    highest = l_scores_sorted[0]
    
    for i in l_scores_sorted:
        if i != highest:
            runner = i 
            break
            
    runner_names = [i for i,j in d.items() if j==runner]
    
    for i in sorted(runner_names):
        print(i)