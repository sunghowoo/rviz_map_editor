/*
 * Copyright (c) 2008, Willow Garage, Inc.
 * All rights reserved.
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in the
 *       documentation and/or other materials provided with the distribution.
 *     * Neither the name of the Willow Garage, Inc. nor the names of its
 *       contributors may be used to endorse or promote products derived from
 *       this software without specific prior written permission.
 *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
 * AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
 * ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
 * LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
 * CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
 * SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
 * INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
 * CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
 * ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 * POSSIBILITY OF SUCH DAMAGE.
 */
/*
 * measure_tool.h
 *
 *  Created on: Aug 8, 2012
 *      Author: gossow
 */

#ifndef LINE_TOOL_H_
#define LINE_TOOL_H_

#include <rviz/tool.h>
#include <ros/ros.h>
#include <ros/console.h>
#include <OGRE/OgreVector3.h>
#include <geometry_msgs/PointStamped.h>


namespace rviz
{
class Line;

class LineTool : public Tool
{
public:
  LineTool();

  ~LineTool() override;

  void onInitialize() override;

  void activate() override;
  void deactivate() override;

  int processMouseEvent( ViewportMouseEvent& event) override;

private:
  enum
  {
    START,
    END
  } state_;

  Line* line_ ;
  Ogre::Vector3 start_;
  Ogre::Vector3 end_;
  float length_;

  QCursor std_cursor_;
  QCursor hit_cursor_;

  ros::NodeHandle nh;
  ros::Publisher pub_line;
};

} /* namespace rviz */
#endif /* Line_TOOL_H_ */
