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
 * measure_tool.cpp
 *
 *  Created on: Aug 8, 2012
 *      Author: gossow
 */

#include "line_tool.h"

#include <rviz/ogre_helpers/line.h>
#include <rviz/viewport_mouse_event.h>
#include <rviz/display_context.h>
#include <rviz/selection/selection_manager.h>
#include <rviz/load_resource.h>

#include <OGRE/OgreSceneNode.h>

#include <sstream>

namespace rviz
{
LineTool::LineTool() : state_(START), length_(-1)
{
}

LineTool::~LineTool()
{
  delete line_;
}

void LineTool::onInitialize()
{
  
  pub_line = nh.advertise<geometry_msgs::PointStamped>("/line", 1);
  line_ = new Line(context_->getSceneManager());

  std_cursor_ = getDefaultCursor();
  hit_cursor_ = makeIconCursor("package://rviz_map_editor/icons/classes/Measure.svg");
}

void LineTool::activate()
{
  state_ = START;
}

void LineTool::deactivate()
{
}

int LineTool::processMouseEvent(ViewportMouseEvent& event)
{
  int flags = 0;

  Ogre::Vector3 pos;

  std::stringstream ss;

  bool success = context_->getSelectionManager()->get3DPoint(event.viewport, event.x, event.y, pos);
  setCursor(success ? hit_cursor_ : std_cursor_);

  switch (state_)
  {
  case START:
    break;
  case END:
    if (success)
    {
      line_->setPoints(start_, pos);
      length_ = (start_ - pos).length();
    }
    break;
  }

  if (length_ > 0.0)
  {
    ss << "[Length: " << length_ << "m] ";
  }

  ss << "Click on two points to measure their distance. Right-click to reset.";
  setStatus(QString(ss.str().c_str()));
  geometry_msgs::PointStamped point;
  
  if (event.leftUp() && success)
  {
    switch (state_)
    {
    case START:
      start_ = pos;
      state_ = END;
      point.point.x = pos.x;
      point.point.y = pos.y;
      pub_line.publish(point);
      //start_coo.push_back(start_);
      break;
    case END:
      end_ = pos;
      state_ = START;
      line_->setPoints(start_, end_);
      point.point.x = pos.x;
      point.point.y = pos.y;
      pub_line.publish(point);
      line_ =new Line(context_->getSceneManager());
      line_ ->setPoints(start_, end_);
      break;
    }

    flags |= Render;
  }

  if (event.rightUp())
  {
    state_ = START;
    line_->setVisible(false);
  }

  return flags;
}

} /* namespace rviz */


#include <pluginlib/class_list_macros.hpp>
PLUGINLIB_EXPORT_CLASS(rviz::LineTool, rviz::Tool)
