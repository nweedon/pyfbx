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

class FBXVertices(FBXBase):

	header = { }

	def __init__(self, fbxBits):
		super().__init__(fbxBits)

		self.readVertices()
		self.readVertexIndices()
		self.readEdges()

	def get(self, key=None):
		if key:
			return self.header[key]

		return self.header

	def readVertices(self):
		self.header["VertexCount"] = (int)(self.findInt("Vertices") / 3)
		self.header["Vertices"] = [];

		decomp = self.decompressStream(	self.findOffset("Vertices").end(0) + 13, 
										self.findOffset("PolygonVertexIndex").start(0))
		
		self.header["Vertices"] = self.unpackFloat3(decomp, self.header["VertexCount"])

	def readVertexIndices(self):
		self.header["VertexIndexCount"] = (int)(self.findInt("PolygonVertexIndex") / 3)
		self.header["VertexIndices"] = [];

		decomp = self.decompressStream( self.findOffset("PolygonVertexIndex").end(0) + 13,
										self.findOffset("Edges").start(0))

		self.header["VertexIndices"] = self.unpackInt3(decomp, self.header["VertexIndexCount"])

	def readEdges(self):
		self.header["EdgeCount"] = (int)(self.findInt("Edges"))
		self.header["Edges"] = ["Not implemented."];