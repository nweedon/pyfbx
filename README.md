pyfbx
=====

pyfbx is a Python module designed to parse Kaydara/Autodesk's FBX 3D Model file format. I haven't ever really liked the official FBX SDK, so I did some work last year to figure out the most important parts of the FBX data structure. I managed to get a sizable amount of information parsed last year, however, the code wasn't very well written. The code was written in C# previously, but this time I've decided to write it in Python to make it as easy to understand as possible. 

__Note:__ I have C# code prepared for other iterations of the FBX file format, however, I need to write them nicely in Python :) However, I do encourage collaboration from others!

####Prerequisites
* Python 3.3

####Supported Versions
* __Binary:__ 2012
* __ASCII:__ None (yet)

####Converting an FBX File
```
$ python pyFBX.py [path_to_fbx_file]
```
* The will output a JSON file, with its attributes pretty-printed. 
* If you want to work out how to use the Python modules themselves, check out the tests!

####Assets
__Wolf Totem 3D Model:__ Currently used to test against. Credit to [https://www.linkedin.com/in/mooga24](Ricardo Catarino).