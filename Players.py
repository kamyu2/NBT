#!/usr/bin/env python
"""
Create Player.dat files with random locations.
"""
import os, sys
import Tkinter, tkFileDialog
import random, math

# local module
try:
	import nbt
except ImportError:
	# nbt not in search path. Let's see if it can be found in the parent folder
	extrasearchpath = os.path.realpath(os.path.join(sys.path[0],os.pardir))
	if not os.path.exists(os.path.join(extrasearchpath,'nbt')):
		raise
	sys.path.append(extrasearchpath)
#from nbt.world import WorldFolder
from nbt.nbt import TAG_Compound, TAG_Byte, TAG_Short, TAG_List, TAG_Int, TAG_Float, TAG_Double, NBTFile, TAG_Int_Array
from nbt.region import RegionFile

class Player:
        def __init__(self, playerName, xpos, ypos, zpos):
                self.filename = "%s.dat" % (playerName)
                self.player = NBTFile()
                motion = TAG_List(name = "Motion", type = TAG_Double)
                motion.insert(0, TAG_Double(value = 0))
                motion.insert(1, TAG_Double(value = 0))
                motion.insert(2, TAG_Double(value = 0))
                pos = TAG_List(name = "Pos", type = TAG_Double)
                pos.insert(0, TAG_Double(value = xpos))
                pos.insert(1, TAG_Double(value = ypos))
                pos.insert(2, TAG_Double(value = zpos))
                rotation = TAG_List(name = "Rotation", type = TAG_Float)
                rotation.insert(0, TAG_Float(value = 0))
                rotation.insert(1, TAG_Float(value = 0))
                abilities = TAG_Compound()
                abilities.name = "abilities"
                abilities.tags.extend([
                        TAG_Byte(name = "flying", value = 0),
                        TAG_Byte(name = "instabuild", value = 0),
                        TAG_Byte(name = "invulnerable", value = 0),
                        TAG_Byte(name = "mayfly", value = 0)
                ])
                self.player.tags.extend([
                        TAG_Byte(name = "OnGround", value = 1),
                        TAG_Byte(name = "Sleeping", value = 0),
                        TAG_Short(name = "Air", value = 300),
                        TAG_Short(name = "AttackTime", value = 0),
                        TAG_Short(name = "DeathTime", value = 0),
                        TAG_Short(name = "Fire", value = -20),
                        TAG_Short(name = "Health", value = 20),
                        TAG_Short(name = "HurtTime", value = 0),
                        TAG_Short(name = "SleepTimer", value = 0),
                        TAG_Int(name = "Dimension", value = 0),
                        TAG_Int(name = "foodLevel", value = 20),
                        TAG_Int(name = "foodTickTimer", value = 0),
                        TAG_Int(name = "playerGameType", value = 0),
                        TAG_Int(name = "SpawnX", value = xpos),
                        TAG_Int(name = "SpawnY", value = ypos),
                        TAG_Int(name = "SpawnZ", value = zpos),
                        TAG_Int(name = "XpLevel", value = 0),
                        TAG_Int(name = "XpTotal", value = 0),
                        TAG_Float(name = "fallDistance", value = 0),
                        TAG_Float(name = "foodExhaustionLevel", value = 0),
                        TAG_Float(name = "foodSaturationLevel", value = 5),
                        TAG_Float(name = "XpP", value = 0),
                        TAG_List(name = "Inventory", type = TAG_Compound),
                        motion,
                        pos,
                        rotation,
                        abilities
                ])

class MakePlayers:
        def __init__(self,frame):
                self.root = frame
                self.root.title('Create Player Files')
                self.region_folder = ''
                self.lowerX = Tkinter.IntVar(value=0)
                self.lowerZ = Tkinter.IntVar(value=0)
                self.higherX = Tkinter.IntVar(value=0)
                self.higherZ = Tkinter.IntVar(value=0)
                self.sealevel = Tkinter.IntVar(value=64)
                self.playerName = Tkinter.StringVar()
                XFrame = Tkinter.Frame(self.root)
                ZFrame = Tkinter.Frame(self.root)
                playerFrame = Tkinter.Frame(self.root)
                buttonandlistFrame = Tkinter.Frame(self.root)
                buttonFrame = Tkinter.Frame(buttonandlistFrame)
                sealevelFrame = Tkinter.Frame(self.root)
                self.lowerXEntry = Tkinter.Entry(XFrame, textvariable=self.lowerX, width=10)
                self.lowerZEntry = Tkinter.Entry(ZFrame, textvariable=self.lowerZ, width=10)
                self.higherXEntry = Tkinter.Entry(XFrame, textvariable=self.higherX, width=10)
                self.higherZEntry = Tkinter.Entry(ZFrame, textvariable=self.higherZ, width=10)
                self.sealevelEntry = Tkinter.Entry(sealevelFrame, textvariable=self.sealevel, width=5)
                self.playerNameEntry = Tkinter.Entry(playerFrame, textvariable=self.playerName, width=30)
                playerNameLabel = Tkinter.Label(playerFrame, text="Player name:")
                self.addPlayerButton = Tkinter.Button(buttonFrame, command=self.addPlayer, text="Add player to list", width=30, height=3)
                self.removePlayerButton = Tkinter.Button(buttonFrame, command=self.removePlayer, text="Remove player from list", width=30, height=3)
                self.createPlayerButton = Tkinter.Button(buttonFrame, command=self.createPlayers, text="Create player.dat files", width=30, height=3)
                self.selectWorldButton = Tkinter.Button(self.root, command=self.selectWorld, text="Select World", width=30, height=3)
                lowerXLabel = Tkinter.Label(XFrame, text="Lower X coordinate:")
                lowerZLabel = Tkinter.Label(ZFrame, text="Lower Z coordinate:")
                higherXLabel = Tkinter.Label(XFrame, text="Higher X coordinate:")
                higherZLabel = Tkinter.Label(ZFrame, text="Higher Z coordinate:")
                sealevelLabel = Tkinter.Label(sealevelFrame, text="Sea level (normal = 64):")
                self.playerList = Tkinter.Listbox(buttonandlistFrame, width=30)
                self.playerNameEntry.bind("<Return>", self.addPlayer)
                lowerXLabel.pack(side='left')
                self.lowerXEntry.pack(side='left', padx=5)
                lowerZLabel.pack(side='left')
                self.lowerZEntry.pack(side='left', padx=5)
                higherXLabel.pack(side='left')
                self.higherXEntry.pack(side='left')
                higherZLabel.pack(side='left')
                self.higherZEntry.pack(side='left')
                playerNameLabel.pack(side='left')
                sealevelLabel.pack(side='left')
                self.sealevelEntry.pack(side='left')
                self.playerNameEntry.pack(side='left')
                self.addPlayerButton.pack(pady=5)
                self.removePlayerButton.pack(pady=5)
                self.createPlayerButton.pack(pady=5)
                XFrame.pack(pady=5)
                ZFrame.pack(pady=5)
                sealevelFrame.pack(pady=10)
                self.selectWorldButton.pack(pady=5)
                playerFrame.pack(pady=5)
                buttonFrame.pack(side='left')
                self.playerList.pack(side='left', fill='y', expand=1)
                buttonandlistFrame.pack(fill='y', expand=1)
                self.heights = []
                count = 0
                for x in range(16):
                        height = []
                        for y in range(16):
                                height.insert(y,count)
                                count += 1
                        self.heights.insert(x,height)

        def validateData(self):
                try:
                        lowX = int(self.lowerX.get())
                except ValueError:
                        print("ERROR: Lower X coordinate is invalid!!")
                        return False
                try:
                        lowZ = int(self.lowerZ.get())
                except ValueError:
                        print("ERROR: Lower Z coordinate is invalid!!")
                        return False
                try:
                        highX = int(self.higherX.get())
                except ValueError:
                        print("ERROR: Higher X coordinate is invalid!!")
                        return False
                try:
                        highZ = int(self.higherZ.get())
                except ValueError:
                        print("ERROR: Higher Z coordinate is invalid!!")
                        return False
                try:
                        sealevel = int(self.sealevel.get())
                except ValueError:
                        print("ERROR: Sea level value is invalid!!")
                        return False
                if lowX >= highX:
                        print("ERROR: Lower X is greater than or equal to Higher X!!")
                        return False
                elif lowZ >= highZ:
                        print("ERROR: Lower Z is greater than or equal to Higher Z!!")
                        return False
                elif sealevel < 0 or sealevel > 256:
                        print("ERROR: Sea level is out of bounds!! (min=0, max=256)")
                        return False
                return True

        def addPlayer(self, event=None):
                alreadyexists = False
                if len(self.playerName.get()) == 0:
                        print("No player name entered!!")
                else:
                        if self.playerList.size() == 1:
                                if self.playerList.get(0) == self.playerName.get():
                                        alreadyexists = True
                        elif self.playerList.size() > 1:
                                players = self.playerList.get(0,self.playerList.size()-1)
                                for player in players:
                                        if player == self.playerName.get():
                                                alreadyexists = True
                        if alreadyexists:
                                print("%s is already in the list!!" % (self.playerName.get()))
                        else:
                                print("Adding player: %s" % (self.playerName.get()))
                                self.playerList.insert(self.playerList.size(), self.playerName.get())
                self.playerName.set("")
                                        

        def removePlayer(self):
                selection = self.playerList.curselection()
                if len(selection) > 0:
                        print("Removing player: %s" % (self.playerList.get(selection)))
                        self.playerList.delete(selection)

        def createPlayers(self):
                if self.validateData():
                        if self.playerList.size() == 1:
                                player = self.createPlayer(self.playerList.get(0))
                                print("Creating %s.dat" % (self.playerList.get(0)))
                                player.player.write_file(player.filename)
                        elif self.playerList.size() > 1:
                                playernames = self.playerList.get(0,self.playerList.size()-1)
                                for name in playernames:
                                        player = self.createPlayer(name)
                                        print("Creating %s.dat" % (name))
                                        player.player.write_file(player.filename)
                        else:
                                print("No players in list!!")
                        self.playerList.delete(0,self.playerList.size()-1)

        def createPlayer(self, name):
                randX = random.randrange(self.lowerX.get(), self.higherX.get())
                randZ = random.randrange(self.lowerZ.get(), self.higherZ.get())
                regionX = math.floor(float(randX)/(32*16))
                regionZ = math.floor(float(randZ)/(32*16))
                chunkX = randX >> 4
                chunkZ = randZ >> 4
                blockX = randX & 0xf
                blockZ = randZ & 0xf
                regionName = "r.%i.%i.mca" % (regionX, regionZ)
                if chunkX < 0:
                        while chunkX < 0:
                                chunkX += 32
                if chunkX > 31:
                        while chunkX > 31:
                                chunkX -= 32
                if chunkZ < 0:
                        while chunkZ < 0:
                                chunkZ += 32
                if chunkZ > 31:
                        while chunkZ > 31:
                                chunkZ -= 32
                if os.path.exists(self.region_folder + regionName):
                        #check heightmap
                        tempRegion = RegionFile(self.region_folder + regionName)
                        tempChunk = tempRegion.get_chunk(chunkX, chunkZ)
                        if tempChunk != None:
                                #chunk exists so use heightmap
                                player = Player(name,randX,tempChunk["Level"]["HeightMap"][self.heights[blockZ][blockX]] + 1,randZ)
                        else:
                                #chunk doesn't exist so use sea level
                                player = Player(name,randX,self.sealevel.get(),randZ)
                else:
                        #use sea level
                        player = Player(name,randX,self.sealevel.get(),randZ)
                return player

        def selectWorld(self):
                world_folder = tkFileDialog.askdirectory(parent=self.root,title='Please select a world folder')
                if (os.path.exists(world_folder+"/region")):
                        self.region_folder = world_folder + "/region/"
                        print("Region folder: %s" % self.region_folder)
                else:
                        print("ERROR: Not a valid world folder!!")
                        self.region_folder = ''
	
if __name__ == '__main__':
        root = Tkinter.Tk()
        mywindow = MakePlayers(root)
	root.mainloop()


