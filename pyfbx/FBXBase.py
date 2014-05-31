'''
Copyright (c) 2014, NIALL FREDERICK WEEDON
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON 
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import re
import struct
import zlib

class FBXBase(object):

	def __init__(self, fbxBits):
		self.bits = fbxBits

	def findOffset(self, search_term):
		return re.search(bytes(search_term, 'ascii'), self.bits)

	def find(self, search_term, length, offset):
		match = self.findOffset(search_term)
		if match:
			index = match.end(0) + offset
			return self.bits[index:index+length]

	def findInt(self, search_term):
		value = self.find(search_term, 4, 1)

		if value != None:
			return struct.unpack("i", value)[0]

		return 0

	def findDouble(self, search_term):
		value = self.find(search_term, 8, 1)

		if value != None:
			return struct.unpack("d", value)[0]

		return 0

	def decompressStream(self, begin, end):
		if self.bits:
			return zlib.decompress(self.bits[begin:end])

	def unpackFloat3(self, decomp, count=1):
		if count == 1:
			return struct.unpack("ddd", decomp[(i*24):(i*24)+24])
		else:
			unpacked = []
			for i in range(0, count):
				x, y, z = struct.unpack("ddd", decomp[(i*24):(i*24)+24])
				unpacked.append([x, y, z])

			return unpacked

	def unpackInt3(self, decomp, count=1):
		if count == 1:
			return struct.unpack("iii", decomp[(i*12):(i*12)+12])
		else:
			unpacked = []
			for i in range(0, count):
				x, y, z = struct.unpack("iii", decomp[(i*12):(i*12)+12])
				unpacked.append([x, y, z])

			return unpacked