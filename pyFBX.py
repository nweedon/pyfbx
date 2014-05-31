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
import sys
import re
import struct
from pyfbx.FBXHeader import FBXHeader
from pyfbx.FBXVertices import FBXVertices
from pyfbx.FBXNormals import FBXNormals
import pprint
import json

def openFile(name):
	print("Opening FBX File...")
	f = open(name, mode='rb')
	return f

def closeFile(f):
	print("Closing FBX File...")
	f.close()

if(__name__ == "__main__"):
	pp = pprint.PrettyPrinter(indent=4, width=40)

	if len(sys.argv) < 2:
		sys.exit("Usage: FBXImporter.py fbx_file");

	f = openFile(sys.argv[1])

	if f:
		# Read the entire file for searching
		fstr = f.read()
		closeFile(f)

		try:
			jsonOut = { }
			fOut = open(sys.argv[1] + '.json', mode='w')

			fbxHeader = FBXHeader(fstr)
			jsonOut["header"] = fbxHeader.get()

			fbxVertices = FBXVertices(fstr)
			jsonOut["mesh"] = fbxVertices.get()

			fbxNormals = FBXNormals(fstr)
			jsonOut["normals"] = fbxNormals.get()

			print("Dumping JSON...")
			fOut.write("/**\n* Autodesk/Kaydara FBX to JSON Conversion Tool\n* Niall Frederick Weedon\n* niallweedon.co.uk\n* github.com/nweedon\n*/\n")
			fOut.write(json.dumps(jsonOut, sort_keys=True, indent=4))

			fOut.close()
		except:
			import traceback, sys
			traceback.print_exc(file=sys.stdout)
		finally:
			print("Finished.")
			sys.exit(-1);