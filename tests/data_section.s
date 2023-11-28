.data
Array1:  	.word 1 2 3 4 5 6 7 8 9
Array2:		.word 10 11 12 13 14 15
String: 	.asciz "This is an example string"
Buffer: 	.space 2048
Counter:	.byte 0


.text
function:
	la t0, Array1
	lw t1, 0(t0)
	
	la s2, Array2
	sw t1, 0(s2)
	
	la t6, String
	li t2, 0x65
	sw t2, 0(t6)
	
	la x0, Buffer
	
	la a7, Counter
	lbu ra, 0(a7)
	addi ra, ra, 1
	sb ra, 0(a7)
	
	ret