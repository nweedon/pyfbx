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
from .FBXBase import FBXBase
from .FBXHeader import FBXHeader

class FBXNormals(FBXBase):

	info = { }

	def __init__(self, fbxBits):
		super().__init__(fbxBits)

		self.header = FBXHeader(fbxBits)

		# 'Normals' appears more than once in FBXVersion 7.1
		group = 1 if (self.header.get()["FBXVersion"] == 7100) else 0

		self.info["NormalsCount"] = (int)(self.find_int("Normals", group) / 3)
		self.info["Normals"] = [];

		begin = self.find_position("Normals", group) + 13
		end = self.find_position("IndexToDirect", group)

		if self.header.is_data_compressed():
			data = self.decompress_stream(begin, end)
		else:
			data = self.get_stream(begin, end)
		
		self.info["Normals"] = self.unpack_float3(data, self.info["NormalsCount"])

	def get(self, key=None):
		if key:
			return self.info[key]

		return self.info