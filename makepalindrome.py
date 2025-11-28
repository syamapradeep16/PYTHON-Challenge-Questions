n = int(input())
l=[]
while(n>0):
    t = int(input())
    name = input()
    l.append(name)
    n-=1
for i in l:
    char_freq = Counter(i)
    c=0
    s=0
    for j in char_freq.values():
        if c == 0 and j%2==1:
            c=1
        elif c==1 and j%2==1:
            s+=1
        elif j%2==1:
            s+=1
    print(s)