'''

a= int(input("first side: "))
b=int(input("second side: "))
print(((a**2)+(b**2))**0.5)


c=int(input("input seconds:"))
a=c//3600
c=c%3600
b=c//60
c=c%60
print(a," ",b," ",c)


a=int(input("input number"))
print("yep" if 10<=a<=50 else "no")


a=int(input())
print((a % 4 == 0 and a % 100 != 0) or a % 400 == 0)


print("Hello, my name Max, and i am 18 y.o.")


a=str(input("input word for uot the half of word"))
length=len(a)
print(a[(length//2-1):(length//2+1)])


a = []
for i in range(3):
    b = int(input())
    a.append(b)

a.pop()
print(a)

a=[]
a=input().split()
a[0], a[-1]=a[-1],a[0]
print(a)
'''

