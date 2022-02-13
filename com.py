from ops import *




def compile_prg(prg):
    assert len(Ops) == 14, "Exhaustive handling of operations in comp"
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
            if op["type"] == Ops.PUSH:
                out.write(f"\t ; -- PUSH {op['value']} -- \n")
                h = hex(op["value"])[2:].rjust(4, '0') ## INT16
                higher_b = h[0:2]
                lower_b = h[2:]
                out.write(f"\tldy #${lower_b}\n")
                out.write(f"\tlda #${higher_b}\n")
                out.write(f"\tjsr PUSH\n")
            
            elif op["type"] == Ops.PLUS:
                out.write(f"\t ; -- PLUS --\n")
                out.write("\tjsr PLUS\n")

            elif op["type"] == Ops.MINUS:
                out.write("\t ; -- MINUS -- \n")
                out.write("\tjsr MINUS\n")

            elif op["type"] == Ops.DUMP:
                out.write("\t ; -- DUMP -- \n")
                out.write("\tjsr LCD__clear_video_ram\n")
                out.write("\tjsr DUMP\n")

            elif op["type"] == Ops.EQUAL:
                out.write("\t ; -- EQUAL -- \n")
                out.write("\tjsr EQ\n")

            elif op["type"] == Ops.IF:
                out.write("\t ; -- IF -- \n")
                
                out.write("\tlda 0, x\n")
                out.write("\tora 1, x\n")
                out.write("\tphp\n")
                out.write("\tPOP\n")
                out.write("\tplp\n")

                assert len(op) >= 2, "Missing end for if statement in compilation"
                out.write(f"\tbeq addr_{op['jmp']}\n")
            
            elif op["type"] == Ops.ELSE:
                out.write("\t ; -- ELSE -- \n")
                out.write(f"\tjmp addr_{op['jmp']}\n")
                out.write(f"addr_{ip}")

            elif op["type"] == Ops.END:
                out.write("\t ; -- END --\n")
                out.write(f"\tjmp addr_{op['jmp']}\n")
                out.write(f"addr_{ip}:\n")

            elif op["type"] == Ops.DUP:
                out.write("\t ; -- DUP -- \n")
                out.write("\tjsr DUP\n")
                
            elif op["type"] == Ops.GT:
                out.write("\t ; -- GREATER -- \n")
                out.write("\tjsr GT\n")

            elif op["type"] == Ops.LT:
                out.write("\t ; -- LESS -- \n")
                out.write("\tjsr LT\n")

            elif op["type"] == Ops.WHILE:
                out.write("\t ; -- WHILE -- \n")
                out.write(f"addr_{ip}:\n")
            elif op["type"] == Ops.DO:
                out.write("\t ; -- DO -- \n")
                out.write("\tlda 1, x\n")
                out.write("\tora 0, x\n")
                out.write("\tphp\n")
                out.write("\tPOP\n")
                out.write("\tplp\n")
                out.write(f"\tbeq addr_{op['jmp']}\n")

            elif op["type"] == Ops.MEM:
                out.write("\t ; -- MEM -- \n")
        


        out.write("loop:\n")
        out.write("\tjmp loop\n\n")
        out.write("\t.org $fffc\n")
        out.write("\tword init\n")
        out.write("\tword $0000\n")