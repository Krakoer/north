from enum import auto, Enum
import subprocess
import sys
from sim import simulate
from com import compile_prg
from lex import load_prg_from_file


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
        call_cmd(["vasm", "output.s",  "-wdc02", "-Fbin", "-dotdir", "-chklabels", "-o", "rom.bin"])
    elif subcommand == "up":
        compile_prg(prg)
        call_cmd(["vasm", "output.s",  "-wdc02", "-Fbin", "-dotdir", "-chklabels", "-o", "rom.bin"])
        call_cmd(["minipro", "-p", "AT28C256", "-w", "rom.bin"])
    
    else:
        print("Unknown subcommand")
        print_help()
        exit()