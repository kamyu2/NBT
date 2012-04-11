#!/usr/bin/env python
"""
Finds signs and loads them in a gui to edit
"""
import os, sys
import Tix, tkFileDialog

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
#from nbt.nbt import TAG_Compound, TAG_Byte, TAG_Short, TAG_List

def validateTextInputSize(event):
                if (event.widget.index('end') >= 15):
                        event.widget.delete(15)
                        
class signframe:
        def __init__(self, root, sign, count):
                self.line1 = Tix.StringVar()
                self.line1.set(sign["Text1"].value)
                self.line2 = Tix.StringVar()
                self.line2.set(sign["Text2"].value)
                self.line3 = Tix.StringVar()
                self.line3.set(sign["Text3"].value)
                self.line4 = Tix.StringVar()
                self.line4.set(sign["Text4"].value)
                mainf = Tix.Frame(root)
                frame = Tix.Frame(mainf)
                l1=Tix.Entry(frame, textvariable=self.line1, width=16)
                l1.bind("<Key>", validateTextInputSize)
                l1.pack()
                l2=Tix.Entry(frame, textvariable=self.line2, width=16)
                l2.bind("<Key>", validateTextInputSize)
                l2.pack()
                l3=Tix.Entry(frame, textvariable=self.line3, width=16)
                l3.bind("<Key>", validateTextInputSize)
                l3.pack()
                l4=Tix.Entry(frame, textvariable=self.line4, width=16)
                l4.bind("<Key>", validateTextInputSize)
                l4.pack()
                label1=Tix.Label(mainf, text=str(count+1), width=15)
                xpos=Tix.Label(mainf, text=str(sign["x"].value), width=7)
                ypos=Tix.Label(mainf, text=str(sign["y"].value), width=7)
                zpos=Tix.Label(mainf, text=str(sign["z"]), width=7)
                label1.pack(side='left')
                xpos.pack(side='left')
                ypos.pack(side='left')
                zpos.pack(side='left')
                frame.pack(side='left')
                mainf.pack(pady=10,padx=10)
                root.update_idletasks()
                
        
                
class SignApp:
        def __init__(self,frame):
                self.world = " "
                self.nether = " "
                self.end = " "
                self.signsnbt = []
                self.signswin = []
                self.signscount = 0
                self.root=frame
                self.root.title('Edit Signs')
                self.root.resizable(0,0)
                self.root.wm_geometry('400x700+300+10')

                load = Tix.Button(self.root, text='OPEN WORLD', command=self.load_dir, width=30,height=5)
                load.pack(side='top')
                self.headings = Tix.Frame(self.root)
                Tix.Label(self.headings,text="Sign Number",width=15).pack(side='left')
                poshead = Tix.Frame(self.headings)
                Tix.Label(poshead,text="Sign Position",width=21).pack(side='top')
                Tix.Label(poshead,text="X",width=7).pack(side='left')
                Tix.Label(poshead,text="Y",width=7).pack(side='left')
                Tix.Label(poshead,text="Z",width=7).pack(side='left')
                poshead.pack(side='left')
                Tix.Label(self.headings,text="Sign Text",width=15).pack(side='left')
                self.headings.pack()
                
                save = Tix.Button(self.root, text='SAVE SIGNS', command=self.save_signs, width=30,height=5)
                save.pack(side='bottom')
                        
                self.swin = Tix.ScrolledWindow(self.root,scrollbar=Tix.Y)
                self.swin.pack()
                self.win = self.swin.window
                

                
        def load_dir(self):
                try:
                        saveFileDir = os.path.join(os.path.join(os.environ['APPDATA'].decode(sys.getfilesystemencoding()), u".minecraft"), u"saves")
                except:
                        saveFileDir = '.'
                world_folder = tkFileDialog.askdirectory(parent=self.root,initialdir=saveFileDir,title='Please select a directory')
                if (not os.path.exists(world_folder)):
        		print("No such folder as "+world_folder)
                	return
                self.world = " "
                self.nether = " "
                self.end = " "
                self.signsnbt = []
                self.signswin = []
                self.signscount = 0
                self.swin.destroy()
                self.swin = Tix.ScrolledWindow(self.root,scrollbar=Tix.Y)
                self.swin.pack()
                self.win = self.swin.window	
                self.main(world_folder,self.win)

        def save_world(self,world1,count):
                updates = 0
                if count >= self.signscount:
                        return count
                for region in world1.iter_regions():
                        print(region.filename)
                        for chunk in region.iter_chunks():
                                chunkupdated = False
                                updates = 0
                                for entity in chunk["Level"]["TileEntities"]:
                                        if entity["id"].value == "Sign" and count < len(self.signsnbt):
                                                if entity["x"].value == self.signsnbt[count]["x"].value and entity["y"].value == self.signsnbt[count]["y"].value and entity["z"].value == self.signsnbt[count]["z"].value:
                                                        entity["Text1"].value = self.signswin[count].line1.get()
                                                        entity["Text2"].value = self.signswin[count].line2.get()
                                                        entity["Text3"].value = self.signswin[count].line3.get()
                                                        entity["Text4"].value = self.signswin[count].line4.get()
                                                        count += 1
                                                        updates += 1
                                                        chunkupdated = True
                                if(chunkupdated):
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
                                                
                                        print("Updating "+ str(updates) + " signs in chunk: x: "+str(x)+" z: "+str(z))
                                        try:
                                                if(region.write_chunk(x,z,chunk)):
                                                        chunk_moved = True
                                        except ValueError as e:
                                                print("ERROR:  Failed to update chunk.")
                                                print(e)
                                if count >= self.signscount:
                                                return count
                return count
                
        def save_signs(self):
                count = 0
                if self.world != " ":
                        print("---SAVING OVERWORLD---")
                        count = self.save_world(self.world, count)
                        print("---DONE---")
                if self.nether != " ":
                        print("---SAVING NETHER---")
                        count = self.save_world(self.nether, count)
                        print("---DONE---")
                if self.end != " ":
                        print("---SAVING END---")
                        count = self.save_world(self.end, count)
                        print("---DONE---")
                        
                                                                
       
        def process_world(self,world1,win):
                print("---LOADING SIGNS---")
                if self.signscount >= 372:
                        print("---temp sign limit reached!---")
                        return
                for region in world1.iter_regions():
                        print(region.filename)
                        for chunk in region.iter_chunks():
                                for entity in chunk["Level"]["TileEntities"]:
                                        if entity["id"].value == "Sign":
                                                if self.signscount < 372:
                                                        print("Sign at x: "+str(entity["x"].value)+" y: "+str(entity["y"].value)+" z: "+str(entity["z"].value))
                                                        self.signsnbt.insert(self.signscount,entity)
                                                        self.signswin.insert(self.signscount,signframe(win,self.signsnbt[self.signscount],self.signscount))
                                                        self.signscount += 1
                                                else:
                                                        print("---temp sign limit reached!---")
                                                        return
                print("---DONE---")


        def main(self,world_folder,win):
                try:
                        if (os.path.exists(world_folder+"/region")):
                                print("Processing the overworld")
                                try:
                                        self.world = WorldFolder(world_folder)
                                except:
                                        print("---overworld has no regions---")
                                        return
                                self.process_world(self.world,win)
                        else:
                                print("Not a valid Minecraft world folder!")
                                return 0
                        
                        if (os.path.exists(world_folder+"/DIM-1")):
                                print("Processing the nether")
                                try:
                                        self.nether = WorldFolder(world_folder+"/DIM-1")
                                except:
                                        print("---nether has no regions---")
                                        return
                                self.process_world(self.nether,win)

                        if (os.path.exists(world_folder+"/DIM1")):
                                print("Processing the end")
                                try:
                                        self.end = WorldFolder(world_folder+"/DIM1")
                                except:
                                        print("---end has no regions---")
                                        return
                                self.process_world(self.end,win)
                except KeyboardInterrupt:
                        return 75 # EX_TEMPFAIL
                
                return 0 # NOERR


	
if __name__ == '__main__':

        root = Tix.Tk()
        mywindow = SignApp(root)
	root.mainloop()


