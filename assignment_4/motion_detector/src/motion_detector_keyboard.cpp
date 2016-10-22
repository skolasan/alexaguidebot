#include "ros/ros.h"
#include "std_srvs/Empty.h"
#include "motion_detector/Mode.h"

int main(int argc, char **argv)
{
	ros::init(argc, argv, "motion_detector_keyboard");

	ros::NodeHandle n;

	// Setup client to exit session.
	ros::ServiceClient exitClient = n.serviceClient<std_srvs::Empty>("exit");
	ros::ServiceClient modeClient = n.serviceClient<motion_detector::Mode>("change_mode");

	/*************************************
	*
	* FILL IN YOUR FUNCTIONALITY HERE.
	*
	*************************************/
	std::string mode("Raw Video");
	while(ros::ok())
	{
		// Clear screen.
		int input;
		std::cout << "\033[2J\033[1;1H";
		motion_detector::Mode mode_srv;

		// Print menu.
		std::cout << "MAIN MENU" << std::endl;
		std::cout << "---------------------------------" << std::endl;
		std::cout << "Current mode: " << mode << std::endl;
		std::cout << "Options:" << std::endl;
		std::cout << "  1 - Raw Video" << std::endl;
		std::cout << "  2 - Farnback Algorithm" << std::endl;
		std::cout << "  3 - Improved Mixture Of Gaussains" << std::endl;
		std::cout << "  4 - Exit" << std::endl;
		std::cout << "---------------------------------" << std::endl;
		std::cout << "Choice: ";
		std::cin >> input;
		std::cout << std::endl;
	
		if (input == 1)
		{
			mode_srv.request.mode=motion_detector::ModeRequest::RAW_VIDEO;
			mode="Raw Video";
		}
		else if(input == 2)
		{
			mode_srv.request.mode=motion_detector::ModeRequest::FARNBACK;
			mode="Farnback Algorithm";
		}
		else if(input == 3)
		{
			mode_srv.request.mode=motion_detector::ModeRequest::MIX_OF_GAUSSIANS;
			mode="Improved Mixture Of Gaussains";
		}
		else if(input == 4)
		{
			std::cout << "Exiting..." << std::endl;
			// Call exit service.
			std_srvs::Empty exitSrv;
			exitClient.call(exitSrv);
			ros::shutdown();
			return 0;
		}
		else
		{
			std::cout << "'" << input << "' is not a valid mode." << std:: endl;
			std::cout << "---------------------------------" << std::endl;
			// Continue message.
			std::cout << "Press any key to continue.";
			getchar();
			getchar();
			continue;
		}
		if(modeClient.call(mode_srv) == true)
		{
			if(mode_srv.response.result)
			{
				std::cout << "Mode set to " << mode << std::endl;
				std::cout << "---------------------------------" << std::endl;
			}
			else
			{
				std::cout << "Mode Change Failed" << std::endl;
				return 1;
			}
		}
		else
		{
			std::cout << "Failed to call mode service " << std::endl;
			return 1;
		}
	}
	return 0;
}
