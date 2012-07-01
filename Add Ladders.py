#!/usr/bin/env python
"""
Finds empty sections and adds a ladder.
"""
import os, sys
import Tkinter, tkFileDialog
import struct
# local module
try:
	import nbt
except ImportError:
	# nbt not in search path. Let's see if it can be found in the parent folder
	extrasearchpath = os.path.realpath(os.path.join(sys.path[0],os.pardir))
	if not os.path.exists(os.path.join(extrasearchpath,'nbt')):
		raise
	sys.path.append(extrasearchpath)
from nbt.world import WorldFolder
from nbt.nbt import TAG_Compound, TAG_Byte, TAG_Byte_Array, TAG_List

def create_section(x):
        light_data = [0]*2048
        block_data = [0]*4096
        block_data[1911] = 65
        new_section = TAG_Compound()
        new_section.tags.extend([
                TAG_Byte(name = "Y", value = x),
                TAG_Byte_Array(name = "BlockLight"),
                TAG_Byte_Array(name = "Blocks"),
                TAG_Byte_Array(name = "Data"),
                TAG_Byte_Array(name = "SkyLight")
                ])
        new_section["BlockLight"].value = bytearray(buffer(struct.pack('b'*len(light_data), *light_data)))
        new_section["Blocks"].value = bytearray(buffer(struct.pack('b'*len(block_data), *block_data)))
        new_section["Data"].value = bytearray(buffer(struct.pack('b'*len(light_data), *light_data)))
        new_section["SkyLight"].value = bytearray(buffer(struct.pack('b'*len(light_data), *light_data)))
        return new_section

def find_empty(chunk):
        updated = False
        empty_section = []
        empty_section.extend([True, True, True, True, True, True, True, True, True, True, True, True, True, True, True, True])
        highest = 0
        for section in chunk["Sections"]:
                empty_section[section["Y"].value] = False
                highest = section["Y"].value
        x = 0
        while x < highest:
                if empty_section[x]:
                        chunk["Sections"].insert(x, create_section(x))
                        updated = True
                x += 1
        return updated

def process_world(world_folder):
        try:
                world = WorldFolder(world_folder)
        except:
                return
        for region in world.iter_regions():
                print(region.filename)
                chunk_moved = False
                for chunk in region.iter_chunks():
                        if(find_empty(chunk["Level"])):
                                x=chunk["Level"]["xPos"].value
                                z=chunk["Level"]["zPos"].value
                                if x < 0:
                                        while x < 0:
                                                x += 32
                                elif x > 31:
                                        while x > 31:
                                                x -= 32
                                if z < 0:
                                        while z < 0:
                                                z += 32
                                elif z > 31:
                                        while z > 31:
                                                z -= 32
                                        
                                print("Updating chunk: x: "+str(x)+" z: "+str(z))
                                try:
                                        #print("HERP")
                                        if(region.write_chunk(x,z,chunk)):
                                                chunk_moved = True
                                        #print("DERP")
                                except ValueError as e:
                                        print("ERROR:  Failed to update chunk.")
                                        print(e)
                #if(chunk_moved):
                #        print("Restructuring region file.")
                                        

def main(world_folder):
        try:
                if (os.path.exists(world_folder+"/region")):
                        print("Processing the overworld")
                        process_world(world_folder)
                else:
                        print("Not a valid Minecraft world folder!")
                        return 0
                if (os.path.exists(world_folder+"/DIM-1")):
                        print("Processing the nether")
                        process_world(world_folder+"/DIM-1")

                if (os.path.exists(world_folder+"/DIM1")):
                        print("Processing the end")
                        process_world(world_folder+"/DIM1")

        except KeyboardInterrupt:
		return 75 # EX_TEMPFAIL
	
	return 0 # NOERR


if __name__ == '__main__':
	if (len(sys.argv) == 1):
		try:
                        saveFileDir = os.path.join(os.path.join(os.environ['APPDATA'].decode(sys.getfilesystemencoding()), u".minecraft"), u"saves")
                except:
                        saveFileDir = '.'
		root = Tkinter.Tk()
		root.withdraw()
                world_folder = tkFileDialog.askdirectory(parent=root,initialdir=saveFileDir,title='Please select a directory')
        else:
        	world_folder = sys.argv[1]
	if (not os.path.exists(world_folder)):
		print("No such folder as "+world_folder)
		sys.exit(72) # EX_IOERR
	
	sys.exit(main(world_folder))
