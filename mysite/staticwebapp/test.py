def mywrapper(func):
    def checker(a, b):
        if a < 0:
            print "a < 0"
            a = 0
        if b < 0:
            print "b < 0"
            b = 0
        ret = func(a, b)
        if ret <= 0:
            print "ret < 0"
            ret = 0
        return ret
    return checker

@mywrapper
def add(a, b):
    print "in add"
    return a+b

def sub(a, b):
    print "in sub"
    return a-b

#add = wrapper(add)
#sub = wrapper(sub)

print add(-2, -3)
