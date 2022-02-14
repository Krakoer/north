from ops import *

def simulate(prg):
    stack = []
    ip = 0
    while ip < len(prg):
        # assert len(Ops) == 13, "Exhaustive handling of operations in simu"
        op = prg[ip]
        if op["type"] == Ops.PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a+b)
        elif op["type"] == Ops.DUMP:
            a = stack.pop()
            print(a)
        elif op["type"] == Ops.PUSH:
            stack.append(op["value"])
        elif op["type"] == Ops.MINUS:
            a = stack.pop()
            b = stack.pop() 
            stack.append(b-a)
        elif op["type"] == Ops.EQUAL:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b))

        elif op["type"] == Ops.IF:
            a = stack.pop()
            if a == 0:
                assert len(op) >= 2, "Missing matching end for if"
                ip = op["jmp"]

        elif op["type"] == Ops.ELSE:
            assert len(op) >= 2, "Else instruction not linked to end"
            ip = op["jmp"]

        elif op["type"] == Ops.END:
            assert len(op) >= 2
            ip = op["jmp"]

        elif op["type"] == Ops.DUP:
            a = stack.pop()
            stack.append(a)
            stack.append(a)

        elif op["type"] == Ops.GT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a < b))

        elif op["type"] == Ops.LT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a > b))

        elif op["type"] == Ops.DO:
            a = stack.pop()
            if not a:
                ip = op["jmp"]
        elif op["type"] == Ops.WHILE:
            pass
        else:
            raise Exception("Unreachable: unknown operand")
        ip+=1

    # Stack non empty warning
    if stack:
        print(f"WARNING : Program finished with {len(stack)} elements on the stack")