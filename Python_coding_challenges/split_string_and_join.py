

def split_and_join(line):
    # write your code here
    list1 = line.split()
    s = "-".join(list1)
    return s

if __name__ == '__main__':
    line = input()
    result = split_and_join(line)
    print(result)