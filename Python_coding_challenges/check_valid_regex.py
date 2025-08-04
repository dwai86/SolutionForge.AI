# Enter your code here. Read input from STDIN. Print output to STDOUT
import re

t = int(input())
for i in range(t):
    s = input().strip()
    
    try:
        re.compile(s)
        print(True)
    except re.error:
        print(False)
