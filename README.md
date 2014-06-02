pyfbx
=====
[![Build Status](https://travis-ci.org/nweedon/pyfbx.svg?branch=master)](https://travis-ci.org/nweedon/pyfbx)

pyfbx is a Python module designed to parse Kaydara/Autodesk's FBX 3D Model file format. I haven't ever really liked the official FBX SDK, so I did some work last year to figure out the most important parts of the FBX data structure. I managed to get a sizable amount of information parsed last year, however, the code wasn't very well written. The code was written in C# previously, but this time I've decided to write it in Python to make it as easy to understand as possible. 

__Note:__ I have C# code prepared for other iterations of the FBX file format, however, I need to write them nicely in Python :) However, I do encourage collaboration from others!

####Prerequisites
* Python 3.2, 3.3 and 3.4

####Supported Versions
* __Binary:__ 2011, 2012, 2013
* __ASCII:__ None (yet)

####Supported Data
* __FBX Header Information__
	* FBXHeaderVersion, FBXVersion, EncryptionType
* __Vertex Information__
	* Vertices, VertexCount, VertexIndexCount, VertexIndices, EdgeCount, Edges
* __Normals Information__
	* NormalsCount, Normals

####Upcoming/Planned Features
* __UV's__
	* UV Coordinates, UVIndex
* __Properties__
	* GlobalProperties, Documents, (more) Header Data, Metadata
* __Animation__
	* Deformers, Bones, Skeleton Hierarchy

####Converting an FBX File
```
$ python pyFBX.py [path_to_fbx_file]
```
* The will output a JSON file, with its attributes pretty-printed. 
* If you want to work out how to use the Python modules themselves, check out the tests!

####Assets
__Wolf Totem 3D Model:__ Currently used to test against. Credit to [Ricardo Catarino](https://www.linkedin.com/in/mooga24).
