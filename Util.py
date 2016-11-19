#Returns the difference between s1 and s2.
#For example if s2 is "aaab" and s1 is "aaa"
#Then it returns +,index of the change (addition).
def differenceBetween(s1, s2):
    if len(s1) == len(s2):
        return [i for i in xrange(len(s2)) if s1[i] != s2[i]][0]
    #this detects additions
    elif len(s1) > len(s2):
        # check if we added into the middle or into the end
        index = [i for i in xrange(len(s2)) if s1[i] != s2[i]]
        if len(index) == 0:
            return ("+", len(s1) - 1, s1[-1])
        else:
            print "right", index
            return ("+", index[0], s1[index[0]])
    #this detects removals
    else:
        # check if we added into the middle or into the end
        index = [i for i in xrange(len(s1)) if s1[i] != s2[i]]
        if len(index) == 0:
            return ("-",(len(s2) - 1), s2[-1])
        else:
            return ("-",index[0], s2[index[0]])