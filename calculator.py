from sys import exit
from string import digits, ascii_letters
from _collections import deque

def sign(args):
    for i in range(len(args)):
        if args[i].startswith("-"):
            if args[i].count("-") % 2 == 0:
                args[i] = args[i].replace("-" * args[i].count("-"), "+")

            else:
                args[i] = args[i].replace("-" * args[i].count("-"), "-")
        elif args[i].startswith("+"):
            if args[i].count("+") > 1:
                args[i] = args[i].replace("+" * args[i].count("+"), "+")

    return args


def subtract_sum(*args):
    if len(args) > 1 and "+" not in args and "-" not in args:
        print("Invalid expression")
        return
    res_except_first = 0
    # print(args)
    for i in range(len(args)):
        if args[i] == "-":
            res_except_first += -1 * int(args[i + 1])
        elif args[i] == "+":
            res_except_first += int(args[i + 1])

    return (int(args[0]) + res_except_first)


def check_cmd(command):
    if command != "/exit" and command != "/help":
        print("Unknown command")
    elif command == "/exit":
        print("Bye!")
        exit()
    elif command == "/help":
        print("""The program calculates the sum, multiplication, division and the subtraction of numbers""")




def add_vars(dic, key, value):
    for k, v in dic.items():
        if value == k:
            value = v


    dic[key] = value
    if dic[key].isalpha():
        print("Invalid assignment")

def use_vars(dic, args):
    for i in range(len(args)):
        if args[i] in dic.keys():
            args[i] = dic[args[i]]
    return args
def check_vars(key, value):
    #print(value)
    for k in key:
        if k.isdigit():
            print("Invalid identifier")
            return False

    if len(value) > 1:
        for d in digits:
            for s in ascii_letters:
                if d in value and s in value or "=" in value:
                    print("Invalid assignment")
                    return False

    return True

def check_precedence(arg, stack_item):
    if arg == "*" or arg == "/":
        if stack_item == "+" or stack_item == "-" or arg != stack_item:
            return True
    else:
        return False

def add_space(args):
    for i in range(len(args)):
        if args[i].startswith("("):
            args[i] = args[i].replace("(", "( ")
        elif args[i].endswith(")"):
            args[i] = args[i].replace(")", " )")
    new_args = " ".join(args)
    return new_args.split()

def check_postfix(*args):
    if ("(" in args and ")" not in args) or ("(" not in args and ")" in args):
        print("Invalid expression")
        return False
    for arg in args:
        if arg.count("*") > 1 or arg.count("/") > 1:
            print("Invalid expression")
            return False
    return True
def turn_postfix(*args):
    result = []
    signs = ["*", "+", "-", "/"]
    stack = deque()
    for arg in args:
        if arg.isdigit() or arg.isalpha():
            #print(1)
            result.append(arg)
        elif (len(stack) == 0 or stack[-1] == "(") and arg in signs:
            #print(2)
            stack.append(arg)
        elif arg in signs and check_precedence(arg, stack[-1]):
            #print(3)
            result.append(stack.pop())
            stack.append(arg)
        elif arg in signs and (arg == stack[-1] or check_precedence(arg, stack[-1]) is False):
            #print(4)
            result.append(stack.pop())
            stack.append(arg)
        elif arg == "(":
            #print(5)
            stack.append(arg)
        elif arg == ")":
            #print(6)
            result.append(stack.pop())
            stack.remove("(")
        else:
            #print(7)
            result.append(arg)
        #print(stack)
    for i in range(len(stack)):
        result.append(stack.pop())
    #print(result)
    return result

def calc_postfix(*args):
    stack = deque()
    for arg in args:
        if arg.isdigit():
            stack.append(arg)
        elif arg.isalpha():
            stack.append(arg)
        elif arg == "+":
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b) + int(a))
        elif arg == "-":
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b) - int(a))
        elif arg == "*":
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b) * int(a))
        elif arg == "/":
            a = stack.pop()
            b = stack.pop()
            stack.append(int(b) // int(a))
    print(stack[-1])

def main():
    var_dict = {}
    while True:
        i = input().split()

        if len(i) == 0:
            continue


        elif i[0].startswith("/"):
            check_cmd(i[0])


        elif i[0].endswith("+"):
            print("Invalid expression")


        elif "=" in "".join(i):
            str_i = "".join(i)
            splitted_str_i = str_i.split("=", 1)
            #print(splitted_str_i)
            if check_vars(splitted_str_i[0], splitted_str_i[1]):
                add_vars(var_dict, splitted_str_i[0], splitted_str_i[1])

        elif len(i) == 1 and i[0].isalpha() and i[0] in var_dict.keys():
            print(var_dict[i[0]])


        elif len(i) == 1 and i[0].isdigit():
            print(i[0])


        elif len(i) == 1 and i[0] not in var_dict.keys():
            print("Unknown variable")

        else:
            try:
                #subtract_sum()
                result = turn_postfix(*add_space(sign(use_vars(var_dict, i))))
                if check_postfix(*result):
                    calc_postfix(*result)
            except ValueError:
                print("Invalid expression")


main()
