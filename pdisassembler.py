import sys


def print_opcode(opcode):
    return f"Opcode: {bin(opcode)[2:]:>7}"


def disassemble_instruction(instruction, ret_return, flag_229):
    # Extract opcode
    opcode = instruction & 0b1111111

    # Decode based on opcode
    if opcode == 0b0110111:
        rd = ((instruction >> 7) & 0b11111)
        imm = ((instruction >> 12) & 0xFFFFFFFF)
        return f"LUI  x{rd}  {imm}"
    elif opcode == 0b0010111:
        rd = ((instruction >> 7) & 0b11111)
        imm = ((instruction >> 12) & 0xFFFFFFFF)
        return f"AUIPC  x{rd}  {imm}"
    elif opcode == 0b1101111:
        rd = ((instruction >> 7) & 0b11111)
        imm = ((instruction >> 12) & 0x80000000 | ((instruction >> 21) & 0x3FF000) | ((instruction >> 20) & 0xFFE) | ((instruction >> 31) & 1))
        return f"JAL  x{rd}  {imm}"
    elif opcode == 0b1100111:
        rd = ((instruction >> 7) & 0b11111)
        rs1 = ((instruction >> 15) & 0b11111)
        imm = ((instruction >> 20) & 0xFFF)
        if (imm == 0 and ret_return):
            return f"ret"
        else:
            return f"JALR  x{rd}  x{rs1}  {imm}"
    elif opcode == 0b1100011:
        # Decode branch instructions (I-format)
        funct3 = (instruction >> 12) & 0b111
        rs1 = ((instruction >> 15) & 0b11111)
        rs2 = ((instruction >> 20) & 0b11111)
        imm = (((instruction >> 8) & 0xF) | ((instruction >> 21) & 0x3E0) | ((instruction << 3) & 0x7E000) | ((instruction >> 31) & 0x100000))
        imm = (imm - (1 << 12)) if imm & (1 << 11) else imm
        return f"{['BEQ', 'BNE', 'BLT', 'BGE', 'BLTU', 'BGEU'][funct3]}  x{rs1}  x{rs2}  {imm}"
    elif opcode == 0b0000011:
        # Decode load instructions (I-format)
        funct3 = (instruction >> 12) & 0b111
        rd = ((instruction >> 7) & 0b11111)
        rs1 = ((instruction >> 15) & 0b11111)
        imm = ((instruction >> 20) & 0xFFF)
        imm = (imm - (1 << 12)) if imm & (1 << 11) else imm
        return f"{['LB', 'LH', 'LW', 'LBU', 'LHU'][funct3]}  x{rd}  x{rs1}  {imm}"
    elif opcode == 0b0100011:
        # Decode store instructions (S-format)
        funct3 = (instruction >> 12) & 0b111
        rs1 = ((instruction >> 15) & 0b11111)
        rs2 = ((instruction >> 20) & 0b11111)
        imm = (((instruction >> 7) & 0x1F) | ((instruction >> 25) & 0xFE0))
        imm = (imm - (1 << 12)) if imm & (1 << 11) else imm
        return f"{['SB', 'SH', 'SW'][funct3]}  x{rs1}  x{rs2}  {imm}"
    elif opcode == 0b0010011:
        # Decode immediate instructions (I-format)
        funct3 = (instruction >> 12) & 0b111
        rd = ((instruction >> 7) & 0b11111)
        rs1 = ((instruction >> 15) & 0b11111)
        imm = (((instruction >> 20) & 0xFFF) | ((instruction >> 31) & 0x800))
        imm = (imm - (1 << 12)) if imm & (1 << 11) else imm
        return f"{['ADDI', 'MV'][funct3]}  x{rd}  x{rs1}  {imm}"
    elif opcode == 0b0110011:
        # Decode R-type instructions
        funct3 = (instruction >> 12) & 0b111
        rd = ((instruction >> 7) & 0b11111)
        rs1 = ((instruction >> 15) & 0b11111)
        rs2 = ((instruction >> 20) & 0b11111)
        funct7 = (instruction >> 25) & 0b1111111

        if funct3 == 0b000 and funct7 == 0b0000000:
            return f"ADD  x{rd}  x{rs1}  x{rs2}"
        elif funct3 == 0b000 and funct7 == 0b0000001:
            return f"MUL  x{rd}  x{rs1}  x{rs2}"
        # Add more cases for other R-type instructions as needed
        else:
            return f"Unknown R-type instruction: {print_opcode(opcode)}"

    elif opcode == 0b1110011:
        return f"ecall"

    else:
        return f"Unknown instruction: {print_opcode(opcode)}"


def disassemble_file(file_path, ret_return, flag_229):
    with open(file_path, 'rb') as file:
        # Read the file as binary
        binary_content = file.read()

        # Flag to determine whether to print lines (229 Flag)
        print_line = False
        
        # Iterate over 4-byte chunks and disassemble each instruction
        for i in range(0, len(binary_content), 4):
            instruction_bytes = binary_content[i:i + 4]

            # If the instruction is less than 4 bytes, pad with zeros
            while len(instruction_bytes) < 4:
                instruction_bytes += b'\x00'

            # Convert bytes to integer (little-endian)
            instruction = int.from_bytes(instruction_bytes, byteorder='little')

            # Disassemble and print the instruction
            instruction_str = disassemble_instruction(instruction, ret_return, flag_229)

            if instruction_str.startswith("ADDI  x0  x0  229"):
                print_line = not print_line
                continue

            if print_line or flag_229:
                print(instruction_str)


def disassemble_single_instruction(instruction):
    # Convert bytes to integer (little-endian)
    instruction = int(instruction, 16)

    # Disassemble and print the instruction
    print(disassemble_instruction(instruction))


def main():
    
    if len(sys.argv) < 3:
        print("")
        print("Usage: python3 pdissambler.py -[OPTIONS] input")
        print("")
        print("\t[OPTIONS]:\n\t -i (singular instruction)\n\t -f (file)\n\t -ret (JALR  x0  x1  0 -> ret)\n\t -no229 (shows all instructions not just ones between addi x0, x0, 229)")
        print("")
        print("\tex. python3 pdisassembler.py -i FF5FF06F")
        print("\tex. python3 pdisassembler.py -f factorial.binary")
        print("")
        exit(1)

    option = sys.argv[1]
    input_arg = sys.argv[2]
    ret_return = 0
    flag_229 = 0 
    
    for i in range(2,len(sys.argv)):
        classifer = sys.argv[i]
        match classifer:
            case "-ret":
                ret_return = 1
            case "-no229":
                flag_229 = 1
            
    if option == '-f':
        disassemble_file(input_arg, ret_return, flag_229)
    elif option == '-i':
        disassemble_single_instruction(input_arg)
    else:
        print("Invalid option. Usage: python3 pdissambler.py -[OPTION] input\n")
        exit(1)


if __name__ == "__main__":
    main()
