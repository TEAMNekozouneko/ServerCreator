import sys

def is_64bits():
    return sys.maxsize > 2**32

def yncheck(ans: str, d: bool):
    ans2 = ans.lower()
    if ans2 == "yes" or ans2 == "y":
        return True
    if ans2 == "no" or ans2 == "n":
        return False
    else:
        return d if d == None else False

def isSpaceOnly(s):
    for ss in s:
        if (ss != " "):
            return False
    
    return True