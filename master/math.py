def recount(inpt):
    temp = ''
    for i in inpt:
        if i in '+-*/^!()':
            temp += ' %s ' % i
        else:
            temp += i

    inpt = temp.split()
    
    temp = []
    for i in range(len(inpt)):
        if inpt[i] == '(':
            temp.append(i)
        elif inpt[i] == ')':
            inpt[temp[-1]] = num_count(inpt[temp[-1]+1:i])
            for j in range(temp[-1],i):
                inpt.pop(temp[-1]+1)
        
    return num_count(inpt)

def num_count(inpt):
    ttt = [inpt.count('/'), inpt.count('*'), inpt.count('^')]
    for i in range(ttt[0]):
        tt = inpt.index('/')
        inpt[tt-1] = int(inpt[tt-1]) / int(inpt[tt+1])
        inpt.pop(tt)
        inpt.pop(tt)
    for i in range(ttt[1]): 
        tt = inpt.index('*')
        inpt[tt-1] = int(inpt[tt-1]) * int(inpt[tt+1])
        inpt.pop(tt)
        inpt.pop(tt)
    for i in range(ttt[2]):
        tt = inpt.index('^')
        inpt[tt-1] = int(inpt[tt-1]) ** int(inpt[tt+1])
        inpt.pop(tt)
        inpt.pop(tt)
        
    while len(inpt) != 1:
        if inpt[1] == '+': inpt[0] = int(inpt[0]) + int(inpt[2])
        elif inpt[1] == '-': inpt[0] = int(inpt[0]) - int(inpt[2])
        inpt.pop(1)
        inpt.pop(1)

    return inpt[0] 
    
def isnum(val):
    try:
        float(val)
        return True
    except Exception:
        return False
    
