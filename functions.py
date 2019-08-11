from bitstring import BitArray

ADD_STALL = 1
FPADD_STALL = 1
SUB_STALL = 1
FPSUB_STALL = 1
MUL_STALL = 1
FPMUL_STALL = 1
DIV_STALL = 1
FPDIV_STALL = 1
S_STALL = 1
EQ_STALL = 1
GT_STALL = 1
AND_STALL = 1
OR_STALL = 1
XOR_STALL = 1
NOR_STALL = 1
LS_STALL = 1

def bit2uint(A):
	return int(A,2)

def bit2int(A):
	b = BitArray(bin=A)  
	return b.int

def int2bit(A):      # For negative numbers ?? write
	b = -1 * A
	c = '{:032b}'.format(b)
	d = str(~(BitArray(bin=c)))
	e = int(d, 16)
	f = e+1
	g = '{:032b}'.format(f)
	return g

# def bit2float(A):    # ?? write 
	

# def float2bit(A, places = 3):    
  
#     whole, dec = str(number).split(".") 
#     whole = int(whole) 
#     dec = int (dec) 
#     res = bin(whole).lstrip("0b") + "."
#     for x in range(places): 
#         whole, dec = str((decimal_converter(dec)) * 2).split(".") 
# 		dec = int(dec) 
#         res += whole 
#     return res 
  
# def decimal_converter(num):  
#     while num > 1: 
#         num /= 10
#     return num 
  
##########################################################################################

def ALU(A, B, Control): # A and B are binary string
	if Control == '00010': # ADD Unsigned
		return '0', '{:032b}'.format(int(A,2) + int(B,2)), ADD_STALL
	if Control == '00001': # ADD
		sum = bit2int(A)+bit2int(B) 
		if(sum >= 0): 
			return '0', '{:032b}'.format(sum), ADD_STALL 
		else: 
			return '0', int2bit(sum), ADD_STALL # if Control == '00010': # FP ADD
	# 	res = (float(A)+float(B))%2**32
	# 	if res >= 2**31:
	# 		return None, res-2**32, FPADD_STALL
	# 	return None, res, FPADD_STALL
	if Control == '00100': # SUB Unsigned
		sub = int(A,2)-int(B,2) 
		if(sub > 0): 
			return '0', '{:032b}'.format(sub), SUB_STALL # assuming A is always > B --
		else: 
			return '0', '{:032b}'.format(2**32 + sub), SUB_STALL 
	if Control == '00011': # SUB
		sub = bit2int(A)-bit2int(B) 
		if(sub >= 0): 
			return '0', '{:032b}'.format(sub), SUB_STALL 
		else: 
			return '0', int2bit(sub), SUB_STALL # if Control == '00101': # FP SUB
	# 	res = (float(A)-float(B))%2**32
	# 	if res >= 2**31:
	# 		return None, res-2**32, FPSUB_STALL
	# 	return None, res, FPSUB_STALL
	if Control == '01101': # MUL Unsigned
		return '0', '{:032b}'.format(int(A,2)*int(B,2)), MUL_STALL 
	if Control == '01100': # MUL
		mul = bit2int(A)*bit2int(B) 
		if(mul >= 0): 
			return '0', '{:032b}'.format(mul), MUL_STALL 
		else: 
			return '0', int2bit(mul), MUL_STALL # if Control == '01000': # FP MUL
	# 	Lo = (A*B)/2**16
	# 	Hi = (A*B)%2**16
	# 	if Lo >= 2**31:
	# 		return None, Lo=Lo-2**32
	# 	if Hi >= 2**31:
	# 		return None, Hi=Hi-2**32
	# 	return None, None, FPMUL_STALL
	if Control == '01011': # DIV Unsigned
		return '0', '{:032b}'.format(int(A,2)/int(B,2)), DIV_STALL 
	if Control == '01010': # DIV
		div = int(A,2)/int(B,2) 
		if(div >= 0): 
			return '0', '{:032b}'.format(div), DIV_STALL 
		else: 
			return '0', int2bit(div), DIV_STALL # if Control == '01011': # FP DIV
	# 	Lo = A/B
	# 	Hi = A%B
	# 	return None, None, FPDIV_STALL
	if Control == '00000': 
		return '0', '{:032b}'.format(0), LS_STALL 
	if Control == '00101': # AND
		d = str(BitArray(bin=A)&BitArray(bin=B)) 
		e = d[2:] 
		return '0', '{:032b}'.format(int(e,2)), AND_STALL 
	if Control == '01000': # NOR
		d = str(~(BitArray(bin=A) | BitArray(bin=B))) 
		e = d[2:] 
		return '0', '{:032b}'.format(int(e, 2)), NOR_STALL 
	if Control == '00110': # OR
		d = str(BitArray(bin=A) | BitArray(bin=B)) 
		e = d[2:] 
		return '0', '{:032b}'.format(int(e, 2)), OR_STALL 
	if Control == '00111': # XOR
		d = str(BitArray(bin=A) ^ BitArray(bin=B)) 
		e = d[2:] 
		return '0', '{:032b}'.format(int(e, 16)), XOR_STALL # if Control == '10000': # SLL
	# 	d = str(BitArray(bin=A) << int(B,2))
	# 	e = d[2:]
	# 	return '0', '{:032b}'.format(int(e)), S_STALL
	# if Control == '10001': # SRL
	# 	d = str(BitArray(bin=A) >> int(B,2))
	# 	e = d[2:]
	# 	return '0', '{:032b}'.format(int(e)), S_STALL
	if Control == '10101': # BEQ
		if(A == B): 
			return '1', '{:032b}'.format(0), EQ_STALL 
		else: 
			return '0', '{:032b}'.format(0), EQ_STALL 
	if Control == '10100': # BNE
		if(A != B): 
			return '1', '{:032b}'.format(0), EQ_STALL 
		else: 
			return '0', '{:032b}'.format(0), EQ_STALL # if Control == '10100': # BLT
	# 	if(A < B):
	# 		return '1', '{:032b}'.format(0), EQ_STALL
	# 	else:
	# 		return '0', '{:032b}'.format(0), EQ_STALL
	# if Control == '10101': # BGT
	# 	if(A > B):
	# 		return '1', '{:032b}'.format(0), EQ_STALL
	# 	else:
	# 		return '0', '{:032b}'.format(0), EQ_STALL
	# if Control == '10110': # BLE
	# 	if(A <= B):
	# 		return '1', '{:032b}'.format(0), EQ_STALL
	# 	else:
	# 		return '0', '{:032b}'.format(0), EQ_STALL
	# if Control == '10111': # BGE
	# 	if(A >= B):
	# 		return '1', '{:032b}'.format(0), EQ_STALL
	# 	else:
	# 		return '0', '{:032b}'.format(0), EQ_STALL


def MUX(A, B, Control):
	if bit2uint(Control) == 1:
		return B
	return A

def MUX4(A, B, C, D, Control1, Control2, Control3):
	if bit2uint(Control1) == 1:
		return B
	if bit2uint(Control2) == 1:
		return C
	if bit2uint(Control3) == 1:
		return D
	return A

def Control(Opcode):
	control = '000000000'

    
	if Opcode == '000000':          # R type instruction
		control = '100100011'
	elif Opcode == '110001':        # lw instruction
		control = '011110000'
	elif Opcode == '110101':        # sw instrction
		control = '010001000'       
	elif Opcode == '001000':		# beq instruction
		control = '000000110'
	elif Opcode == '101000':		# bne instruction
		control = '000000101'		
	elif Opcode == '000100' or Opcode == '100100' or Opcode == '001100' or Opcode == '101100' or Opcode == '011100':		# addi
		control = '010100011'
	# elif Opcode == '010000':			# j
	# 	control = '000000100'
	# elif Opcode == '100100':		# addiu
	# 	control = '010100001'
	# elif Opcode == '001100':		# andi
	# 	control = '010100001'
	# elif Opcode == '101100':		# ori
	# 	control = '010100001'
	# elif Opcode == '011100':		# xori
	# 	control = '010100001'

	return control[0], control[1], control[2], control[3], control[4], control[5], control[6], control[7], control[8] 

def ShiftLeft(A,N):
	res = A + '0'*N
	return res[-32:]

def SignExtend(A):
	return A[0]*16 + A

def ALUController(funct, ALUOp0, ALUOp1): # gives control for ALU
	alusig = '00000'
	if ALUOp0 == '1' and ALUOp1 == '0':		# bne
		alusig = '10100'
	elif ALUOp0 == '0' and ALUOp1 == '1':	# beq
		alusig = '10101'
	elif ALUOp0 == '0' and ALUOp1 == '0':   # lw sw
		alusig = '00010'
	elif ALUOp0 == '1' and ALUOp1 == '1':
		if funct == '000001':	# add
			alusig = '00001'
		if funct == '100001':	# addu
			alusig = '00010'
		if funct == '010001':	# sub
			alusig = '00011'
		if funct == '110001':	# subu
			alusig = '00100'
		if funct == '001001':	# and
			alusig = '00101'
		if funct == '101001':	# or
			alusig = '00110'
		if funct == '011001':	# xor
			alusig = '00111'
		if funct == '111001':	# nor
			alusig = '01000'
		if funct == '000100':	# jr
			alusig = '01001'
		if funct == '010110':	# div
			alusig = '01010'
		if funct == '110110':	# divu
			alusig = '01011'
		if funct == '000110':	# mult
			alusig = '01100'
		if funct == '100110':	# multu
			alusig = '01101'
		if funct == '010010':	# add.d
			alusig = '01110'
		if funct == '110010':	# div.d
			alusig = '01111'
		if funct == '001010':	# mul.d
			alusig = '10000'
		if funct == '101010':	# sub.d
			alusig = '10001'
		if funct == '011010':	# mfhi
			alusig = '10010'
		if funct == '111010':	# mflo
			alusig = '10011'

	return alusig