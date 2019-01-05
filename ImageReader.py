import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np

def GetImage(Name):
    img = mpimg.imread(Name)
    Image,R,G,B = TransformImage(img)
    return Image

def TransformImage(Image):
    w = len(Image)
    h = len(Image[0])
    
    NewImage = np.empty((h,w),dtype=list)
    R = np.empty((h,w))
    G = np.empty((h,w))
    B = np.empty((h,w))

    
    for x in range(w):
        for y in range(h):
            NewImage[y,x] = Image[w-x-1][y]
            R[y,x] = Image[x][y][0]
            G[y,x] = Image[x][y][1]
            B[y,x] = Image[x][y][2]
        
    return NewImage,R,G,B
    
def CompareColour(C1,C2,Max=0.015):
    return np.sqrt((C1[0]-C2[0])**2+(C1[1]-C2[1])**2+(C1[2]-C2[2])**2) <= Max
#prefix = "C:/Users/Eigenaar/Desktop/New game/Images/"
#Name = "Map1.png"
#FileName = prefix+Name

#img = mpimg.imread(FileName)
#Image,R,G,B = TransformImage(img)
#print(Image[0,0])
#plt.imshow(R)
#plt.show()

