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

	def find_count(self, searchTerm):
		"""
		Searches the FBX file for [searchTerm] and returns the number
		of matches.
		"""
		return len(re.findall(bytes(searchTerm, 'ascii'), self.bits))

	def find_position(self, searchTerm, matchNum=0, end=True):
		"""
		Searches the FBX file for [searchTerm], and returns the position at
		which it was found. By default, this function returns the end position 
		of the first match. 
		To override this, provide the relevant optional arguments, [matchNum] and/or [end].
		"""
		match = re.finditer(bytes(searchTerm, 'ascii'), self.bits)
		if match:
			matchCount = self.find_count(searchTerm)
			matchNum = 0 if (matchNum > matchCount - 1) else matchNum
			i = 0

			for m in match:
				if i == matchNum:
					if end:
						return m.end(0)
					else:
						return m.begin(0)
				i += 1

	def find(self, searchTerm, length, offset, matchNum=0):
		"""
		Searches the FBX file for [searchTerm] and returns [length] bytes
		succeeding the position found by find_position, plus [offset]. 
		"""
		index = self.find_position(searchTerm, matchNum) + offset
		return self.bits[index:index+length]

	def find_int(self, searchTerm, group=0):
		"""
		Convenience function for finding the integer value succeeding
		a structure definition, such as 'PolygonVertexIndex'.
		"""
		value = self.find(searchTerm, 4, 1, group)

		if value != None:
			return struct.unpack("i", value)[0]

		return 0

	def find_double(self, searchTerm, group=0):
		"""
		Convenience function for finding the double value succeeding
		a structure definition, such as 'PolygonVertexIndex'.
		"""
		value = self.find(searchTerm, 8, 1, group)

		if value != None:
			return struct.unpack("d", value)[0]

		return 0

	def get_stream(self, begin, end):
		if self.bits:
			return self.bits[begin:end]

	def decompress_stream(self, begin, end):
		if self.bits:
			return zlib.decompress(self.bits[begin:end])

	def unpack_float3(self, decomp, count=1):
		if count == 1:
			return struct.unpack("ddd", decomp[(i*24):(i*24)+24])
		else:
			unpacked = []
			for i in range(0, count):
				x, y, z = struct.unpack("ddd", decomp[(i*24):(i*24)+24])
				unpacked.append([x, y, z])

			return unpacked

	def unpack_int3(self, decomp, count=1):
		if count == 1:
			return struct.unpack("iii", decomp[(i*12):(i*12)+12])
		else:
			unpacked = []
			for i in range(0, count):
				x, y, z = struct.unpack("iii", decomp[(i*12):(i*12)+12])
				unpacked.append([x, y, z])

			return unpacked