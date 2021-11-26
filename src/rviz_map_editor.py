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
from nav_msgs.msg import *
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
        rospy.logwarn("[rviz_map_editor] successfully start editing map  ")
        robot_number = rospy.get_param("~robot_number", '') 
        self.line_coordinate = []
        self.remove_coordinate =[]
        self.im = None
        self.draw = None
        self.subs = []; self.pubs = {}; self.srvs = []
        self.subs.append(rospy.Subscriber("/line", PointStamped , self.coordinate_cb))
        self.subs.append(rospy.Subscriber("/remove", PointStamped , self.remove_cb))
        self.subs.append(rospy.Subscriber("%s/map"%robot_number, OccupancyGrid , self.map_cb))
         
        self.running_once = False

	def __del__(self):
		self.shutdown()
		for p in self.pubs.values():p.unregister()
		for s in self.subs:s.unregister()
		rospy.loginfo("[rviz_map_editor] Shutdowning..")

    def coordinate_cb(self, msg):
        
        line_pose_array = []
        line_pose = Pose2D() 
        line_pose.x= msg.point.x
        line_pose.y= msg.point.y
        line_pose_array.append(line_pose)
        self.line_coordinate.append(line_pose_array)
        rospy.loginfo("[rviz_map_editor] coordinate_cb: %s ",self.line_coordinate )

    def remove_cb(self, msg):
        remove_pose_array = []
        remove_pose = Pose2D() 
        remove_pose.x= msg.point.x
        remove_pose.y= msg.point.y
        remove_pose_array.append(remove_pose)
        self.remove_coordinate.append(remove_pose_array)
        rospy.loginfo("[rviz_map_editor] remove_cb :  %s ",self.remove_coordinate )


    def map_cb(self,msg):

        self.width = msg.info.width 
        self.height = msg.info.height
        self.resolution =msg.info.resolution 
        self.origin_x = msg.info.origin.position.x
        self.origin_y =msg.info.origin.position.y

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

        self.draw.ellipse([(x1, y1), (x2, y2)],fill = 'white' , outline= None)
        
 
    def flushing(self):
        pass
 
    def save(self):
        save_path = rospy.get_param("~save_path", "/home/syscon/catkin_ws/src/rviz_map_editor/edit_.pgm" )
        self.im.save(save_path)
        rospy.logwarn("[rviz_map_editor] successfully save map (~ing)  ")

    def global_to_pixel_x(self,coordinate):

        return     (1/self.resolution) *  (coordinate - self.origin_x) 
        
    def global_to_pixel_y(self,coordinate):

        return     self.height-(1/self.resolution) * ( coordinate - self.origin_y) 


    def main(self):
    
        while(True):
            try:
                if rospy.is_shutdown():
                    if self.running_once == False:            
                        if len(self.line_coordinate) > 1 : 
                            
                            if len(self.line_coordinate) % 2 == 1 : ## delete odd coordinate
                                self.line_coordinate.pop(-1)
                            i = 0
                            division =  len(self.line_coordinate) // 2 
                            for  i in range(0, division) :

                                x1 = self.global_to_pixel_x( self.line_coordinate[2*i][0].x  )
                                y1 = self.global_to_pixel_y(self.line_coordinate[2*i][0].y  )
                                x2 = self.global_to_pixel_x(self.line_coordinate[2*i+1][0].x  )
                                y2 = self.global_to_pixel_y(self.line_coordinate[2*i+1][0].y  )                                                        
                                self.__drawLine( (x1 , y1 ), (x2 , y2) ,width =1 )

                        if len(self.remove_coordinate) > 0:
                            i = 0
                            radius = 1
                            r = (1/self.resolution) * radius 
                            for i in range(0,len(self.remove_coordinate)):
                                x_r1 = self.global_to_pixel_x( self.remove_coordinate[i][0].x )
                                y_r1 = self.global_to_pixel_y(self.remove_coordinate[i][0].y )
                                self.__drawCircle( (x_r1-r , y_r1 -r ), (x_r1+r , y_r1+r) )
                                #rospy.loginfo("[rviz_map_editor] pix_coordinate x :  %s ",x1 )
                                #rospy.loginfo("[rviz_map_editor] pix_coordinate y :  %s ",y1)
                                
                        self.save()
                        self.running_once =True
                        
            except Exception, e:
                rospy.logwarn("[rviz_map_editor] %s"%traceback.format_exc())
                return False

if __name__ == "__main__":
    rospy.init_node('rviz_map_editor')    
    a = DrawImageHandler()
    path = rospy.get_param("~load_path", "/home/syscon/catkin_ws/src/rviz_map_editor/rollout.pgm")
    a.getImage(path)    
    a.main()

     

