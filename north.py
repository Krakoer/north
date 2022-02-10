from enum import auto, Enum
import subprocess
import sys

class Ops(Enum):
    PUSH=auto()
    PLUS=auto()
    DUMP=auto()
    MINUS = auto()
    EQUAL = auto()
    

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

def simulate(prg):
    stack = []
    for op in prg:
        assert len(Ops) == 5, "Exhaustive handling of operations in simu"
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
        else:
            raise Exception("Unreachable: unknown operand")

def compile_prg(prg):
    with open("output.s", "w") as out:
        out.write("\t.org $8000\n")
        out.write("init:                                           ; boot routine, first thing loaded\n")
        out.write("\tldx #$ff                                    ; initialize the stackpointer with 0xff\n")
        out.write("\ttxs\n")
        out.write("\tjsr LCD__initialize\n")
        out.write("\tjsr LCD__clear_video_ram\n")
        out.write("\tldx #0\n")
        out.write("main:\n")

        ##  COMPILATION

        for op in prg:
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
                out.write("\tjsr DUMP\n")

            elif op[0] == Ops.EQUAL:
                out.write("\t ; -- EQUAL -- \n")
                out.write("\tjsr EQ\n")

                


        out.write("loop:\n")
        out.write("\tjmp loop\n\n")
        out.write("\tinclude \"io.s\"\n")
        out.write("\tinclude \"stack.s\"\n")
        out.write("\tinclude \"maths.s\"\n")
        out.write("\tinclude \"str.s\"\n")
        out.write("\t.org $fffc\n")
        out.write("\tword init\n")
        out.write("\tword $0000\n")

def parse_token(token: list):
    (file_path, row, col, word) = token

    assert len(Ops) == 5, "Exhaustive handling of operations in parsing"
    
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
    else:
        raise Exception(f"Invalid token in \"{file_path}\", line {row+1}:{col+1}: {word}")
        exit(1)

def lex_file(path):
    with open(path, 'r') as f:
        return [(path, row, col, token) for (row, line) in enumerate(f.readlines()) for (col, token) in lex_line(line)]

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
    return prg

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