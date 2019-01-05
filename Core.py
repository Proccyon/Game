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
        self.Solid = Solid #If actors can move over this floor
        self.Colour = Colour / 100 #Used in reading the png file
        self.Name = Name
        
class Tile: #A position in a room. 
    def __init__(self,x,y,Room,Floor,Actor=None):
        self.x = x #X coord within a room
        self.y = y #Y coord within a room
        self.Floor = Floor #Properties of the tile itself
        self.Actor = Actor #The actor standing on this tile. Can be None
        self.Room  = Room #The room the tile is in
        self.Inventory = np.empty((10),dtype = Item)     
        
class Item:
    def __init__(self,Image,Location=None,Name=""):
        self.Image = Image #Sprite of the item
        self.Location = Location #The location of the item, on a tile, in a player inventory etc.
        self.Name = Name
        self.ItemId = None #The index of its location in the inventory list
                  
class Actor: #A living character. A Player, monster, animal etc
    def __init__(self,Tile=None,IntSize = 10):
        self.Tile = Tile #Tile the actor resides on
        self.x = Tile.x #x coord of tile in room
        self.y = Tile.y #y coord of tile in room
        self.Room = Tile.Room # The room the actor is in
        self.Tile.Actor  = self #The tile the actor resides on
        self.Inventory = np.empty((IntSize),dtype = Item) #List of items the player carries
        self.IntSize = IntSize
        self.FreeSpace = IntSize
        ActorList.append(self) #Ads itself to a global list of all actors
        
    def Drop(self,ItemId): #Drops an item on the tile the actor is standing on
        if(self.Tile != None):
            if(MoveItem(self.Inventory[ItemId],self.Tile)): #If succesfull, add 1 to FreeSpace
                self.FreeSpace += 1
             
    def Move(self,x,y): #Moves the actor to a different tile with coord x,y in the same room
        MoveActor(x,y,self,self.Room)
        
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
        
        


#--------Classes--------#     

#--------Functions--------#

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
    
def MoveActor(x,y,Actor,Room): #Moves an actor to a new location
    
    try: #Might have to do something more elegant
        NewTile = Room.TileArray[x,y]
        if(NewTile.Actor == None): #If the tile is empty of actors
            Actor.Tile.Actor = None #Empties the old tile
            NewTile.Actor = Actor #Places the actor at it's new location
            Actor.x = x #Puts the information of the tile in the actor
            Actor.y = y
            Actor.Room = Room
            Actor.Tile = NewTile
            return True
        else:
            return False
            
    except IndexError: #If x,y is out of bounds, will probably check this before using this function
        return False #Return True when succesfully moved, otherwise return False
        
    
    
    
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