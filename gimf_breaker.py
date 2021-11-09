
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw
 
 
 
class DrawImageHandler():
 
    #COLOR = "#FF0000"
    COLOR = "#000000"
    white = "FFFFFF"
 
    
    def __init__(self):
        self.im = None
        self.draw = None
 
    def getImage(self, path):
        self.im = Image.open(path)
        self.draw = ImageDraw.Draw(self.im)
 
    def drawRect(self, (x1,y1), (x2,y2), width=4 ):
        if width < 4:
            self.__drawRectUnder4((x1,y1), (x2,y2), width)
        else:
            self.__drawRectOver4((x1,y1), (x2,y2), width)  
 
        self.im.show()
        
    def __drawRectUnder4(self, (x1,y1), (x2,y2), width):
        for i in xrange(width):
            self.draw.rectangle([(x1-i, y1-i), (x2+i, y2+i)], outline=self.COLOR)
        
    def __drawRectOver4(self, (x1, y1), (x2,y2), width):
        originwidth = width
        width //=2
        width += 1
        
        self.draw.line([(x1-originwidth, y1-width), (x2+originwidth, y1-width)],
                       width = originwidth, fill=self.COLOR)
        self.draw.line([(x2+width, y1-originwidth), (x2+width, y2+originwidth)],
                       width = originwidth, fill=self.COLOR)
        self.draw.line([(x2+originwidth, y2+width), (x1-originwidth, y2+width)],
                       width = originwidth, fill=self.COLOR)        
        self.draw.line([(x1-width, y2+originwidth), (x1-width, y1-originwidth)],
                       width = originwidth, fill=self.COLOR)
 
        """
        self.draw.line([(x1, y1), (x2, y1),
                        (x2, y2), (x1, y2),
                        (x1, x1)],
                       width= originwidth, fill="blue")
        """        
 
        
    def flushing(self):
        pass
 
    def save(self):
        self.im.save("/home/syscon/Desktop/testing_map.pgm")
 
 
path = "/home/syscon/catkin_ws/src/dock_simulation/sp_gazebo/map/rollout.pgm"
 
# 테스트 코드
if __name__ == "__main__":
    a = DrawImageHandler()
    a.getImage(path)
    a.drawRect((100,100),(400,400), width=8)
    #if rospy.is_shutdown():
    a.save()