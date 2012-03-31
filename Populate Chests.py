#!/usr/bin/env python
"""
Finds and edits the contents of chests 
"""
import locale, os, sys
import Tkinter, tkFileDialog
import random

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
from nbt.nbt import TAG_Compound, TAG_Byte, TAG_Short, TAG_List

def items_from_nbt(nbtlist):
	items = {}	# block_id -> count
	for item in nbtlist:
		id = item['id'].value
		count = item['Count'].value
		if id not in items:
			items[id] = 0
		items[id] += count
	return items
   
def derp_chests(chunk, randomitems):
        updated = False
        for entity in chunk['TileEntities']:
                slot = 0
		if entity["id"].value == "Chest":
                        items = items_from_nbt(entity["Items"])
			if sum(items.values()) == 0:
                                print("empty chest found")
                                itemlist = TAG_List(type=TAG_Compound)
                                for randomitem in randomitems:
                                        if slot < 27:
                                                if random.randrange(0,100) < int(randomitem[3]):
                                                        item = TAG_Compound()
                                                        if int(randomitem[2]) > 127:
                                                                randomitem[2] = '127'
                                                        elif int(randomitem[2]) < 1:
                                                                randomitem[2] = '1'
                                                        item.tags.extend([
                                                                TAG_Byte(name="Count", value=int(randomitem[2])),
                                                                TAG_Byte(name="Slot", value=slot),
                                                                TAG_Short(name="Damage", value=int(randomitem[1])),
                                                                TAG_Short(name="id", value=int(randomitem[0]))
                                                        ])
                                                        itemlist.insert(slot,item)
                                                        slot += 1
                                                        updated = True
                                if updated:
                                        entity["Items"] = itemlist
                                #print("START TEST TEST TEST")
                                #print(entity["Items"].pretty_tree())
                                #print("END TEST TEST TEST")
        return updated

def process_world(world_folder, randomitems):
        try:
                world = WorldFolder(world_folder)
        except:
                return
        for region in world.iter_regions():
                print(region.filename)
                for chunk in region.iter_chunks():
                        if(derp_chests(chunk["Level"], randomitems)):
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
                                        
                                print("Updating chests in chunk: x: "+str(x)+" z: "+str(z))
                                try:
                                        region.write_chunk(x,z,chunk)
                                except ValueError as e:
                                        print("ERROR:  Failed to update chunk.")
                                        print(e)
                                        

def main(world_folder):
        randomfile = open('./RandomItems.txt', 'r')
        randomitems = []
        for line in randomfile:
                if line.count('#') == 0 and len(line) > 4:
                        randomitem = line.split()
                        randomitems.append(randomitem)
        try:
                if (os.path.exists(world_folder+"/region")):
                        print("Processing the overworld")
                        process_world(world_folder, randomitems)
                else:
                        print("Not a valid Minecraft world folder!")
                        return 0
                
                if (os.path.exists(world_folder+"/DIM-1")):
                        print("Processing the nether")
                        process_world(world_folder+"/DIM-1", randomitems)

                if (os.path.exists(world_folder+"/DIM1")):
                        print("Processing the end")
                        process_world(world_folder+"/DIM1", randomitems)
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
