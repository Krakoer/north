from enum import auto, Enum
import subprocess
import sys

class Ops(Enum):
    PUSH=auto()
    PLUS=auto()
    DUMP=auto()
    MINUS = auto()
    EQUAL = auto()
    IF = auto()
    END = auto()
    ELSE = auto()
    GT = auto()
    LT = auto()
    DUP = auto()
    WHILE = auto()
    DO = auto()

def push(x):
    return (Ops.PUSH, x)

def plus():
    return (Ops.PLUS, )

def dump():
    return (Ops.DUMP, )

def minus():
    return (Ops.MINUS, )

def equal():
    return (Ops.EQUAL, )

def iff():
    return (Ops.IF, )

def elze():
    return (Ops.ELSE, )

def end():
    return (Ops.END, )

def greater():
    return (Ops.GT, )

def less():
    return (Ops.LT, )

def dup():
    return (Ops.DUP, )

def wile():
    return (Ops.WHILE, )

def do():
    return (Ops.DO, )

def simulate(prg):
    stack = []
    ip = 0
    while ip < len(prg):
        assert len(Ops) == 13, "Exhaustive handling of operations in simu"
        op = prg[ip]
        if op[0] == Ops.PLUS:
            a = stack.pop()
            b = stack.pop()
            stack.append(a+b)
        elif op[0] == Ops.DUMP:
            a = stack.pop()
            print(a)
        elif op[0] == Ops.PUSH:
            stack.append(op[1])
        elif op[0] == Ops.MINUS:
            a = stack.pop()
            b = stack.pop() 
            stack.append(b-a)
        elif op[0] == Ops.EQUAL:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a == b))

        elif op[0] == Ops.IF:
            a = stack.pop()
            if a == 0:
                assert len(op) >= 2, "Missing matching end for if"
                ip = op[1]

        elif op[0] == Ops.ELSE:
            assert len(op) >= 2, "Else instruction not linked to end"
            ip = op[1]

        elif op[0] == Ops.END:
            assert len(op) >= 2
            ip = op[1]

        elif op[0] == Ops.DUP:
            a = stack.pop()
            stack.append(a)
            stack.append(a)

        elif op[0] == Ops.GT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a < b))

        elif op[0] == Ops.LT:
            a = stack.pop()
            b = stack.pop()
            stack.append(int(a > b))

        elif op[0] == Ops.DO:
            a = stack.pop()
            if not a:
                ip = op[1]
        elif op[0] == Ops.WHILE:
            pass
        else:
            raise Exception("Unreachable: unknown operand")
        ip+=1

    # Stack non empty warning
    if stack:
        print(f"WARNING : Program finished with {len(stack)} elements on the stack")

def compile_prg(prg):
    assert len(Ops) == 13, "Exhaustive handling of operations in comp"
    with open("output.s", "w") as out:
        out.write("\t.org $8000\n")
        out.write("\tinclude \"io.s\"\n")
        out.write("\tinclude \"stack.s\"\n")
        out.write("\tinclude \"maths.s\"\n")
        out.write("\tinclude \"str.s\"\n")
        out.write("init:                                           ; boot routine, first thing loaded\n")
        out.write("\tldx #$ff                                    ; initialize the stackpointer with 0xff\n")
        out.write("\ttxs\n")
        out.write("\tjsr LCD__initialize\n")
        out.write("\tjsr LCD__clear_video_ram\n")
        out.write("\tldx #0\n")
        out.write("main:\n")

        ##  COMPILATION

        for ip, op in enumerate(prg):
            # PUSH
            if op[0] == Ops.PUSH:
                out.write(f"\t ; -- PUSH {op[1 ]} -- \n")
                h = hex(op[1])[2:].rjust(4, '0') ## INT16
                higher_b = h[0:2]
                lower_b = h[2:]
                out.write(f"\tldy #${lower_b}\n")
                out.write(f"\tlda #${higher_b}\n")
                out.write(f"\tjsr PUSH\n")
            
            elif op[0] == Ops.PLUS:
                out.write(f"\t ; -- PLUS --\n")
                out.write("\tjsr PLUS\n")

            elif op[0] == Ops.MINUS:
                out.write("\t ; -- MINUS -- \n")
                out.write("\tjsr MINUS\n")

            elif op[0] == Ops.DUMP:
                out.write("\t ; -- DUMP -- \n")
                out.write("\tjsr LCD__clear_video_ram\n")
                out.write("\tjsr DUMP\n")

            elif op[0] == Ops.EQUAL:
                out.write("\t ; -- EQUAL -- \n")
                out.write("\tjsr EQ\n")

            elif op[0] == Ops.IF:
                out.write("\t ; -- IF -- \n")
                
                out.write("\tlda 0, x\n")
                out.write("\tora 1, x\n")
                out.write("\tphp\n")
                out.write("\tPOP\n")
                out.write("\tplp\n")

                assert len(op) >= 2, "Missing end for if statement in compilation"
                out.write(f"\tbeq addr_{op[1]}\n")
            
            elif op[0] == Ops.ELSE:
                out.write("\t ; -- ELSE -- \n")
                out.write(f"\tjmp addr_{op[1]}\n")
                out.write(f"addr_{ip}")

            elif op[0] == Ops.END:
                out.write("\t ; -- END --\n")
                out.write(f"\tjmp addr_{op[1]}\n")
                out.write(f"addr_{ip}:\n")

            elif op[0] == Ops.DUP:
                out.write("\t ; -- DUP -- \n")
                out.write("\tjsr DUP\n")
                
            elif op[0] == Ops.GT:
                out.write("\t ; -- GREATER -- \n")
                out.write("\tjsr GT\n")

            elif op[0] == Ops.LT:
                out.write("\t ; -- LESS -- \n")
                out.write("\tjsr LT\n")

            elif op[0] == Ops.WHILE:
                out.write("\t ; -- WHILE -- \n")
                out.write(f"addr_{ip}:\n")
            elif op[0] == Ops.DO:
                out.write("\t ; -- DO -- \n")
                out.write("\tlda 1, x\n")
                out.write("\tora 0, x\n")
                out.write("\tphp\n")
                out.write("\tPOP\n")
                out.write("\tplp\n")
                out.write(f"\tbeq addr_{op[1]}\n")
        


        out.write("loop:\n")
        out.write("\tjmp loop\n\n")
        out.write("\t.org $fffc\n")
        out.write("\tword init\n")
        out.write("\tword $0000\n")

def parse_token(token: list):
    (file_path, row, col, word) = token

    assert len(Ops) == 13, "Exhaustive handling of operations in parsing"
    
    if word.isdigit():
        return push(int(word))
    elif word == "+":
        return plus()
    elif word == "-":
        return minus()
    elif word == ".":
        return dump()
    elif word == "=":
        return equal()
    elif word == "if":
        return iff()
    elif word == "end":
        return end()
    elif word == "else":
        return elze()
    elif word == "dup":
        return dup()
    elif word == ">":
        return greater()
    elif word == "<":
        return less()
    elif word == "while":
        return wile()
    elif word == "do":
        return do()
    else:
        raise Exception(f"Invalid token in \"{file_path}\", line {row+1}:{col+1}: {word}")
        exit(1)

def cross_reference_blocks(prg):
    stack = []
    for ip, op in enumerate(prg):
        assert len(Ops) == 13, "Asserted Ops count in cross reference"
        if op[0] == Ops.IF:
            stack.append(ip)
        elif op[0] == Ops.ELSE:
            if stack:
                if_ip = stack.pop()
                assert prg[if_ip][0] == Ops.IF, "Else used without if statement"
                prg[if_ip] = (Ops.IF, ip) # Say if to jump just after the else instruction
                stack.append(ip)
        elif op[0] == Ops.END:
            if stack:
                block_ip = stack.pop()
                block = prg[block_ip][0]
                if block == Ops.IF or block == Ops.ELSE:
                    prg[block_ip] = (block, ip)
                    prg[ip] = (op[0], ip)
                elif block == Ops.DO:
                    while_ip = stack.pop()
                    prg[block_ip] = (block, ip)
                    prg[ip] = (op[0], while_ip)
                else:
                    raise Exception("Not implemented")
        elif op[0] == Ops.WHILE:
            stack.append(ip)
        elif op[0] == Ops.DO:
            stack.append(ip)

    return prg

def lex_file(path):
    with open(path, 'r') as f:
        for (row, line) in enumerate(f.readlines()):
            for (col, token) in lex_line(line):
                yield (path, row, col, token)

def find_predicate(line, start, predicate):
    while start < len(line) and not predicate(line[start]):
        start +=1

    return start

def find_next_token(line, col):
    return find_predicate(line, col, lambda x : not x.isspace())

def find_end_token(line, col):
    return find_predicate(line, col, lambda x : x.isspace())

def lex_line(line):
    col = find_next_token(line, 0)
    while col < len(line):
        col_end = find_end_token(line, col)
        yield (col, line[col:col_end])
        col = find_next_token(line, col_end)

def load_prg_from_file(path):
    tokens = lex_file(path)
    prg = []
    for t in tokens:
        prg.append(parse_token(t))
    return cross_reference_blocks(prg)

def print_help():
    print(f"Usage : {sys.argv[0]} <SUBCOMMAND> [ARGS]")
    print("SUBCOMMANDS:")
    print("\tsim <file>\tSimulate the prg")
    print("\tcom <file>\tCompile the prg")
    print("\tup\tCompile and uplaod the prg")


def call_cmd(args):
    print(args)
    subprocess.call(args)

if __name__ == "__main__":
    argv = sys.argv
    if len(argv) < 3:
        print("ERR missing arg")
        print_help()
        exit(1)
    
    subcommand = argv[1]
    source_path = argv[2]
    prg = load_prg_from_file(source_path)

    if subcommand == "sim":
        simulate(prg)
    elif subcommand == "com":
        compile_prg(prg)
        call_cmd(["vasm", "output.s",  "-c02", "-Fbin", "-dotdir", "-chklabels", "-o", "rom.bin"])
    elif subcommand == "up":
        compile_prg(prg)
        call_cmd(["vasm", "output.s",  "-c02", "-Fbin", "-dotdir", "-chklabels"])
        call_cmd(["minipro", "-p", "AT28C256", "-w", "a.out"])
    
    else:
        print("Unknown subcommand")
        print_help()
        exit()