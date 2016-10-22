#!/usr/bin/env python
import roslib
roslib.load_manifest('motion_detector')
import sys
import rospy
import cv2
import numpy as np
from motion_detector.srv import Mode
from motion_detector.srv import ModeResponse
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImageConverter:

   def __init__(self):
      self.mode=0
      self.output_image_pub = rospy.Publisher("image_converter/output_video",Image)
      self.mode_service = rospy.Service("change_mode",Mode,self.handle_mode_change);
      self.bridge = CvBridge()
      self.image_sub = rospy.Subscriber("/usb_cam/image_raw",Image,self.callback)
      self.bg_img_captured=False

   def FarnebackAlgorithm(self,grayscale_prev_img,grayscale_next_img,orig_next_img):
      flow_map = cv2.calcOpticalFlowFarneback(grayscale_prev_img, \
                     grayscale_next_img, 0.5, 3, 15, 3, 5, 1.2, 0)
      h, w = flow_map.shape[:2]
      fx, fy = flow_map[:,:,0], flow_map[:,:,1]
      magnitude_vector = fx*fx+fy*fy
      frame_mean=np.mean(magnitude_vector);
      # Added 1.5 to account for small errors in flow map calculation
      ret,flow_mask = cv2.threshold(magnitude_vector, frame_mean+1.5, \
                        255, cv2.THRESH_BINARY);
      # Morphological close operation to fill unfilled white contours
      # 15x15 kernel
      kernel = np.ones((15,15),np.uint8)
      flow_mask = cv2.morphologyEx(flow_mask, cv2.MORPH_CLOSE, kernel)
      #Find contours and discard contours with small areas
      contours,hierarchy = cv2.findContours(np.uint8(flow_mask),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      for cnt in contours:
        if(cv2.contourArea(cnt)>1000):
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(orig_next_img,(x,y),(x+w,y+h),(0,255,0),2)
      return orig_next_img

   def handle_mode_change(self,req):
      if req.mode < req.RAW_VIDEO or req.mode > req.MIX_OF_GAUSSIANS:
         return ModeResponse(False)
      self.mode = req.mode
      return ModeResponse(True)

   def callback(self,data):
       try:
         cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
         if(not self.bg_img_captured):
            self.bg_image = cv_image
            self.grayscale_prev_img = cv2.cvtColor(self.bg_image,cv2.COLOR_BGR2GRAY) 
            self.bg_img_captured = True
            return
       except CvBridgeError as e:
         print(e)
   
       try:
         if self.mode == 0:
            self.output_image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
         elif self.mode == 1:
            grayscale_next_img=cv2.cvtColor(cv_image,cv2.COLOR_BGR2GRAY);
            output_img=self.FarnebackAlgorithm(self.grayscale_prev_img,grayscale_next_img,cv_image)
            self.grayscale_prev_img=grayscale_next_img
            self.output_image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"));
       except CvBridgeError as e:
         print(e)
   
def main(args):
   ic = ImageConverter()
   rospy.init_node('motion_detector_python', anonymous=True)
   try:
      rospy.spin()
   except KeyboardInterrupt:
      print("Shutting down")
      rospy.shutdown();

if __name__ == '__main__':
   main(sys.argv)
