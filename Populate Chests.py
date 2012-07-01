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

class PopulateChestsWindow:
        def __init__(self,frame):
                self.root = frame
                self.root.title('Populate Chests')
                self.region_folder = ''
                self.lowerX = Tkinter.IntVar(value=0)
                self.lowerZ = Tkinter.IntVar(value=0)
                self.lowerY = Tkinter.IntVar(value=0)
                self.higherX = Tkinter.IntVar(value=0)
                self.higherZ = Tkinter.IntVar(value=0)
                self.higherY = Tkinter.IntVar(value=0)
                self.doOverworld = Tkinter.BooleanVar(value=True)
                self.doNether = Tkinter.BooleanVar(value=True)
                self.doEnd = Tkinter.BooleanVar(value=True)
                XFrame = Tkinter.Frame(self.root)
                ZFrame = Tkinter.Frame(self.root)
                YFrame = Tkinter.Frame(self.root)
                self.lowerXEntry = Tkinter.Entry(XFrame, textvariable=self.lowerX, width=10)
                self.lowerZEntry = Tkinter.Entry(ZFrame, textvariable=self.lowerZ, width=10)
                self.lowerYEntry = Tkinter.Entry(YFrame, textvariable=self.lowerY, width=10)
                self.higherXEntry = Tkinter.Entry(XFrame, textvariable=self.higherX, width=10)
                self.higherZEntry = Tkinter.Entry(ZFrame, textvariable=self.higherZ, width=10)
                self.higherYEntry = Tkinter.Entry(YFrame, textvariable=self.higherY, width=10)
                self.selectWorldButton = Tkinter.Button(self.root, command=self.selectWorld, text="Select World", width=30, height=3)
                self.selectRandomFileButton = Tkinter.Button(self.root, command=self.selectRandomFile, text="Select Random Items File", width=30, height=3)
                self.randomizeButton = Tkinter.Button(self.root, command=self.main, text="Populate Chests", width=30, height=3)
                lowerXLabel = Tkinter.Label(XFrame, text="Lower X coordinate:")
                lowerZLabel = Tkinter.Label(ZFrame, text="Lower Z coordinate:")
                lowerYLabel = Tkinter.Label(YFrame, text="Lower Y coordinate:")
                higherXLabel = Tkinter.Label(XFrame, text="Higher X coordinate:")
                higherZLabel = Tkinter.Label(ZFrame, text="Higher Z coordinate:")
                higherYLabel = Tkinter.Label(YFrame, text="Higher Y coordinate:")
                lowerXLabel.pack(side='left')
                self.lowerXEntry.pack(side='left', padx=5)
                lowerZLabel.pack(side='left')
                self.lowerZEntry.pack(side='left', padx=5)
                higherXLabel.pack(side='left')
                self.higherXEntry.pack(side='left')
                higherZLabel.pack(side='left')
                self.higherZEntry.pack(side='left')
                lowerYLabel.pack(side='left')
                self.lowerYEntry.pack(side='left', padx=5)
                higherYLabel.pack(side='left')
                self.higherYEntry.pack(side='left')
                self.overworldCheckBox = Tkinter.Checkbutton(self.root, text="Process Overworld", variable=self.doOverworld, onvalue=True, offvalue=False, height=1, width=15)
                self.netherCheckBox = Tkinter.Checkbutton(self.root, text="Process Nether", variable=self.doNether, onvalue=True, offvalue=False, height=1, width=15)
                self.endCheckBox = Tkinter.Checkbutton(self.root, text="Process End", variable=self.doEnd, onvalue=True, offvalue=False, height=1, width=15)
                self.doAllButton = Tkinter.Button(self.root, command=self.doAll, text="Reset to entire map", width=30, height=3)
                self.selectWorldButton.pack(pady=5)
                self.selectRandomFileButton.pack(pady=5)
                XFrame.pack(pady=5)
                ZFrame.pack(pady=5)
                YFrame.pack(pady=5)
                self.overworldCheckBox.pack()
                self.netherCheckBox.pack()
                self.endCheckBox.pack()
                self.doAllButton.pack(pady=5)
                self.randomizeButton.pack(pady=5)
                self.world_folder = ' '
                self.random_file = ' '

        def selectWorld(self):
                try:
                        saveFileDir = os.path.join(os.path.join(os.environ['APPDATA'].decode(sys.getfilesystemencoding()), u".minecraft"), u"saves")
                except:
                        saveFileDir = '.'
		self.world_folder = tkFileDialog.askdirectory(parent=self.root,initialdir=saveFileDir,title='Please select a world folder')
        
                if (not os.path.exists(self.world_folder)):
                        print("No such folder as "+self.world_folder)
                        self.world_folder = ' '

        def selectRandomFile(self):
                self.random_file = tkFileDialog.askopenfilename(parent=self.root,title='Please select a random items file')

        def doAll(self):
                self.lowerX.set(0)
                self.higherX.set(0)
                self.lowerZ.set(0)
                self.higherZ.set(0)
                self.lowerY.set(0)
                self.higherY.set(0)
                self.doOverworld.set(True)
                self.doNether.set(True)
                self.doEnd.set(True)

        def main(self):
                randomfile = open(self.random_file, 'r')
                randomitems = []
                for line in randomfile:
                        if line.count('#') == 0 and len(line) > 4:
                                randomitem = line.split()
                                randomitems.append(randomitem)
                try:
                        if self.doOverworld.get():
                                if (os.path.exists(self.world_folder+"/region")):
                                        print("Processing the overworld")
                                        self.process_world(self.world_folder, randomitems)
                                else:
                                        print("Overworld files not found!")

                        if self.doNether.get():
                                if (os.path.exists(self.world_folder+"/DIM-1")):
                                        print("Processing the nether")
                                        self.process_world(self.world_folder+"/DIM-1", randomitems)
                                else:
                                        print("Nether folder not found!")

                        if self.doEnd.get():
                                if (os.path.exists(self.world_folder+"/DIM1")):
                                        print("Processing the end")
                                        self.process_world(self.world_folder+"/DIM1", randomitems)
                                else:
                                        print("End folder not found!")
                except KeyboardInterrupt:
                        return 75 # EX_TEMPFAIL
                print("DONE!")

        def process_world(self, world_folder, randomitems):
                try:
                        world = WorldFolder(world_folder)
                except:
                        return
                for region in world.iter_regions():
                        print(region.filename)
                        chunk_moved = False
                        for chunk in region.iter_chunks():
                                if(self.derp_chests(chunk["Level"], randomitems)):
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

        def derp_chests(self, chunk, randomitems):
                updated = False
                for entity in chunk['TileEntities']:
                        if entity["id"].value == "Chest":
                                if (self.lowerX.get() <= entity["x"].value <= self.higherX.get() and self.lowerZ.get() <= entity["z"].value <= self.higherZ.get() and self.lowerY.get() <= entity["y"].value <= self.higherY.get()) or (self.lowerX.get() == self.higherX.get() == self.lowerZ.get() == self.higherZ.get() == self.lowerY.get() == self.higherY.get() == 0):
                                        updated = (self.process_entity(entity, randomitems) or updated)
                for entity in chunk['Entities']:
                        if entity["id"].value == "Minecart":
                                if entity["Type"].value == 1:
                                        position = []
                                        for coord in entity["Pos"]:
                                                position.append(float(coord.value))        
                                        if (self.lowerX.get() <= position[0] <= self.higherX.get() and self.lowerZ.get() <= position[2] <= self.higherZ.get() and self.lowerY.get() <= position[1] <= self.higherY.get()) or (self.lowerX.get() == self.higherX.get() == self.lowerZ.get() == self.higherZ.get() == self.lowerY.get() == self.higherY.get() == 0):
                                                updated = (self.process_entity(entity, randomitems) or updated)
                return updated

        def process_entity(self, entity, randomitems):
                slot = 0
                updated = False
                items = items_from_nbt(entity["Items"])
                if sum(items.values()) == 0:
                        print("empty chest found")
                        itemlist = TAG_List(type=TAG_Compound)
                        for randomitem in randomitems:
                                if slot < 27:
                                        if random.uniform(0,100) < float(randomitem[3]):
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

if __name__ == '__main__':
        root = Tkinter.Tk()
        mywindow = PopulateChestsWindow(root)
        root.mainloop()
