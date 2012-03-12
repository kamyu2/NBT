#!/usr/bin/env python
"""
Prints the seed of a world.
"""

import locale, os, sys

# local module
try:
	import nbt
except ImportError:
	# nbt not in search path. Let's see if it can be found in the parent folder
	extrasearchpath = os.path.realpath(os.path.join(sys.path[0],os.pardir))
	if not os.path.exists(os.path.join(extrasearchpath,'nbt')):
		raise
	sys.path.append(extrasearchpath)
from nbt.nbt import NBTFile

def main(world_folder):
	filename = os.path.join(world_folder,'level.dat')
	level = NBTFile(filename)
	print level["Data"]["RandomSeed"]
	return 0 # NOERR


if __name__ == '__main__':
	if (len(sys.argv) == 1):
		print "No world folder specified!"
		sys.exit(22) # EINVAL
	world_folder = sys.argv[1]
	if (not os.path.exists(world_folder)):
		print "No such folder as "+filename
		sys.exit(2) # ENOENT
	
	sys.exit(main(world_folder))