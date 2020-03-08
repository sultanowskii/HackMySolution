a = int(input())
b = int(input())
c = int(input())

if a > b:
    if a > c:
        print(a)
    elif c > a:
        print(c)
else:
    if b > c:
        print(b)
    elif c > b:
        print(c)