.data
temp: 	.word 1

.text
# this file is not actually executable but can sufficiently test different aspects of the lab
random:
    li a0, 7
    li t0, -1
    li x24, 4
    li x25, 4
    li x26, 4
    li x27, 4
    li x28, 4
    li x12, 39

    addi x0, x0, 229 # THIS TELLS THE COMMON.S FILE THAT THE FUNCTION STARTS ON THE NEXT LINE. -----------------------------------------------------------------------------------
tested_Funct: 
    # fake load addresses to make sure the student checked all criteria for the la instruction
    auipc x0, 0x00000
    mul t6, x0, x0
    
    ret
    
    li t3, 7
    # fake load addresses to make sure the student checked all criteria for the la instruction
    auipc x0, 0x00000
    addi x0, t0, 7
    
    la t4, temp
    jal random

    addi x0, x0, 229 # THIS TELLS THE COMMON.S FILE THAT THE FUNCTION STARTS ON THE NEXT LINE. -----------------------------------------------------------------------------------

random2:
	li a0, 8
	li a6, 4
	ret