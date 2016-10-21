#include "ros/ros.h"
#include "math_two_nums/MathTwoNums.h"
#include "math_two_nums/Mode.h"
#include "std_srvs/Empty.h"
#include "cmath"

int mode;
math_two_nums::Mode::Request mode_req;

bool mathCallback(math_two_nums::MathTwoNums::Request  &req,
                  math_two_nums::MathTwoNums::Response &res)
{
	ROS_INFO("request: x=%f, y=%f", req.a, req.b);

	/*********************************
	 *
	 * DO THE MATH BASED ON THE MODE
	 *
	 *********************************/
	if (mode == mode_req.ADDITION)
	{
		res.result = req.a + req.b;
		res.error="SUCCESS";
	}

	if (mode == mode_req.SUBTRACTION)
	{
		res.result = req.a - req.b;
		res.error="SUCCESS";
	}

	if (mode == mode_req.MULTIPLICATION)
	{
		res.result = req.a * req.b;
		res.error="SUCCESS";
	}

	if (mode == mode_req.DIVISION)
	{
		if(req.b != 0)
		{
			res.result = req.a / req.b;
			res.error="SUCCESS";
		}
		else
		{
			res.result = NAN;
			res.error="Divide by zero";
		}
	}

	ROS_INFO("sending back response: %f", res.result);
	return true;
}

bool modeCallback(math_two_nums::Mode::Request  &req,
					math_two_nums::Mode::Response &res)
{
	ROS_INFO("mode: %d", req.mode);
	mode = req.mode;
	res.result=true;
	return true;
}

bool exitCallback(std_srvs::Empty::Request &req,
                  std_srvs::Empty::Response &res)
{
	ros::shutdown();

	return true;
}

/******************************
 *
 * SETUP MODE CALLBACK HERE.
 *
 ******************************/

int main(int argc, char **argv)
{
	ros::init(argc, argv, "math_two_nums_server");
	ros::NodeHandle node;

	ros::ServiceServer mathServer = node.advertiseService("math_two_nums", mathCallback);
	ros::ServiceServer modeServer = node.advertiseService("set_math_mode", modeCallback);

	ros::ServiceServer exitServer = node.advertiseService("exit", exitCallback);

	/******************************
	 *
	 * SETUP THE MODE SERVER HERE.
	 *
	 ******************************/

	ROS_INFO("Ready to math two nums.");

	ros::spin();

  return 0;
}
