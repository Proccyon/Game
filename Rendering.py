import pyglet as pgl
from pyglet.window import mouse
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.window import mouse
from pyglet.window import key
import numpy as np
from Images import *
from Core import *


#--------Start--------#
WindowWidth = 20 #Width of the window in units of boxes
WindowHeight = 20 #Height of the window in units of boxes
X0 = 11 #The x coord the camera is pointed at
Y0 = 10 #The y coord the camera is pointed at
L = 30 #Length of 1 box in pixels
FPS = 5 #Frames per second
ScrollSpeed = 10 #How fast you can scroll through the map

window = pgl.window.Window(WindowWidth*L,WindowHeight*L)
Batch = pgl.graphics.Batch()
ImgPrefix = "C:/Users/Eigenaar/Desktop/New game/Images/"

keys = key.KeyStateHandler()
window.push_handlers(keys)

FloorGroup = pgl.graphics.OrderedGroup(0) #Draw order for floors
ActorGroup = pgl.graphics.OrderedGroup(1) #Draw order for Actors


#--------Start--------#



#--------Definitions--------#

def DrawTiles(Room):
    FloorSpriteList = []
    ActorSpriteList = []
    for X in range(Room.W):
        for Y in range(Room.H):
            Tile = Room.TileArray[X,Y]
            Xtotal = L*(0.5*WindowWidth-X0+X)
            Ytotal = L*(0.5*WindowHeight-Y0+Y)
            
            FloorSpriteList.append(pgl.sprite.Sprite(img=Tile.Floor.Image,x=Xtotal,
            y=Ytotal,batch=Batch,group=FloorGroup))
            
            if(Tile.Actor != None):
                ActorSpriteList.append(pgl.sprite.Sprite(img=Tile.Actor.Image,x=Xtotal,
                y=Ytotal,batch=Batch,group=ActorGroup))
            
    return FloorSpriteList, ActorSpriteList
            
    
def BackGround(Image,L,S,Xoffset,Yoffset):
    background = pgl.graphics.OrderedGroup(0)
    SpriteList = []
    for X in range(S):
        for Y in range(S):
            SpriteList.append(pgl.sprite.Sprite(img=Image,x=L*X-Xoffset,y=L*Y-Yoffset,batch=Batch,group=background))
    return SpriteList

def Show(Room):
    
    #SpriteList = DrawTiles(Room)
    def update(dt): #Allows you to scroll through the map
        global X0
        global Y0
        
        if keys[key.LEFT]:
            X0-= ScrollSpeed/FPS
        if keys[key.RIGHT]:
            X0+= ScrollSpeed/FPS
        if keys[key.UP]:
            Y0+= ScrollSpeed/FPS
        if keys[key.DOWN]:
            Y0-= ScrollSpeed/FPS
    
    @window.event
    def on_draw():
        OneRound()
        SpriteList,ActorSpriteList = DrawTiles(Room)
        window.clear()
        Batch.draw()
        

        
    pgl.clock.schedule_interval(update,1/FPS)
    pgl.app.run()

#--------Definitions--------#

#--------End--------#

Show(NewRoom)








#if __name__ == "__main__":
    #BackgroundList = BackGround(Grid_Img,31,2,15,15)
    
    #foreground = pgl.graphics.OrderedGroup(1)
    #wood = pgl.sprite.Sprite(img=Wood_Img,x=1,y=1,batch=Batch,group=foreground)
    #@window.event
    #def on_draw():
        #window.clear()
       # Batch.draw()
        
    #pgl.app.run()
#--------End--------#