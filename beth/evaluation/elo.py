raise NotImplementedError()


A = 1
B = 0.5
C = 2

def expected(A,B,base_elo=400):
    return 1/(1+10**((B-A)/base_elo))

def elo(old,exp,score,k = 32):
    return old + k * (score - exp)

for i in range(10):
    exp = expected(A,B,base_elo = 0.5)
    if i < 8:
        B = elo(B,1-exp,1,k = 0.1)
    else:
        B = elo(B,1-exp,0,k = 0.1)
    
    print(A,B,C)
    
for i in range(10):
    exp = expected(C,B,base_elo = 0.5)
    if i < 2:
        B = elo(B,1-exp,1,k = 0.1)
    else:
        B = elo(B,1-exp,0,k = 0.1)
        

    
    print(A,B,C)