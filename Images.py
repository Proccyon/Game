import pyglet as pgl
from pyglet.window import mouse
from pyglet.image.codecs.png import PNGImageDecoder
from pyglet.window import mouse
import numpy as np

ImgPrefix = "C:/Users/Eigenaar/Desktop/New game/Images/"

Stream = open(ImgPrefix+"Grid.png", 'rb')
Grid_Img = pgl.image.load(ImgPrefix+"Grid.png", file=Stream)
Stream = open(ImgPrefix+"Wood1.png", 'rb')
Wood_Img = pgl.image.load(ImgPrefix+"Wood1.png", file=Stream)
Stream = open(ImgPrefix+"Road1.png", 'rb')
Road_Img = pgl.image.load(ImgPrefix+"Road1.png", file=Stream)
Stream = open(ImgPrefix+"Grass1.png", 'rb')
Grass_Img = pgl.image.load(ImgPrefix+"Grass1.png", file=Stream)
Stream = open(ImgPrefix+"Human1.png", 'rb')
Human1_Img = pgl.image.load(ImgPrefix+"Human1.png", file=Stream)