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

class FBXVertices(FBXBase):

	info = { }

	def __init__(self, fbxBits):
		super().__init__(fbxBits)

		self.header = FBXHeader(fbxBits)

		self.read_vertices()
		self.read_vertex_indices()
		self.read_edges()

	def get(self, key=None):
		if key:
			return self.info[key]

		return self.info

	def read_vertices(self):
		self.info["VertexCount"], self.info["Vertices"] = self.parse_section("Vertices", "PolygonVertexIndex", self.FLOAT3, lambda count: count/3)

	def read_vertex_indices(self):
		self.info["VertexIndexCount"], self.info["VertexIndices"] = self.parse_section("PolygonVertexIndex", "Edges", self.INT3, lambda count: count/3)

		# Indices are muddled in 2011 and 2013. See https://github.com/nweedon/pyfbx/issues/1
		# for more information
		affectedVersions = [7100, 7300]
		if self.header.get()["FBXVersion"] in affectedVersions:
			for i in range(0, len(self.info["VertexIndices"])):
				vertex = self.info["VertexIndices"][i]
				self.info["VertexIndices"][i] = [vertex[1], (vertex[2] * -1) - 1, (vertex[0] * -1) - 1]

	def read_edges(self):
		self.info["EdgeCount"], self.info["Edges"] = self.parse_section("Edges", "GeometryVersion", self.INT, affected_versions=[7100, 7300])