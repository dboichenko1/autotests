import random
list_int = [1,2,3,4]
class Custom_error(BaseException):
    pass

try:
    while True:
        inputs = int(input("input int from 1 to 4: "))
        if inputs > len(list_int)-1:
            raise Custom_error
        elif inputs == list_int[random.randint(0,3)]:
            print("nice")
        else:
            print("bad try")
            continue
except Custom_error:
    print("very long input")


