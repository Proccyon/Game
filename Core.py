import numpy as np
from Images import *
from ImageReader import *
#from Rendering import *
from Behaviour import *
#--------Classes--------#

class Room: #A collection of tiles. For example the inside of a house or the outside world
    def __init__(self,FileName):

        self.Image = GetImage(ImgPrefix+FileName) #A png image
        self.W = self.Image.shape[0] #Width of the room
        self.H = self.Image.shape[1] #Height of the room
        self.TileArray = np.empty((self.W,self.H),dtype=Floor)
        self.ConvertImage()
    
    def ConvertImage(self): #transforms the image into an array with tiles
        
        for x in range(self.W):
            for y in range(self.H):
                for floor in FloorList:
                    if CompareColour(floor.Colour,self.Image[x,y]): #Checks if colours match
                        self.TileArray[x,y] = Tile(x,y,self,floor)
                        break
                        
                    
        
class Floor: #A property of a tile. For example grass, road or a wall
    def __init__(self,Image,Solid,Colour,Name=""):
        self.Image = Image #The sprite of this floor
        self.Colour = Colour / 100 #Used in reading the png file
        self.Name = Name

    
class Tile: #A position in a room. 
    def __init__(self,x,y,Room,Floor,Actor=None,Block=None):
        self.x = x #X coord within a room
        self.y = y #Y coord within a room
        self.Floor = Floor #Properties of the tile itself
        self.Actor = Actor #The actor standing on this tile. Can be None
        self.Room  = Room #The room the tile is in
        self.Inventory = np.empty((10),dtype = Item)
        self.Block = Block     
        
class Item:
    def __init__(self,Image,Location=None,Name=""):
        self.Image = Image #Sprite of the item
        self.Location = Location #The location of the item, on a tile, in a player inventory etc.
        self.Name = Name
        self.ItemId = None #The index of its location in the inventory list

class Block:
    def __init__(self,BlockTemp,Tile = None):
        self.Image = BlockTemp.Image
        self.SolidN = BlockTemp.SolidN
        self.SolidW = BlockTemp.SolidW
        self.SolidE = BlockTemp.SolidE
        self.SolidS = BlockTemp.SolidS
        self.SolidM = BlockTemp.SolidM
        self.SolidDict = { #Dictionary that couples 
            (1,0): self.SolidE,
            (-1,0): self.SolidW,
            (0,1): self.SolidN,
            (0,-1): self.SolidS,
            (0,0): self.SolidM
            }
            
        
        self.Tile = Tile
        if(Tile != None):
            MoveBlock(Tile,Block) #Places the block at the tile
        else:
            self.x = None
            self.y = None
            self.Room = None

class BlockTemplate:
    def __init__(self,Image,SolidN=True,SolidW=True,SolidE=True,SolidS=True,SolidM=True):
        self.Image = Image
        self.SolidN = SolidN #If actors can move through the north of this block
        self.SolidW = SolidW #If actors can move through the west of this block
        self.SolidE = SolidE #If actors can move through the east of this block
        self.SolidS = SolidS #If actors can move through the south of this block
        self.SolidM = SolidM #If actors can exist on this tile at all
        #ex. a block can be solid in all directions except M so this block can work as a cage

class Request: #
    def __init__(self):
        pass
    
class WalkRequest(Request):
    def __init__(self,x,y,Actor):
        Request.__init__()
        self.Energy = 50 #Engergy cost to perform this action
        self.Actor = Actor
        self.x = x
        self.y = y
        
    def DoWalk(self):
        pass
        


#-----Actor and Subclasses-----#              
class Actor: #A living character. A Player, monster, animal etc
    def __init__(self,Tile=None,IntSize = 10):

        self.Inventory = np.empty((IntSize),dtype = Item) #List of items the player carries
        self.IntSize = IntSize #Maximum inventory space
        self.FreeSpace = IntSize #Amount of free inventory space
        ActorList.append(self) #Ads itself to a global list of all actors
        
        self.Tile = Tile #Tile the actor resides on
        if(Tile != None):
            MoveActor(Tile,self) #If a tile is given, Move actor to said tile
            #This also changes atributes in the tile object
        else:
            self.Room = None #Done just to initialize these attributes
            self.x = None
            self.y = None
        
    def Drop(self,ItemId): #Drops an item on the tile the actor is standing on
        if(self.Tile != None):
            if(MoveItem(self.Inventory[ItemId],self.Tile)): #If succesfull, add 1 to FreeSpace
                self.FreeSpace += 1
             
    def Move(self,x,y): #Moves the actor to a different tile with coord x,y in the same room
        MoveActorXY(x,y,self,self.Room)
        
    def PickUp(self,ItemId): #Picks up an item with certain ItemId
        item = self.Tile.Inventory[ItemId]
        if(MoveItem(item,self)):
            self.FreeSpace -= 1 #If Succesfull, Remove 1 from FreeSpace
        
    def CountInventory(self): #Counts the amount of free inventory slots
        Counter = 0
        for item in self.Inventory:
            if(item == None):
                Counter += 1
        self.FreeSpace = Counter
        
        
class Humanoid(Actor): #A Human-like creature
    def __init__(self,Tile=None,IntSize = 10):
        Actor.__init__(self,Tile,IntSize)
        

class Human(Humanoid): #
    def __init__(self,Image,Tile=None,Name = "",Health = 10,Behaviour = None,IntSize = 10):
        Humanoid.__init__(self,Tile,IntSize)
        self.Image = Image #Sprite of the actor
        self.Name = Name
        self.Health = Health
        self.Behaviour =  Behaviour #A Function describing the behaviour of the actor
    
    def DoTurn(self): #The action the actor does during his turn
        self.Behaviour(self)
#-----Actor and Subclasses-----#     
        


#--------Classes--------#     

#--------Functions--------#
def FindTile(x,y,Room): #Finds the tile with (x,y) coords in a room
    try:
       return Room.TileArray[x,y]
       
    except IndexError: #Return False when x,y out of bounds
        return False

def OneRound():
    for actor in ActorList:
        actor.DoTurn()

def MoveItem(Item,Destination): #Moves an item to a new location
    for i in range(len(Destination.Inventory)):
        if(Destination.Inventory[i] == None): #Looks for an empty inventory slot
            Destination.Inventory[i] = Item #Places the item in the inventory of the destination
            Item.Location.Inventory[Item.ItemId] = None #Empties the old location of the item
            Item.Location = Destination #Sets the item location to the new location
            Item.ItemId = i #Sets the ItemId to the new Id
            return True
    return False
    

def MoveActor(NewTile,Actor):#Moves actor to a specific tile    

    if(NewTile.Actor == None): #If the tile is empty of actors
        if(Actor.Tile != None):
            Actor.Tile.Actor = None #Empties the old tile
        NewTile.Actor = Actor #Places the actor at it's new location
        Actor.x = NewTile.x #Puts the information of the tile in the actor
        Actor.y = NewTile.y
        Actor.Room = NewTile.Room
        Actor.Tile = NewTile
        return True
    else:
        return False
            
def MoveActorXY(x,y,Actor,Room): #Moves an actor to a new location
    NewTile = FindTile(x,y,Room)
    return MoveActor(NewTile,Actor)
    

def MoveBlock(NewTile,Block): #Moves a block to a different tile
    
    #Checks if there isn't already a block or actor at NewTile
    if(NewTile.Block == None and (NewTile.Actor == None or Block.SolidM == False)):
        
        if(Block.Tile != None):
            Block.Tile.Block = None
        NewTile.Block = Block
        Block.x = NewTile.x
        Block.y = NewTile.y
        Block.Room = NewTile.Room
        Block.Tile = NewTile
        return True #Returns True if successful
    else:
        return False #Returns False if unsuccessful
   
def MoveBlockXY(x,y,Block,Room):
     NewTile = FindTile(x,y,Room)
     return MoveBlock(NewTile,Block)
     
def CanWalk(Actor,x,y):#Checks if actor can walk to certain tile
        
    dx = x - Actor.x
    dy = y - Actor.y
    if(not((dx,dy) in [(1,0),(-1,0),(0,1),(0,-1)])):
        return False #Checks if new Tile is 1 away from old tile
        
    Tile = FindTile(x,y,Actor.Room)
    if(not(Tile)): #If x,y is outside of room, return False
        return False
        
    if(Tile.Actor != None):
        return False #If there is already an actor on x,y, return False
            
    if(Tile.Block == None):
        return True #If there is no block on x,y, return True
            
        
    if(Tile.Block.SolidDict[(-dx,-dy)] or Tile.Block.SolidDict[(0,0)]):
        return False #Checks if the block at x,y is solid in given direction
    
    return True
        
    

#--------Functions--------#

#--------GlobalVariables--------#
ActorList = []


GrassFloor = Floor(Grass_Img,False,np.asarray([9.4,37.3,18.0]),"Grass")
RoadFloor = Floor(Road_Img,False,np.asarray([71.8,68.6,21.6]),"Road")
WoodFloor = Floor(Wood_Img,True,np.asarray([40.4,40.4,40.4]),"Wood")

FloorList = [GrassFloor,RoadFloor,WoodFloor]



#--------GlobalVariables--------#

#--------End--------#
NewRoom = Room("Map1.png")
Player = Human(Human1_Img,NewRoom.TileArray[1,2],"Kees",Behaviour = WalkCircle)


#--------End--------#
