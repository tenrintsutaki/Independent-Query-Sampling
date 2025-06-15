import sys

# data = sys.stdin.read().strip().split()
# print(data)



def quick_sort(ls):
    if len(ls) <= 1:
        return ls
    pivot = ls[len(ls)//2]
    left = [x for x in ls if x < pivot]
    middle = [x for x in ls if x == pivot]
    right = [x for x in ls if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

def merge(left,right):
    res = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            res.append(left[i])
            i += 1
        else:
            res.append(right[j])
            j += 1
    res.extend(left[i:])
    res.extend(right[j:])
    return res

def merge_sort(ls):
    if len(ls) <= 1:
        return ls
    mid = len(ls) // 2
    left = merge_sort(ls[:mid])
    right = merge_sort(ls[mid:])
    return merge(left,right)

if __name__ == '__main__':
    ls = list(map(int, sys.stdin.readline().strip().split()))  # 读取第一行
    print(quick_sort(ls))
    print(merge_sort(ls))