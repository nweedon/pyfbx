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
import os
from pytest import fixture
from ..pyfbx.FBXVertices import FBXVertices
from ..pyfbx.FBXNormals import FBXNormals
from ..pyfbx.FBXHeader import FBXHeader

@fixture(autouse=True)
def before():
	# Set up before a test runs
	f = open(os.path.join(os.path.dirname(__file__), 'model/WolfFBX_Binary_2012.fbx'), mode='rb')
	binaryModelData = f.read()
	f.close()
	return { "model_data" : { "binary_2012": binaryModelData } }


def test_vertices(before):
	# Test each instance of model data. Although the reader
	# will eventually parse different FBX file versions, the output
	# should be the same for all of them.
	for data in before['model_data']:
		print("Testing: " + data)
		fbxVertices = FBXVertices(before['model_data'][data])
		jsonOut = fbxVertices.get()
		assert jsonOut["VertexCount"] == 1128
		assert jsonOut["VertexIndexCount"] == 1726
		assert len(jsonOut["VertexIndices"]) == 1726

def test_normals(before):
	# Test each instance of model data. Although the reader
	# will eventually parse different FBX file versions, the output
	# should be the same for all of them.
	for data in before['model_data']:
		print("Testing: " + data)
		fbxNormals = FBXNormals(before['model_data'][data])
		jsonOut = fbxNormals.get()
		assert jsonOut["NormalsCount"] == 5178
		assert len(jsonOut["Normals"]) == 5178

def test_fbx_2012(before):
	print("Testing: binary_2012")
	# Test all information relevant to 2012 FBX files.
	fbxHeader = FBXHeader(before['model_data']['binary_2012'])
	jsonOut = fbxHeader.get()
	assert jsonOut["EncryptionType"] == 0
	assert jsonOut["FBXHeaderVersion"] == 1003
	# 7200 is the version for 2012 FBX files
	assert jsonOut["FBXVersion"] == 7200