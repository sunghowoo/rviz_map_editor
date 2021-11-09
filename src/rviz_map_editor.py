#!/usr/bin/python

"""********************************************************************
*
* Software License Agreement (BSD License)
*
*  Copyright (c) 2021,  Syscon Engineering Co., Ltd.
						Research Institute. 
*  All rights reserved.
*
* Author: Sungho Woo
* Purpose :Easy map editor using rviz for every engineer. PEACE
*******************************************************************"""
from logging import exception
from PIL import Image, ImageDraw
import rospy, tf, math, traceback
from std_msgs.msg import Bool
from geometry_msgs.msg import *
from laser_perceptions.msg import LaserSampleSetList, LaserSampleSet
from std_srvs.srv import SetBool
import numpy as np
# for marker
import matplotlib.pyplot as plt
from visualization_msgs.msg import Marker
from geometry_msgs.msg import Quaternion
import ros_numpy
import os, pickle
from syscon_msgs.msg import RobotState
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
 
 
 
class DrawImageHandler():
 
    def __init__(self):
        self.im = None
        self.draw = None
        self.subs = []; self.pubs = {}; self.srvs = []
        self.subs.append(rospy.Subscriber("/clicked_point", PointStamped , self.coordinate_cb))

    def coordinate_cb(self, msg):
        
        self.line_coordinate = []
        line_pose = Pose2D() 
        line_pose.x= msg.pose.orientation.x
        line_pose.y= msg.pose.orientation.y
        self.line_coordinate.append(line_pose)

  
	def __del__(self):
		self.shutdown()
		for p in self.pubs.values():p.unregister()
		for s in self.subs:s.unregister()
		rospy.loginfo("[rviz_map_editor] Shutdowning..")

    def getImage(self, path):
        self.im = Image.open(path)
        self.draw = ImageDraw.Draw(self.im)
 
    def drawRect(self, (x1,y1), (x2,y2), width=5 ):
        if width < 4:
            self.__drawLine((x1,y1), (x2,y2), width)
            self.__drawCircle((x1,y1), (x2,y2))
 
        self.im.show()
        
    def __drawLine(self, (x1,y1), (x2,y2), width):
        
        self.draw.line([(x1, y1), (x2, y2)], width = width, fill='black')

    def __drawCircle(self, (x1,y1), (x2,y2) ):

        self.draw.ellipse([(x1, y1), (x2, y2)],fill = 'black' , outline= None)
        
 
    def flushing(self):
        pass
 
    def save(self):
        self.im.save("/home/syscon/Desktop/testing_map.pgm")

    def main(self):
        path = "/home/syscon/Desktop/rviz_map_editor/cradle_world.pgm"
        self.getImage(path)
        if (rospy.is_shutdown()) :
            try:

            if len(self.line_coordinate) > 0 : 
                
                if len(self.line_coordinate) % 2 == 1 : ## delete odd coordinate
                    self.line_coordinate.pop([-1])
                
                for (int i in len(self.line_coordinate)//2):
                    x1 = self.line_coordinate[2*i].pose.x
                    y1 = self.line_coordinate[2*i].pose.x
                    x2 = self.line_coordinate[2*i+1].pose.x
                    y2 = self.line_coordinate[2*i+1].pose.x                                                           
                    self.__drawLine( (x1 , y1 ), (x2 , y2) ,width =3 )


            except Exception, e:
                rospy.logwarn("[rviz_map_editor] %s"%e)
                return False, e
 
if __name__ == "__main__":
    rospy.init_node('rviz_map_editor')    
    
    a = DrawImageHandler()
    a.main()
    #a.getImage(path)
    #a.drawRect((100,100),(200,200), width=3)
    if rospy.is_shutdown():
        a.save()
