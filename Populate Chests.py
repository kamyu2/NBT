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

def process_entity(entity, randomitems):
        slot = 0
        updated = False
        items = items_from_nbt(entity["Items"])
        if sum(items.values()) == 0:
                print("empty chest found")
                itemlist = TAG_List(type=TAG_Compound)
                for randomitem in randomitems:
                        if slot < 27:
                                if random.randrange(0,100) < int(randomitem[3]):
                                        item = TAG_Compound()
                                        try:
                                                quantity = int(randomitem[2])
                                        except ValueError:
                                                try:
                                                        lowrand, highrand = randomitem[2].split('-')
                                                        quantity = random.randrange(int(lowrand), int(highrand) + 1)
                                                except ValueError:
                                                        print("ERROR: Invalid quantity range.  Defaulting to 1.")
                                                        line = ''
                                                        for section in randomitem:
                                                                line += ' ' + section
                                                        print(line)
                                                        quantity = 1
                                        if quantity > 127:
                                                quantity = 127
                                        elif quantity < 1:
                                                quantity = 1
                                        item.tags.extend([
                                                TAG_Byte(name="Count", value=quantity),
                                                TAG_Byte(name="Slot", value=slot),
                                                TAG_Short(name="Damage", value=int(randomitem[1])),
                                                TAG_Short(name="id", value=int(randomitem[0]))
                                        ])
                                        if len(randomitem) > 4:
                                                enchants = TAG_List(name="ench", type=TAG_Compound)
                                                count = 4
                                                try:
                                                        while len(randomitem) > count:
                                                                enchant = TAG_Compound()
                                                                enchant.tags.extend([
                                                                        TAG_Short(name="id", value=int(randomitem[count])),
                                                                        TAG_Short(name="lvl", value=int(randomitem[count+1]))
                                                                ])
                                                                enchants.insert((count-4)/2,enchant)
                                                                count += 2
                                                        tag = TAG_Compound()
                                                        tag.tags.extend([enchants])
                                                        tag.name = "tag"
                                                        item.tags.extend([tag])
                                                except IndexError:
                                                        print("ERROR: invalid enchant data")
                                                        line = ''
                                                        for section in randomitem:
                                                                line += ' ' + section
                                                        print(line)
                                        itemlist.insert(slot,item)
                                        slot += 1
                                        updated = True
                if updated:
                        entity["Items"] = itemlist
        return updated
                                
def derp_chests(chunk, randomitems):
        updated = False
        for entity in chunk['TileEntities']:
                if entity["id"].value == "Chest":
                        updated = (process_entity(entity, randomitems) or updated)
        for entity in chunk['Entities']:
                if entity["id"].value == "Minecart":
                        if entity["Type"].value == 1:
                                updated = (process_entity(entity, randomitems) or updated)
        return updated

def process_world(world_folder, randomitems):
        try:
                world = WorldFolder(world_folder)
        except:
                return
        for region in world.iter_regions():
                print(region.filename)
                chunk_moved = False
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
                                        #print("HERP")
                                        if(region.write_chunk(x,z,chunk)):
                                                chunk_moved = True
                                        #print("DERP")
                                except ValueError as e:
                                        print("ERROR:  Failed to update chunk.")
                                        print(e)
#                if(chunk_moved):
#                        print("Restructuring region file.")
                                        

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
