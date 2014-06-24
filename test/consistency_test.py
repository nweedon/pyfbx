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
from pytest import fixture
from .unit import before
from ..pyfbx.FBXVertices import FBXVertices
from ..pyfbx.FBXNormals import FBXNormals
from ..pyfbx.FBXHeader import FBXHeader
from ..pyfbx.FBXTextures import FBXTextures

def test_vertices_consistency(before):
	# Test each instance of model data. Although the reader
	# will eventually parse different FBX file versions, the output
	# should be the same for all of them.
	for i in range(0, len(before['model_data'])):
		print("Testing: " + before['files'][i])
		fbxVertices = FBXVertices(before['model_data'][i])
		jsonOut = fbxVertices.get()["VertexIndices"]
		# Test first and last values
		assert jsonOut[0] == [84, 88, -7]
		assert jsonOut[len(jsonOut) - 1] == [1123, 1125, -1122]

		jsonOut = fbxVertices.get()["Vertices"]
		assert jsonOut[0] == [4.894176483154297, -5.2721147537231445, 33.48030090332031]
		assert jsonOut[len(jsonOut) - 1] == [27.58094024658203, 0.4144550561904907, 26.248268127441406]

		# 2011 and 2013 export UV's differently to 2012, so we
		# can only check if the format of UVs is consistent for the
		# first entry.
		fbxTextures = FBXTextures(before['model_data'][i])
		jsonOut = fbxTextures.get()["UVIndices"]
		assert jsonOut[0] == [0, 3, 2]

		# Edge and normal values are idempotent per version, but
		# export slightly differently across versions. As such, consistency
		# tests cannot be run against these (until I find out whether there
		# is something in the headers)
		
