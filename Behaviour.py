import numpy as np

class A:
    def __init__(self):
        self.ID = 4
        
obj = A()
obj.Hello = 43
print(hasattr(obj,"Hello"))


def WalkCircle(self):
    Xmove = 0
    Ymove = 0
    
    if(not(hasattr(self,"CircleCounter"))): #If object self doesn't have attribute CircleCounter already
        self.CircleCounter = 0
    
    if(self.CircleCounter == 0):
        Xmove = 1
    if(self.CircleCounter == 1):
        Ymove = 1
    if(self.CircleCounter == 2):
        Xmove = -1
    if(self.CircleCounter == 3):
        Ymove = -1
        
    self.CircleCounter += 1
    if(self.CircleCounter >= 4):
        self.CircleCounter = 0
    
    self.Move(self.x + Xmove,self.y + Ymove)
    
    