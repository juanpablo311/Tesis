def power(base,exp,expi=None):
    if expi==None: expi=exp
    if(exp==1):
        return(expi*base)
    if(exp!=1):
        return(base*power(base,exp-1,expi))

print(power(3,4))