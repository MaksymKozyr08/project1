"""def factorial(n):
    if n==0:
        return 1
    else: 
        return n*factorial(n-1)
b=int(input())
print(factorial(b))


def revers_function(arr):
    for i in range(len(arr)//2):
        arr[i],arr[len(arr)-i-1]=arr[len(arr)-i-1],arr[i]
numbers=list(map(int,input().split()))
revers_function(numbers)
for item in numbers:
    print(item,end= " ")


def left_landslide(arr):
    if not arr:
        return
    dop_element = arr[-1]
    for i in range(len(arr) - 1, 0, -1):
        arr[i]=arr[i-1]
    arr[0]=dop_element

def print_f(arr):
    for i in arr:
        print(i,end=" ")
    print()

def right_landslide(arr):
    dop_element=arr[0]
    for i in range(0,len(arr)-1,1):
        arr[i]=arr[i+1]
    arr[len(arr)-1]=dop_element
    
numbers=list(map(int,input().split()))
print("До зсуву:")
print_f(numbers)

right_landslide(numbers)

print("Після зсуву вправо:")
print_f(numbers)
"""
s=input()
#print(s)
for i in range(len(s)//2):
    if s[i]!=s[len(s)-i-1]:
        print(-1)
        break
    else:
        print("Polidrom")
        break
