import structure
import functions

TC_WB = '0'*128
# stores:
# 	- OP/NOP - 0 bit. If NOP then no operation to be performed
# 	- MemtoReg - 4 bit.
# 		if 1: forward MMdata
# 		else: forward ALUoutput1
# 	- RegWrite - 5 bit. whether to write to WBreg
# 	- MMdata - 64-95 bits. data read from MM in DS
# 	- ALUoutput1 - 96-127 bits. Stores 2nd output of ALU
# 	- WBreg - 58-63 bits. write back register address

DS_TC = '0'*128
# stores:
# 	- OP/NOP - 0 bit. If NOP then no operation to be performed
# 	- WriteBack/ WriteThrough - 1 bit. cache write policy
# 	- MemtoReg - 4 bit.
# 	- RegWrite - 5 bit.
# 	- MemRead - 6 bit. 1 if load operation
# 	- MemWrite - 7 bit. 1 if store operation
# 	- readHit - 8 bit. read hit in d-cache
# 	- writeHit - 9 bit. write hit in d-cache
# 	- MMdata - 64-95 bits. data to be read/written to d-cache
# 	- ALUoutput1/MMaddress - 96-127 bits.
# 	- WBreg - 58-63 bits.

DF_DS = '0'*128
# stores:
# 	- OP/NOP - 0 bit. If NOP then no operation to be performed
# 	- WriteBack/ WriteThrough - 1 bit.
# 	- MemtoReg - 4 bit.
# 	- RegWrite - 5 bit.
# 	- MemRead - 6 bit.
# 	- MemWrite - 7 bit.
# 	- readHit - 8 bit.
# 	- writeHit - 9 bit.
# 	- PC - 16-31 bits.
# 	- MMdata - 64-95 bits. data to be read/written to d-cache
# 	- ALUoutput1/MMaddress - 96-127 bits
# 	- WBreg - 58-63 bits

EX_DF = '0'*128
# stores:
# 	- OP/NOP - 0 bit. If NOP then no operation to be performed
# 	- WriteBack/ WriteThrough - 1 bit.
# 	- MemtoReg - 4 bit.
# 	- RegWrite - 5 bit.
# 	- MemRead - 6 bit.
# 	- MemWrite - 7 bit.
# 	- PC - 16-31 bits. Program counter
# 	- MMdata - 64-95 bits. data to be read/written to d-cache
# 	- ALUoutput1/MMaddress - 96-127 bits
# 	- WBreg - 58-63 bits

RF_EX = '0'*128
# stores:
# 	- OP/NOP - 0 bit. If NOP then no operation to be performed
# 	- WriteBack/ WriteThrough - 1 bit.
# 	- delaySlot - 2-3 bits. User argument for delay slots and their number
# 	- MemtoReg - 4 bit.
# 	- RegWrite - 5 bit.
# 	- MemRead - 6 bit.
# 	- MemWrite - 7 bit.
# 	- ALUsrc - 8 bit. source for ALU input 2
# 	- branch - 9 bit. branch instruction
# 	- ALUcontrol - 10-14 bits. ALU operation
# 	- PC - 16-31 bits. Program counter
# 	- ReadData1 - 32-63 bits
# 	- ReadData2 - 64-95 bits
# 	- SignExtendedImmediate - 96-111 bits.
# 	- WBreg - 112-117 bits

IS_RF = '0'*128
# stores:
# 	- OP/NOP - 0 bit. If NOP then no operation to be performed
# 	- WriteBack/ WriteThrough - 1 bit.
# 	- delaySlot - 2-3 bits.
# 	- Forwarding - 4 bit. User argument for enabling forwarding
# 	- PC - 16-31 bits. Program counter
# 	- Instruction - 32-63 bits. 32-bit instruction

IF_IS = '0'*128
# stores:
# 	- OP/NOP - 0 bit. If NOP then no operation to be performed
# 	- WriteBack/ WriteThrough - 1 bit.
# 	- delaySlot - 2-3 bits.
# 	- Forwarding - 4 bit. User argument for enabling forwarding
# 	- InstrHit - 5 bit. if instruction fetched from i-cache
# 	- PC - 16-31 bits. Program counter
# 	- Instruction - 32-63 bits. 32-bit instruction

#################################################################################################

def Preprocessing():
	global I_MEM

	global I_MEM

	# file1 = open("instruction_memory", "r")

	# line1 = file1.readlines()
	# i1 = 0
	# #charbuf = []
	# for x1 in line1:
	# 	l1 = x1.split()
	# 	#print l[1]
	# 	CharBuf.append(l1[1][::-1])
	# 	i1+=1

	# file1.close()

	for i in range(min(len(CharBuf),I_MEM_size/4)):
		# print i, CharBuf[i]
		I_MEM.write('{:032b}'.format(i*4),CharBuf[i])

	# file2 = open("data_memory", "r")
	# line2 = file2.readlines()

	# for x2 in line2:
	# 	l2 = x2.split()
	# 	MM.write('{:032b}'.format(int(l2[0])), '{:032b}'.format(int(l2[1])))

	# file2.close()

	# file3 = open("mapping_data_memory", "r")
	# line3 = file3.readlines()

	# i = 1
	# for x3 in line3:
	# 	l3 = x3.split()
	# 	Rregs[i] = '{:032b}'.format(int(l3[1]))
	# 	i+=1

	# file3.close()

#################################################################################################

def IF():
	global PC
	global IF_IS

	IF_IS = bytearray(IF_IS)
	if(Stall.stall == 1): # stall check
		if (Stall.initBy > 0): # inititiated by RF, EX, DF, DS, TC, WB
			IF_IS = str(IF_IS)
			print "--" + Stall.type + "stall--IF--"
			return
	# print "PC\t", PC
	# print "DF_DS[16:32]\t", DF_DS[16:32]
	# print "Branch.branch\t", Branch.branch
	PC = functions.MUX(PC,DF_DS[16:32],str(Branch.branch)) # PC as binary string
	print "\nPC: ", int(PC,2)
	if(int(PC,2) >= I_MEM_size or int(PC,2) >= 4*len(CharBuf)): # Check OP/NOP by checking end of instruction memory
		IF_IS[0] = '0'
		IF_IS = str(IF_IS)
		print "--NOP--IF--"
		return

	InstrHit, Instruction = i_Cache.read(functions.bit2uint(PC)) # try to read from i-cache

	# forward relevant data
	IF_IS[0] = '1'
	IF_IS[1] = WriteBack_WriteThrough
	IF_IS[2:4] = delaySlots
	IF_IS[4] = Forwarding
	IF_IS[5] = InstrHit
	IF_IS[16:32] = PC
	IF_IS[32:64] = Instruction
	IF_IS = str(IF_IS)

	_,PC,_ = functions.ALU('0'*16 + PC,'{:032b}'.format(4),'00010') # PC = PC + 4
	PC = PC[-16:]
	if (InstrHit == '1'): print "--i-cache hit--IF--"
	else: print "--i-cache miss--IF--"
	return

#################################################################################################

def IS():
	global IF_IS
	global IS_RF
	global stallNext
	global stalltype
	global stallcycles
	global stallinitBy
	global HazardReg2

	IS_RF = bytearray(IS_RF)
	# print "PC internal IS: ", IF_IS[16:32]
	if(Stall.stall == 1): # stall check
		if (Stall.initBy == 2): # inititiated by IS
			IS_RF[0] = '1'
			IS_RF = str(IS_RF)
			print "--" + Stall.type + "stall--IS--"
			return
		if (Stall.initBy > 2): # inititiated by RF, EX, DF, DS, TC, WB
			IS_RF = str(IS_RF)
			print "--" + Stall.type + "stall--IS--"
			return
	if(Branch.branch and Branch.delaySlots < 3): # branched
		IS_RF[0] = '0'
		IS_RF = str(IS_RF)
		print "--Branched--IS--"
		return
	if(IF_IS[0] == '0'): # Check OP/NOP
		IS_RF[0] = '0'
		IS_RF = str(IS_RF)
		print "--NOP--IS--"
		return
	if(IF_IS[5] == '1'): # i-cache hit
		IS_RF = IF_IS
		print "--i-cache read hit--IS--"
		return

	Instruction = I_MEM.read(IF_IS[16:32])
	IS_RF = bytearray(IF_IS)
	IS_RF[32:64] = Instruction
	if stallNext == 0:
		stallinitBy = 2
		stalltype = "iMEM read stall"
		stallcycles = 2
		stallNext = 1
	HazardReg2 = str(IS_RF)
	IS_RF[0] = '0'
	IS_RF = str(IS_RF)
	print "--iMEM read--IS--"

	i_Cache.write(functions.bit2uint(IF_IS[16:32]), Instruction)
	return

#################################################################################################

def RF():
	global IS_RF
	global RF_EX
	global HazardReg1
	global HazardReg2
	global stallNext

	RF_EX = bytearray(RF_EX)
	if(Stall.stall == 1 and Stall.initBy >= 3): # stall check
		if (Stall.initBy > 3): # inititiated by RF, EX, DF, DS, TC, WB
			RF_EX = str(RF_EX)
			print "--" + Stall.type + "stall--RF--"
			return
		if (Stall.initBy == 3):
			HazardReg2 = IS_RF
			IS_RF = HazardReg1
			print "HazardReg2\t", HazardReg2
			print "IS_RF\t\t", IS_RF
	elif(Branch.branch and Branch.delaySlots < 2): # branched
		RF_EX[0] = '0'
		RF_EX = str(RF_EX)
		print "--Branched--RF--"
		return
	elif(IS_RF[0] == '0'): # Check OP/NOP
		RF_EX[0] = '0'
		RF_EX = str(RF_EX)
		print "--NOP--RF--"
		return
	# initial decode
	Instruction = IS_RF[32:64]
	opcode = Instruction[26:32]
	rs = Instruction[21:26]
	rt = Instruction[16:21]
	rd = Instruction[11:16]
	shamt = Instruction[6:11]
	funct = Instruction[0:6]
	Immediate = Instruction[0:16]

	# checking for integer or float operation
	if ((functions.bit2uint(str(funct)) > 17) and (functions.bit2uint(str(funct)) < 22)):
		rs = '1' + rs
		rt = '1' + rt
		rd = '1' + rd
	else:
		rs = '0' + rs
		rt = '0' + rt
		rd = '0' + rd

	# print rs, rt, rd
	# hazard detection
	stall_EX_DF = bytearray('00')
	stall_DF_DS = bytearray('00')
	stall_DS_TC = bytearray('00')
	stall_TC_WB = bytearray('00')

	# stall_EX_DF[0] = str(int(EX_DF[3]) and int(ALU(EX_DF[58:64],rs,'eq')[0])) # TBD
	# stall_EX_DF[1] = str(int(EX_DF[3]) and int(ALU(EX_DF[58:64],rt,'eq')[0]))
	# stall_DF_DS[0] = str(int(DF_DS[3]) and int(ALU(DF_DS[58:64],rs,'eq')[0]))
	# stall_DF_DS[1] = str(int(DF_DS[3]) and int(ALU(DF_DS[58:64],rt,'eq')[0]))
	# stall_DS_TC[0] = str(int(DS_TC[3]) and int(ALU(DS_TC[58:64],rs,'eq')[0]))
	# stall_DS_TC[1] = str(int(DS_TC[3]) and int(ALU(DS_TC[58:64],rt,'eq')[0]))
	# stall_TC_WB[0] = str(int(TC_WB[3]) and int(ALU(TC_WB[58:64],rs,'eq')[0]))
	# stall_TC_WB[1] = str(int(TC_WB[3]) and int(ALU(TC_WB[58:64],rt,'eq')[0]))

	stall_EX_DF[0] = str(int(EX_DF[0]) and int(EX_DF[5]) and int(EX_DF[58:64]==rs)) # TBD
	stall_EX_DF[1] = str(int(EX_DF[0]) and int(EX_DF[5]) and int(EX_DF[58:64]==rt))
	stall_DF_DS[0] = str(int(DF_DS[0]) and int(DF_DS[5]) and int(DF_DS[58:64]==rs))
	stall_DF_DS[1] = str(int(DF_DS[0]) and int(DF_DS[5]) and int(DF_DS[58:64]==rt))
	stall_DS_TC[0] = str(int(DS_TC[0]) and int(DS_TC[5]) and int(DS_TC[58:64]==rs))
	stall_DS_TC[1] = str(int(DS_TC[0]) and int(DS_TC[5]) and int(DS_TC[58:64]==rt))
	stall_TC_WB[0] = str(int(TC_WB[0]) and int(TC_WB[5]) and int(TC_WB[58:64]==rs))
	stall_TC_WB[1] = str(int(TC_WB[0]) and int(TC_WB[5]) and int(TC_WB[58:64]==rt))

	# print EX_DF[5],DF_DS[5],DS_TC[5],TC_WB[5]
	# print "rs, rt, rd\t", rs, rt, rd
	# print "EX_DF[58:64], DF_DS[58:64], DS_TC[58:64], TC_WB[58:64]\t", EX_DF[58:64], DF_DS[58:64], DS_TC[58:64], TC_WB[58:64]
	# print "hazard\t", stall_EX_DF,stall_DF_DS,stall_DS_TC,stall_TC_WB
	# whether to stall on hazard
	if (opcode == '000000'): # R type operation
		if (functions.bit2uint(str(stall_EX_DF)) > 0): # If just preceding instruction generated hazard
			HazardReg1 = IS_RF
			IS_RF = HazardReg2
			RF_EX[0] = '0'
			RF_EX = str(RF_EX)
			stallNext = 1
			stalltype = "--hazard R-type EX_DF--RF--"
			stallinitBy = 3
			stallcycles = 2
			print "--hazard R-type EX_DF--RF--"
			return
		if (IS_RF[4] == '0' and ((functions.bit2uint(str(stall_DF_DS)) > 0) or (functions.bit2uint(str(stall_DS_TC)) > 0) or (functions.bit2uint(str(stall_TC_WB)) > 0))): # forwarding off
			HazardReg1 = IS_RF
			IS_RF = HazardReg2
			RF_EX[0] = '0'
			RF_EX = str(RF_EX)
			stallNext = 1
			stalltype = "--hazard R-type else--RF--"
			stallinitBy = 3
			stallcycles = 2
			print "--hazard R-type else--RF--"
			return

	if (opcode == '110001' or opcode == '000100' or opcode == '100100' or opcode == '001100' or opcode == '101100' or opcode == '011100'): # load or I type operation
		if ((functions.bit2uint(str(stall_EX_DF)[0]) > 0) or (functions.bit2uint(str(stall_DF_DS)[0]) > 0) or (functions.bit2uint(str(stall_DS_TC)[0]) > 0)): #data not yet fetched
			HazardReg1 = IS_RF
			IS_RF = HazardReg2
			RF_EX[0] = '0'
			RF_EX = str(RF_EX)
			stallNext = 1
			stalltype = "--hazard load-type else--RF--"
			stallinitBy = 3
			stallcycles = 2
			print "--hazard load-type else--RF--"
			return
		if (IS_RF[4] == '0' and (functions.bit2uint(str(stall_TC_WB)[0]) > 0)): # forwarding off
			HazardReg1 = IS_RF
			IS_RF = HazardReg2
			RF_EX[0] = '0'
			RF_EX = str(RF_EX)
			stallNext = 1
			stalltype = "--hazard load-type TC_WB--RF--"
			stallinitBy = 3
			stallcycles = 2
			print "--hazard load-type TC_WB--RF--"
			return

	# get forwarded data if available
	DataSrc1 = functions.MUX(TC_WB[96:128],TC_WB[64:96],TC_WB[4])
	DataSrc2 = functions.MUX(DS_TC[96:128],DS_TC[64:96],DS_TC[4])
	DataSrc3 = functions.MUX(DF_DS[96:128],DF_DS[64:96],DF_DS[4])

	if ((functions.bit2uint(str(funct)) > 17) and (functions.bit2uint(str(funct)) < 22)): 
		Readreg1 = Fregs[functions.bit2uint(str(rs[1:])[::-1])]
		Readreg2 = Fregs[functions.bit2uint(str(rt[1:])[::-1])]
	else:
		Readreg1 = Rregs[functions.bit2uint(str(rs[1:])[::-1])]
		Readreg2 = Rregs[functions.bit2uint(str(rt[1:])[::-1])]

	ReadData1 = functions.MUX4(Readreg1,DataSrc1,DataSrc2,DataSrc3,str(stall_TC_WB)[0],str(stall_DS_TC)[0],str(stall_DF_DS)[0])
	ReadData2 = functions.MUX4(Readreg2,DataSrc1,DataSrc2,DataSrc3,str(stall_TC_WB)[1],str(stall_DS_TC)[1],str(stall_DF_DS)[1])

	# decoding continued
	RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, branch, ALUOp1, ALUOp2 = functions.Control(opcode)

	WBreg = functions.MUX(rt, rd, RegDst)
	# print "Instruction\t", Instruction
	# print "Funct\t ", funct, ALUOp1, ALUOp2 
	ALUcontrol = functions.ALUController(funct, ALUOp1, ALUOp2)

	# print "ALUcontrol\t", ALUcontrol
	IS_RF = HazardReg2
	RF_EX = bytearray(IS_RF)
	RF_EX[0] = '1'
	RF_EX[4] = MemtoReg
	RF_EX[5] = RegWrite
	RF_EX[6] = MemRead
	RF_EX[7] = MemWrite
	RF_EX[8] = ALUSrc
	RF_EX[9] = branch
	RF_EX[10:15] = ALUcontrol
	RF_EX[32:64] = ReadData1
	RF_EX[64:96] = ReadData2
	RF_EX[96:112] = Immediate
	RF_EX[112:118] = WBreg
	RF_EX = str(RF_EX)
	# print "Instruction RF\t", Instruction
	# print "ALUcontrol RF\t", RF_EX[10:15]
	# print "Readreg2 RF\t", Readreg2
	# print "ReadData1 RF\t", ReadData1
	# print "ReadData2 RF\t", ReadData2
	# print "Immediate RF\t", RF_EX[96:112]
	print "--decoded--RF--"
	# print RegDst, ALUSrc, MemtoReg, RegWrite, MemRead, MemWrite, branch, ALUOp1, ALUOp2
	return

#################################################################################################

def EX():
	global RF_EX
	global EX_DF
	global Branch
	global stallNext
	global stalltype
	global stallcycles
	global stallinitBy
	global branchNext

	EX_DF = bytearray(EX_DF)
	if (Stall.stall == 1): # stall check
		# print "\t\t\t STALL check"
		if (Stall.initBy > 4): # inititiated by DF, DS, TC, WB
			EX_DF = str(EX_DF)
			print "--" + Stall.type + "stall--EX--"
			return
		if (Stall.initBy == 4): # inititiated by EX
			if (Stall.cycles < 2):
				EX_DF[0] = '1'
			else:
				Stall.cycles -= 1
				stallNext = 1
			EX_DF = str(EX_DF)
			print "--" + Stall.type + "stall--EX--"
			return
	if(Branch.branch and Branch.delaySlots < 1): # branched
		EX_DF[0] = '0'
		EX_DF = str(EX_DF)
		print "--Branched--EX--"
		return
	if(RF_EX[0] == '0'): # Check OP/NOP
		EX_DF[0] = '0'
		EX_DF = str(EX_DF)
		print "--NOP--EX--"
		return

	# ALU Operation
	Immediate = RF_EX[96:112]
	Immediate = functions.SignExtend(Immediate[::-1])
	immediateShifted = functions.ShiftLeft(Immediate, 2)
	immediateShifted = immediateShifted[::-1]
	_,PC,_ = functions.ALU('0'*32,immediateShifted,'00010')
	PC = PC[::-1]
	ALUinput1 = RF_EX[32:64]
	ALUinput2 = functions.MUX(RF_EX[64:96], immediateShifted, RF_EX[8])
	# print "Immediate\t", immediateShifted
	# print "PC\t", PC
	# print "ALUsrc\t", RF_EX[8]
	print "ALUinput1\t", ALUinput1
	print "ALUinput2\t", ALUinput2
	print "ALUcontrol EX\t", RF_EX[10:15]
	ALUoutput0, ALUoutput1, StallCycles = functions.ALU(ALUinput1, ALUinput2, RF_EX[10:15])

	print "ALUoutput0\t", ALUoutput0
	print "ALUoutput1\t", ALUoutput1
	print "StallCycles\t", StallCycles
	branchNext = int(ALUoutput0) and int(RF_EX[9])
	print "branchNext\t", branchNext
	Branch.delaySlots = functions.bit2uint(RF_EX[2:4])
	
	EX_DF = bytearray(RF_EX)
	if StallCycles > 1:
		stallinitBy = 4
		stalltype = 'EX'
		stallcycles = StallCycles
		stallNext = 1
		EX_DF[0] = '0'

	EX_DF[58:64] = RF_EX[112:118]
	EX_DF[16:32] = PC[-16:]
	EX_DF[64:96] = RF_EX[64:96]
	EX_DF[96:128] = ALUoutput1
	EX_DF = str(EX_DF)

	print "--" + RF_EX[10:15] + "--EX--"
	return

#################################################################################################

def DF():
	global EX_DF
	global DF_DS

	DF_DS = bytearray(DF_DS)
	if(Stall.stall == 1): # stall check
		if (Stall.initBy > 4): # inititiated by DF, DS, TC, WB
			DF_DS = str(DF_DS)
			print "--" + Stall.type + "--DF--"
			return
	if(EX_DF[0] == '0'): # Check OP/NOP
		DF_DS[0] = '0'
		DF_DS = str(DF_DS)
		print "--NOP--DF--"
		return

	if (not (functions.bit2uint(EX_DF[6]) or functions.bit2uint(EX_DF[7]))): # if not MemRead and not MemWrite
		DF_DS = EX_DF
		DF_DS = str(DF_DS)
		print "--no MEM use--DF--"
		return
	if(functions.bit2uint(EX_DF[6])): # MemRead
		ALUoutput1 = functions.bit2uint(EX_DF[96:128])
		readHit, MMdata = d_Cache.read(ALUoutput1)
		DF_DS = bytearray(EX_DF)
		DF_DS[8] = readHit
		DF_DS[64:96] = MMdata
		DF_DS = str(DF_DS)
		if readHit == '1': 
			print "--d-cache read hit--DF--"
		else:
			print "--d-cache read miss--DF--"
		return
	if (functions.bit2uint(EX_DF[7]) and not functions.bit2uint(EX_DF[1])): # MemWrite and WriteBack
		ALUoutput1 = functions.bit2uint(str(EX_DF[96:128]))
		MMdata = str(EX_DF[64:96])
		writeHit, MMaddress, MMdata = d_Cache.write(ALUoutput1, MMdata)
		DF_DS = bytearray(EX_DF)
		DF_DS[9] = writeHit
		DF_DS[96:128] = '{:032b}'.format(MMaddress)
		DF_DS[64:96] = MMdata
		DF_DS = str(DF_DS)
		print "--d-cache WriteBack--DF--"
		return
	if (functions.bit2uint(EX_DF[7])): # MemWrite and WriteThrough
		ALUoutput1 = functions.bit2uint(EX_DF[96:128])
		MMdata = str(EX_DF[64:96])
		writeHit, _, _ = d_Cache.write(ALUoutput1, MMdata)
		DF_DS = bytearray(EX_DF)
		DF_DS[7] = writeHit
		DF_DS = str(DF_DS)
		print "--d-cache WriteThrough--DF--"
		return

#################################################################################################

def DS():
	global DF_DS
	global DS_TC
	global stallNext
	global stalltype
	global stallcycles
	global stallinitBy

	DS_TC = bytearray(DS_TC)
	if (Stall.stall == 1): # stall check
		if (Stall.initBy > 5): # inititiated by DS, TC, WB
			DS_TC[0] = '1'
			DS_TC = str(DS_TC)
			print "--" + Stall.type + "--DS--"
			return
	if(DF_DS[0] == '0'): # Check OP/NOP
		DS_TC[0] = '0'
		DS_TC = str(DS_TC)
		print "--NOP--DS--"
		return

	if (not (functions.bit2uint(DF_DS[6]) or functions.bit2uint(DF_DS[7]))): # if not MemRead and not MemWrite
		DS_TC = str(DF_DS)
		print "--no MEM use--DS--"
		return
	if (functions.bit2uint(DF_DS[6]) and functions.bit2uint(DF_DS[8])): # MemRead and ReadHit
		DS_TC = str(DF_DS)
		print "--d-cache read hit--DS--"
		return
	if (functions.bit2uint(DF_DS[7]) and (not functions.bit2uint(DF_DS[1])) and functions.bit2uint(DF_DS[9])): # MemWrite and WriteBack and WriteHit
		DS_TC = str(DF_DS)
		print "--d-cache write hit--DS--"
		return
	if (functions.bit2uint(DF_DS[6])): # MemRead and not ReadHit
		DS_TC = bytearray(DF_DS)
		MMaddress = str(DF_DS[96:128])
		print MMaddress[::-1]
		DS_TC[64:96] = MM.read(MMaddress[::-1])
		stallinitBy = 6
		stalltype = "MEM read stall"
		stallNext = 1
		stallcycles = 2
		DS_TC[0] = '0'
		DS_TC = str(DS_TC)
		print "--MEM read--DS--", str(DS_TC[64:96])
		return
	if (functions.bit2uint(DF_DS[7])): # MemWrite
		DS_TC = bytearray(DF_DS)
		MMaddress = DF_DS[96:128]
		MMdata = DF_DS[64:96]
		# print MMaddress
		# print MMdata
		MM.write(MMaddress[::-1],MMdata)
		stallinitBy = 6
		stalltype = "MEM write stall"
		stallcycles = 2
		stallNext = 1
		DS_TC[0] = '0'
		DS_TC = str(DS_TC)
		print "--MEM write--DS--"
		return

#################################################################################################

def TC():
	global DS_TC
	global TC_WB

	TC_WB = bytearray(TC_WB)
	if(DS_TC[0] == '0'): # Check OP/NOP
		TC_WB[0] = '0'
		TC_WB = str(TC_WB)
		print "--NOP--TC--"
		return

	if(DS_TC[6] == '0'): # MemRead == 0
		TC_WB = str(DS_TC)
		print "--MemRead false--TC--"
		return
	if (DS_TC[8] == '1'): # readHit == 1
		TC_WB = str(DS_TC)
		print "--readHit--TC--"
		return

	# update d-cache
	MMaddress = functions.bit2uint(DS_TC[96:128])
	MMdata = DS_TC[64:96]
	writeHit, MMaddress, MMdata = d_Cache.write(MMaddress, MMdata)
	if (writeHit == '0'):
		MM.write(MMaddress,MMdata)

	TC_WB = str(DS_TC)
	print "--d-cache update--TC--"
	return

#################################################################################################

def WB():
	global TC_WB

	if(TC_WB[0] == '0'): # Check OP/NOP
		print "--NOP--WB--"
		return
	if(TC_WB[5] == '0'): # RegWrite is false
		print "--RegWrite false--WB--"
		return
	WBaddr = TC_WB[59:64]
	WBaddr = functions.bit2uint(WBaddr[::-1])
	WBdata = functions.MUX(TC_WB[96:128],TC_WB[64:96],TC_WB[4])
	if (TC_WB[58] == '0'): 
		Rregs[WBaddr] = WBdata
	if (TC_WB[58] == '1'): 
		Fregs[WBaddr] = WBdata

	# print "WBaddr\t", WBaddr
	# print "WBdata\t", WBdata
	print "--written--WB--"
	return

#################################################################################################

CharBuf = [] # Char buffer for code
Forwarding = False # Forwarding

Stall = structure.Stall()
stallNext = 0
stallinitBy = 0
stalltype = ''
stallcycles = 0

Branch = structure.Branch()
branchNext = 0

I_MEM_size = 128 # size of instruction memory
MM_size = 1024 # MM size

i_Cache_size = 256
i_Cache_assoc = 4
i_Cache_linesize = 4
d_Cache_size = 128
d_Cache_assoc = 4
d_Cache_linesize = 4

WriteBack_WriteThrough = '1'
Forwarding  ='0'
delaySlots = '00'

Rregs = ['0'*32]*32 # R registers
Fregs = ['0'*32]*32 # F registers

I_MEM = structure.Memory(I_MEM_size) # Instruction MEM
MM = structure.Memory(MM_size) # MM

# i-cache
i_Cache = structure.Cache(i_Cache_size, i_Cache_assoc, i_Cache_linesize)
# d-cache
d_Cache = structure.Cache(d_Cache_size, d_Cache_assoc, d_Cache_linesize)

PC = '0'*16 # Program counter

HazardReg1 = '0'*128
HazardReg2 = '0'*128
#################################################################################################

# Rregs[0] = '01'*16
# Rregs[1] = '10'*16
# Rregs[3] = '0110'*8
# Rregs[4] = '1111'*8
Rregs[6] = '01'*16
Rregs[5] = '01'*16

# print Rregs[0]
# print Rregs[1]
# print Rregs[2]

for i in range(1):
	# CharBuf.append(str(i%10)*32)

	# CharBuf.append("10100000000000001010001100110001")
	# CharBuf.append("00000100000010001000000000000000")
	# CharBuf.append("00000100000000001100000100000000")
	# CharBuf.append("00000100000011000000000100000000")

	# CharBuf.append("11100000000000001010001100110101") # sw
	# CharBuf.append("00010000000000001010001100001000") # BNE
	CharBuf.append("00010000000000001010001100101000") # BEQ
	# CharBuf.append("00100100000111101100000100000000") # and
	# CharBuf.append("0100000000000000000000000010000") # j

# MM.write('{:032b}'.format(20),'{:032b}'.format(1))
# d_Cache.write(671088640, '00000000000000000000000000000001')
	Preprocessing()

# Stall.initBy = 4
# Stall.type = 'test stall'
# stallNext = 1

# Branch.branch = 1
# Branch.delaySlots = 0
# branchNext = 1

# for i in range(33):
# 	print i_Cache.write(i*4, CharBuf[i])

# for j in range(i_Cache.setNo):
# 	for k in  range(i_Cache.sets[j].associativity):
# 		print [[i_Cache.sets[j].lines[k].entries[l].address, i_Cache.sets[j].lines[k].entries[l].value] for l in range(i_Cache.sets[j].lines[k].linesize/4)]
	# print
# print "\nd-cache"
# for j in range(d_Cache.setNo):
# 		for k in  range(d_Cache.sets[j].associativity):
# 			for l in range(d_Cache.sets[j].lines[k].linesize/4):
# 				print d_Cache.sets[j].lines[k].entries[l].address, d_Cache.sets[j].lines[k].entries[l].value

# print "\niMEM"
# I_MEM.printMem()
# print "\nMM"
# MM.printMem()

i = 0
while(i < 2*len(CharBuf) + 16):
	# print "\nPC: ", int(PC,2)
	print "Stall\t", Stall.stall, Stall.initBy, Stall.cycles
	WB()
	print "WB_"
	# print "Stall\t", Stall.stall
	TC()
	print "TC_WB\t", TC_WB, "\t\t", len(TC_WB)
	# print "Stall\t", Stall.stall
	DS()
	print "DS_TC\t", DS_TC, "\t\t", len(DS_TC)
	# print "Stall\t", Stall.stall
	DF()
	print "DF_DS\t", DF_DS, "\t\t", len(DF_DS)
	# print "Stall\t", Stall.stall
	# print "stall: ", Stall.stall, Stall.initBy, Stall.type
	# print "branch: ", Branch.branch, Branch.delaySlots
	EX()
	print "EX_DF\t", EX_DF, "\t\t", len(EX_DF)
	# print "Stall\t", Stall.stall
	RF()
	# print "Stall\t", Stall.stall
	print "RF_EX\t", RF_EX, "\t\t", len(RF_EX)
	# print "MemtoReg\t", RF_EX[4]
	# print "RegWrite\t", RF_EX[5]
	# print "MemRead\t", RF_EX[6]
	# print "MemWrite\t", RF_EX[7]
	# print "ALUsrc\t", RF_EX[8]
	# print "branch\t", RF_EX[9]
	# print "ALUcontrol RF\t", RF_EX[10:15]
	# print "ReadData1\t", RF_EX[32:64]
	# print "ReadData2\t", RF_EX[64:96]
	# print "SignExtendedImmediate\t", RF_EX[96:112]
	# print "WBreg\t", RF_EX[112:118]

	IS()
	print "IS_RF\t", IS_RF, "\t\t", len(IS_RF)
	# print "Stall\t", Stall.stall
	IF()
	print "IF_IS\t", IF_IS, "\t\t", len(IF_IS)
	# print "Stall\t", Stall.stall
	print "\n\n"
	# print "stallNext: ", stallNext
	# print "branchNext: ", branchNext

	Stall.stall = stallNext
	Stall.initBy = stallinitBy
	Stall.type = stalltype
	Stall.cycles = stallcycles
	Branch.branch = branchNext
	stallNext = 0
	branchNext = 0
	# i_Cache.write(i*4, str(i%10)*32)
	i += 1
	# print
	# for j in range(i_Cache.setNo):
	# 	for k in  range(i_Cache.sets[j].associativity):
	# 		for l in range(i_Cache.sets[j].lines[k].linesize/4):
	# 			print i_Cache.sets[j].lines[k].entries[l].address, i_Cache.sets[j].lines[k].entries[l].value

# print "\nd-cache"
# for j in range(d_Cache.setNo):
# 		for k in  range(d_Cache.sets[j].associativity):
# 			for l in range(d_Cache.sets[j].lines[k].linesize/4):
# 				print d_Cache.sets[j].lines[k].entries[l].address, d_Cache.sets[j].lines[k].entries[l].value

# print Rregs[4]
# print Rregs[3]
# print Rregs[15]

# print "register 5 -", Rregs[5]
# for i in range(len(CharBuf)):
# 	print i_Cache.write(functions.bit2uint(PC), CharBuf[i])
# 	print "i-cache status\t",i
# 	for j in range(i_Cache.setNo):
# 		for k in  range(i_Cache.sets[j].associativity):
# 			for l in range(i_Cache.sets[j].lines[k].linesize/4):
# 				print i_Cache.sets[j].lines[k].entries[l].address, i_Cache.sets[j].lines[k].entries[l].value
# 	PC = '{:032b}'.format(functions.bit2uint(PC)+4)
# 	print '\n\n'
# print "\nMM"
# MM.printMem()