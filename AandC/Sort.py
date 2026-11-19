def binary_sorch(a: list[int],key: int, left: int, right: int)->int:
    while left<right:
        mid=(left+right)//2
        if a[mid]>=key:
            right=mid
        else:
            left=mid+1
    return right
def sort_iner(a: list[int])->list[int]:
    for i in range(1,len(a)):
        key=a[i]
        k=binary_sorch(a,key,0,i)
        for j in range(i, k, -1):
            a[j]=a[j-1]
        a[k]=key
    return a
def dop_to_mege_sort(left: list[int], right: list[int])->list[int]:
    result=[]
    i=0
    j=0
    while i<len(left) and j<len(right):
        if left[i]<=right[j]:
            result.append(left[i])
            i+=1
        else:
            result.append(right[j])
            j+=1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def marge_sort(arr: list[int])->list[int]:
    if len(arr)<=1:
        return arr
    mid=len(arr)//2
    left_part=marge_sort(arr[:mid])
    right_part=marge_sort(arr[mid:])

    return dop_to_mege_sort(left_part, right_part)

def hanoi(k: int, src: str, dst: str, aux: str) -> None:
    if k == 0:
        return
    hanoi(k - 1, src, aux, dst)
    print(f"Диск {k}: {src} -> {dst}")
    hanoi(k - 1, aux, dst, src)


def hanoi(k: int, src:str, dst: str, aux: str)->None:
    if k==0:
        return
    hanoi(k-1,src,aux,dst)
    print(f"Диск {k}: {src} -> {dst}")
    hanoi(k-1,aux,dst,src)

n = int(input())
hanoi(n, "A", "C", "B")
