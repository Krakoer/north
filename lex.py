from ops import *


def parse_token(token: list):
    (file_path, row, col, word) = token
    loc = (file_path, row+1, col+1)
    assert len(Ops) == 13, "Exhaustive handling of operations in parsing"
    
    if word.isdigit():
        return {"type": push(), "value": int(word), "loc":loc}
    elif word == "+":
        return {"type": plus(), "loc":loc}
    elif word == "-":
        return {"type": minus(), "loc":loc}
    elif word == "dump":
        return {"type": dump(), "loc":loc}
    elif word == "=":
        return {"type": equal(), "loc":loc}
    elif word == "if":
        return {"type": iff(), "loc":loc}
    elif word == "end":
        return {"type": end(), "loc":loc}
    elif word == "else":
        return {"type": elze(), "loc":loc}
    elif word == "dup":
        return {"type": dup(), "loc":loc}
    elif word == ">":
        return {"type": greater(), "loc":loc}
    elif word == "<":
        return {"type": less(), "loc":loc}
    elif word == "while":
        return {"type": wile(), "loc":loc}
    elif word == "do":
        return {"type": do(), "loc":loc}
    elif word == "mem":
        return {"type": mem(), "loc":loc}
    else:
        raise Exception(f"Invalid token in \"{file_path}\", line {row+1}:{col+1}: {word}")
        exit(1)

def cross_reference_blocks(prg):
    stack = []
    for ip, op in enumerate(prg):
        assert len(Ops) == 13, "Asserted Ops count in cross reference"
        if op["type"] == Ops.IF:
            stack.append(ip)
        elif op["type"] == Ops.ELSE:
            if stack:
                if_ip = stack.pop()
                assert prg[if_ip]["type"] == Ops.IF, "Else used without if statement"
                prg[if_ip]["jmp"] = ip # Say if to jump just after the else instruction
                stack.append(ip)
        elif op["type"] == Ops.END:
            if stack:
                block_ip = stack.pop()
                block_type = prg[block_ip]["type"]
                if block_type == Ops.IF or block_type == Ops.ELSE:
                    prg[block_ip]["jmp"] = ip
                    prg[ip]["jmp"] = ip
                elif block_type == Ops.DO:
                    while_ip = stack.pop()
                    prg[block_ip]["jmp"] = ip
                    prg[ip]["jmp"] = while_ip
                else:
                    raise Exception("Not implemented")
        elif op["type"] == Ops.WHILE:
            stack.append(ip)
        elif op["type"] == Ops.DO:
            stack.append(ip)

    return prg

def lex_file(path):
    with open(path, 'r') as f:
        for (row, line) in enumerate(f.readlines()):
            for (col, token) in lex_line(line.split("//")[0]):
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
        token = line[col:col_end]
        yield (col, token)
        col = find_next_token(line, col_end)

def load_prg_from_file(path):
    tokens = lex_file(path)
    prg = []
    for t in tokens:
        prg.append(parse_token(t))
    return cross_reference_blocks(prg)