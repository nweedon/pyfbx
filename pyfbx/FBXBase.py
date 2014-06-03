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
	INT3 = 0
	FLOAT3 = 1
	INT = 2

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

	def find_string(self, searchTerm, group=0, encoding='utf-8'):
		"""
		Convenience function for finding the string value succeeding
		a structure definition, such as 'Creator'.
		"""
		length = self.find_int(searchTerm)
		return self.find(searchTerm, length, 5, group).decode(encoding)

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

	def unpack_int(self, decomp, count=1):
		if count == 1:
			return struct.unpack("i", decomp[(i*4):(i*4)+4])
		else:
			unpacked = []
			for i in range(0, count):
				a = struct.unpack("i", decomp[(i*4):(i*4)+4])
				unpacked.append(a[0])

			return unpacked

	def parse_section(self, section, next_section, data_type, count_modifier=None, affected_versions=[7100]):
		"""
		Parse a section of the FBX file. 
		@param section The section of the file to parse_section
		@param next_section The section immediately following section.
		@param data_type Tells the function how to unpack the data (INT3, FLOAT3, INT)
		@param count_modifier Lambda function which affects the read count
		@param affected_versions The version numbers which are affected by duplicate 'keys' in the file
			(i.e.: 'PolygonVertexIndex' appears more than once in versions 7.1 and 7.3)
		@returns [count, unpacked_data]
		"""
		# Change to the second match if the header version of this file is
		# affected by duplicate 'keys'.
		group = 1 if (self.header.get()["FBXVersion"] in affected_versions) else 0

		if not self.header:
			self.header = FBXHeader(self.bits)

		# Get the number of entires
		count = (int)(self.find_int(section, group))

		# Modify the count read, if count_modifer is provided
		if count_modifier:
			count = (int)(count_modifier(count))

		# Calculate the data range
		begin = self.find_position(section, group) + 13
		end = self.find_position(next_section, group)

		# Decompress the stream if the FBX Header version
		# implements zlib compression
		if self.header.is_data_compressed():
			data = self.decompress_stream(begin, end)
		else:
			data = self.get_stream(begin, end)

		# Unpack the data into something useful
		if data_type == self.INT3:
			unpacked = self.unpack_int3(data, count)
		elif data_type == self.FLOAT3:
			unpacked = self.unpack_float3(data, count)
		elif data_type == self.INT:
			unpacked = self.unpack_int(data, count)
		
		return [count, unpacked]