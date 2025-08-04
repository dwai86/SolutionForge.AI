if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())
    l = list(arr)
    sorted_l = sorted(l, reverse=True)
    #print(sorted_l)
    winner = sorted_l[0]
    for i in sorted_l:
        if i == winner:
            pass
        else:
            print(i)
            break

'''
## inputs
5
2 3 6 6 5
'''