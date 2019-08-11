import functions

class MemorySlot(object): # an element of memory
	"""docstring for MemorySlot"""
	def __init__(self, address):
		super(MemorySlot, self).__init__()
		self.address = address
		self.value  = '0'*32
		
	def read(self):
		return self.value

	def write(self, value):
		self.value = value

	def readAddr(self):
		return self.address

	def erase(self):
		self.value = '0'*32


class Memory(object): # array of memoryslots
	"""
	docstring for Memory
	size is in multiple of 4
	"""
	def __init__(self, size):
		super(Memory, self).__init__()
		self.size = size
		self.slots = [MemorySlot(i*4) for i in range(size/4)]

	def read(self, address):
		return self.slots[functions.bit2uint(address)/4].read()

	def write(self, address, value):
		self.slots[functions.bit2uint(address)/4].write(value)

	def printMem(self):
		for i in range(self.size/4):
			print "address : ", self.slots[i].readAddr(), "\tvalue : ", self.slots[i].read()

	def erase(self):
		for i in range(self.size/4):
			self.slots[i].erase()

#################################################################################################

class CacheEntry(object):
	"""docstring for CacheEntry"""
	def __init__(self):
		super(CacheEntry, self).__init__()
		self.value  = '0'*32
		self.address = 0

	def read(self, address):
		if (self.address == address):
			return '1', self.value
		return '0', '0'*32

	# def update(self, address, value):
	# 	if (self.address == address):
	# 		self.value = value
	# 		return 1
	# 	return 0

	def write(self, address, value):
		Oldaddr = self.address
		Oldval = self.value
		self.value = value
		self.address = address
		# print "CacheEntry write\tOldaddr:", Oldaddr, "   Oldval:", Oldval, "   self:", (self.address, self.value)
		return Oldaddr, Oldval

	def erase(self):
		self.value = '0'*32
		self.address = 0


class CacheLine(object):
	"""
	docstring for CacheLine
	linesize must be in multiples of 4
	"""
	def __init__(self, linesize):
		super(CacheLine, self).__init__()
		self.linesize = linesize
		self.entries = [CacheEntry() for i in range(linesize/4)]
		self.present = 0
		self.accessed = 0
		self.dirty = 0

	def read(self, address):
		# print "present: ", self.present, "accessed: ", self.accessed, "address: ", address
		if (self.present == 0):
			return '0', '0'*32
		readHit, readVal = self.entries[(address/4)%(self.linesize/4)].read(address)
		if (readHit == '1'):
			self.accessed = 1
		return readHit, readVal

	# def update(self, address, value):
	# 	return self.entries[address%(linesize/4)].update(address, value)

	def write(self, address, value): # returns writeHit, notReplaced, Oldaddress, Oldvalue
		if (self.present == 0):
			self.accessed = 1
			self.present = 1
			self.dirty = 0
			retAddr, retVal = self.entries[(address/4)%(self.linesize/4)].write(address, value)
			# print "cacheline write\tnot present   self:", (self.entries[address%(self.linesize/4)].address, self.entries[address%(self.linesize/4)].value)
			return '1', '1', retAddr, retVal
		if (self.accessed == 0):
			self.accessed = 1
			dirty = self.dirty
			self.dirty = 0
			retAddr, retVal = self.entries[(address/4)%(self.linesize/4)].write(address, value)
			# print "cacheline write\tnot accessed\tretAddr:",retAddr, "   retVal:",retVal, "   self:", (self.entries[address%(self.linesize/4)].address, self.entries[address%(self.linesize/4)].value)
			return '1', str(int(not dirty)), retAddr, retVal
		self.accessed = 0
		# print "cacheline write LRU miss   self:", (self.entries[address%(self.linesize/4)].address, self.entries[address%(self.linesize/4)].value)
		return '0', '0', '0', '0'*32

	def erase(self):
		self.present = 0
		self.accessed = 0


class CacheSet(object):
	"""docstring for CacheSet"""
	def __init__(self, associativity, linesize):
		super(CacheSet, self).__init__()
		self.associativity = associativity
		self.linesize = linesize
		self.lines = [CacheLine(linesize) for i in range(associativity)]

	def read(self, address):
		for i in range(self.associativity):
			readHit, readVal = self.lines[i].read(address)
			# print "read: ", readHit, readVal

			if (readHit == '1'):
				return readHit, readVal
		return '0', '0'*32

	# def update(self, address, value):
	# 	for i in range(self.associativity):
	# 		if self.lines[i].update(address, value):
	# 			return 1
	# 	return 0

	def write(self, address, value):
		writeHit = '0'
		retaddr = None
		retval = None
		i = 0
		
		readHit = '0'
		for i in range(self.associativity):
			readHit, _ = self.lines[i].read(address)
			# print "read: ", readHit, readVal

			if (readHit == '1'):
				self.lines[i].entries[(address/4)%(self.linesize/4)].write(address, value)
				self.lines[i].dirty = 1
				return '1', 0, '0'*32


		while(writeHit == '0'):
			writeHit, notreplaceHit, retaddr, retval = self.lines[i].write(address, value)
			i = (i+1)% self.associativity
		# print "cacheset write\tline:",i, "   self:", (self.lines[i].entries[address%(self.linesize/4)].address, self.lines[i].entries[address%(self.linesize/4)].value)
		# print "cacheset write\tline:",i, replaceHit, retaddr, retval
		return notreplaceHit, retaddr, retval

	def erase(self):
		for i in range(self.associativity):
			self.lines[i].erase()


class Cache(object):
	"""
	docstring for Cache
	size should be multiple of linesize*associativity
	"""
	def __init__(self, size, associativity = 1, linesize = 4):
		super(Cache, self).__init__()
		self.size = size
		self.associativity = associativity
		self.linesize = linesize
		self.setNo = size/(linesize*associativity)
		self.sets = [CacheSet(associativity, linesize) for i in range(self.setNo)]

	def read(self, address):
		return self.sets[(address/self.linesize)%self.setNo].read(address)

	# def update(self, address, value):
	# 	return self.sets[address%self.setNo].update(address, value)

	def write(self, address, value):
		# print "cache write\t", "number of sets:", self.setNo, "   address:", address, "   set:", (address/4)%self.setNo, "   value:", value
		# print "cache write\tself:", (self.sets[(address/4)%self.setNo].lines[i].entries[address%(self.linesize/4)].address, self.sets[(address/4)%self.setNo].lines[i].entries[address%(self.linesize/4)].value)
		return self.sets[(address/self.linesize)%self.setNo].write(address, value)

	def erase(self):
		for i in range(self.setNo):
			self.sets[i].erase()

#################################################################################################

class Stall(object):
	"""docstring for Stall"""
	def __init__(self):
		super(Stall, self).__init__()
		self.stall = 0
		self.initBy = 0
		self.type = ''
		self.cycles = 0

#################################################################################################

class Branch(object):
	"""docstring for Branch"""
	def __init__(self):
		super(Branch, self).__init__()
		self.branch = 0
		self.delaySlots = 0