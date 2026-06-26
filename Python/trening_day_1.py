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

prices = {"apple": 50, "banana": 80, "orange": 90}  
a=str(input())
if(a in prices):
    print(prices.get(a))
else:
    print(0)



game_map = {(0, 0): "Старт", (1, 2): "Скриня з золотом", (3, 3): "Монстр"}
b=input().split()
a=(int(b[0]),int(b[1]))
print(game_map.get(a,"empty coloum"))

a=str(input())
b=set(a)
print(b)
print(len(b))


a=set(input().split())
b=set(input().split())
b={a[0]}
c=set(a[1])

common_friends=a&b
only_max=a-b

print(common_friends)
print(only_max)

a=input().split()
b=int(a)
for i in b:
    b[i],b[len(b)-i]=b[len(b)-i],b[i]
print(b)


b=[int(x) for x in input().split()]
print(b)
x=len(b)-1
y=0
while x>y:
    b[x],b[y]=b[y],b[x]
    y+=1
    x-=1
    #print(b[x],b[y])
print(b)


a=str(input())
print(a[::-1])


import sys
a=str(input())

x=len(a)-1
y=0

while x>y:
    if a[x]!=a[y]:
        print("it`s no palindrom")
        sus.exit(0)
    x-=1
    y+=1
print("palindrom")

'''


