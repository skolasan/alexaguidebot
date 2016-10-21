#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include "ros/ros.h"

enum operating_modes_e
{
	RAW_PASS_THROUGH=0
};
typedef operating_modes_e operating_modes_t;

class ImageConverter
{
	ros::NodeHandle m_nh;
	image_transport::ImageTransport m_it;
	image_transport::Subscriber m_image_sub;
	image_transport::Publisher m_image_pub;
	operating_modes_t mode;

public:
	ImageConverter()
		: m_it(m_nh),mode(RAW_PASS_THROUGH)
	{
		// Subscrive to input video feed and publish output video feed
		m_image_sub = m_it.subscribe("/usb_cam/image_raw", 1, 
									&ImageConverter::ImageCb, this);
		m_image_pub = m_it.advertise("/image_converter/output_video", 1);
  }

	~ImageConverter()
	{
	}

	void ImageCb(const sensor_msgs::ImageConstPtr& msg)
	{
		cv_bridge::CvImagePtr cv_ptr;
		try
		{
			cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
		}
		catch (cv_bridge::Exception& e)
		{
			ROS_ERROR("cv_bridge exception: %s", e.what());
			return;
		} 
		// Output modified video stream
		m_image_pub.publish(cv_ptr->toImageMsg());
	}
};


int main(int argc, char **argv)
{
	ros::init(argc, argv, "motion_detector_node");
	/*************************************
	*
	* FILL IN YOUR FUNCTIONALITY HERE.
	*
	*************************************/
	ImageConverter ic;
	ros::spin();
	return 0;
}
