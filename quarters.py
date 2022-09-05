#define a function that takes a list as its argument and returns a dictionary of lists representing the most precise quarters of the elements in the list
#e.g.quarrters([1,2,3,4,5,6,7,8]) returns {"list1":[1,2],"list2":[3,4],"list3":[5,6],"list4":[7,8]}
def quarters(somelist):
    quarters = {}
    if len(somelist) < 4:
        quarters["list1"] = somelist
        return quarters
    elif len(somelist)%4 == 0:
        q1 = int(len(somelist)/4)
        quarters["list1"] = somelist[:q1]
        quarters["list2"] = somelist[q1:2*q1]
        quarters["list3"] = somelist[2*q1:3*q1]
        quarters["list4"] = somelist[3*q1:4*q1]
        return quarters
    else:
        remainder = len(somelist)%4
        multiple = len(somelist) - remainder
        q1 = int(multiple/4)
        for i in range(1,(q1)+2):
            if i == 1:
                quarters["list1"] = somelist[:q1]
            else:
                quarters["list{0}".format(i)] = somelist[(i-1)*q1:(i*q1)]
        quarters["list{0}".format(q1+2)] = somelist[multiple:]
        return quarters


        