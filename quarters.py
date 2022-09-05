#define a function that takes a list as its argument and returns a dictionary of lists representing the most precise quarters of the elements in the list
#e.g.quarrters([1,2,3,4,5,6,7,8]) returns {"list1":[1,2],"list2":[3,4],"list3":[5,6],"list4":[7,8]}
def quarters(somelist):
    quarters = {}
    if len(somelist) < 4: #there 4 or fewer elements in the list
        quarters["list1"] = somelist
        return quarters
    elif len(somelist)%4 == 0: #number of elements in the list are divisible by 4
        q1 = int(len(somelist)/4)
        quarters["list1"] = somelist[:q1]
        quarters["list2"] = somelist[q1:2*q1]
        quarters["list3"] = somelist[2*q1:3*q1]
        quarters["list4"] = somelist[3*q1:4*q1]
        return quarters
    else: #number of elements in the list is greater than 4 but is not divisible by 4; therefore, the dictionary will be comprised of 5 separate lists
        remainder = len(somelist)%4
        multiple = len(somelist) - remainder
        q1 = int(multiple/4)
        for i in range(1,6):
            if i == 1:
                quarters["list1"] = somelist[:q1]
            elif i in [2,3,4]:
                quarters["list{0}".format(i)] = somelist[(i-1)*q1:(i*q1)]
            else:
                quarters["list{0}".format(i)] = somelist[(i-1)*q1:]
        return quarters

        