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

class SpawnersWindow:
        def __init__(self,frame):
                self.root = frame
                self.root.title('Randomize Spawners')
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
                self.selectRandomFileButton = Tkinter.Button(self.root, command=self.selectRandomFile, text="Select Random File", width=30, height=3)
                self.randomizeButton = Tkinter.Button(self.root, command=self.main, text="Randomize Spawners", width=30, height=3)
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
                self.random_file = tkFileDialog.askopenfilename(parent=self.root,title='Please select a randomizer file')

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
                #print("xmin: " + str(self.lowerX.get()) + " xmax: " + str(self.higherX.get()))
                #print("zmin: " + str(self.lowerZ.get()) + " zmax: " + str(self.higherZ.get()))
                #print("overworld: " + str(self.doOverworld.get()) + " nether: " + str(self.doNether.get()) + " end: " + str(self.doEnd.get()))
                randomfile = open(self.random_file, 'r')
                randomSpawners = []
                for line in randomfile:
                        if line.count('#') == 0:
                                randomSpawner = line.split()
                                randomSpawners.append(randomSpawner)
                try:
                        if self.doOverworld.get():
                                if (os.path.exists(self.world_folder+"/region")):
                                        print("Processing the overworld")
                                        self.process_world(self.world_folder, randomSpawners)
                                else:
                                        print("Overworld files not found!")

                        if self.doNether.get():
                                if (os.path.exists(self.world_folder+"/DIM-1")):
                                        print("Processing the nether")
                                        self.process_world(self.world_folder+"/DIM-1", randomSpawners)
                                else:
                                        print("Nether folder not found!")

                        if self.doEnd.get():
                                if (os.path.exists(self.world_folder+"/DIM1")):
                                        print("Processing the end")
                                        self.process_world(self.world_folder+"/DIM1", randomSpawners)
                                else:
                                        print("End folder not found!")
                except KeyboardInterrupt:
                        return 75 # EX_TEMPFAIL
                print("DONE!")

        def process_world(self, world_folder, randomSpawners):
                try:
                        world = WorldFolder(world_folder)
                except:
                        return
                for region in world.iter_regions():
                        print(region.filename)
                        chunk_moved = False
                        for chunk in region.iter_chunks():
                                if(self.randomize_Spawners(chunk["Level"], randomSpawners)):
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

        def randomize_Spawners(self, chunk, randomSpawners):
                updated = False
                for entity in chunk['TileEntities']:
                        if entity["id"].value == "MobSpawner":
                                if (self.lowerX.get() <= entity["x"].value <= self.higherX.get() and self.lowerZ.get() <= entity["z"].value <= self.higherZ.get() and self.lowerY.get() <= entity["y"].value <= self.higherY.get()) or (self.lowerX.get() == self.higherX.get() == self.lowerZ.get() == self.higherZ.get() == self.lowerY.get() == self.higherY.get() == 0):
                                        randomchance = random.uniform(0,100)
                                        runningpercent = 0.0
                                        spawnerchosen = False
                                        try:
                                                for randomSpawner in randomSpawners:
                                                        if not spawnerchosen:
                                                                runningpercent += float(randomSpawner[0])
                                                                #print("chance: " + str(randomchance) + " random: " + str(runningpercent))
                                                                if randomchance < runningpercent:
                                                                        spawnerchosen = True
                                                                        entity["EntityId"].value = randomSpawner[1]
                                                                        updated = True
                                        except IndexError:
                                                print("ERROR updating spawner!")
                return updated

if __name__ == '__main__':
        root = Tkinter.Tk()
        mywindow = SpawnersWindow(root)
        root.mainloop()
