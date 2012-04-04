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
   
def randomize_Spawners(chunk, randomSpawners):
        updated = False
        spawnerTypes = []
        spawnerTypes.extend([
                "Creeper",
                "Skeleton",
                "Zombie",
                "Spider",
                "CaveSpider",
                "Enderman",
                "Ghast",
                "Blaze",
                "Silverfish",
                "PigZombie",
                "LavaSlime",
                "Slime",
                "Pig",
                "Sheep",
                "Cow",
                "Chicken",
                "Squid",
                "Wolf",
                "Villager",
                "Giant",
                "Monster"
        ])
        for entity in chunk['TileEntities']:
                slot = 0
		if entity["id"].value == "MobSpawner":
                        randomchance = random.randrange(0,100)
                        runningpercent = 0
                        spawnerchosen = False
                        count = 0
                        try:
                                for randomSpawner in randomSpawners:
                                        if not spawnerchosen:
                                                runningpercent += int(randomSpawner[0])
                                                if randomchance < runningpercent:
                                                        spawnerchosen = True
                                                else:
                                                        count += 1
                                if spawnerchosen:
                                        entity["EntityId"].value = spawnerTypes[count]
                                        updated = True
                        except IndexError:
                                print("ERROR updating spawner!")
        return updated

def process_world(world_folder, randomSpawners):
        try:
                world = WorldFolder(world_folder)
        except:
                return
        for region in world.iter_regions():
                print(region.filename)
                chunk_moved = False
                for chunk in region.iter_chunks():
                        if(randomize_Spawners(chunk["Level"], randomSpawners)):
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
                                        
                                print("Updating apawners in chunk: x: "+str(x)+" z: "+str(z))
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
        randomfile = open('./RandomSpawners.txt', 'r')
        randomSpawners = []
        for line in randomfile:
                if line.count('#') == 0:
                        randomSpawner = line.split()
                        randomSpawners.append(randomSpawner)
        try:
                if (os.path.exists(world_folder+"/region")):
                        print("Processing the overworld")
                        process_world(world_folder, randomSpawners)
                else:
                        print("Not a valid Minecraft world folder!")
                        return 0
                
                if (os.path.exists(world_folder+"/DIM-1")):
                        print("Processing the nether")
                        process_world(world_folder+"/DIM-1", randomSpawners)

                if (os.path.exists(world_folder+"/DIM1")):
                        print("Processing the end")
                        process_world(world_folder+"/DIM1", randomSpawners)
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
