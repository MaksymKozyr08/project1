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
a = list(map(int, input().split()))
print(sort_iner(a))

