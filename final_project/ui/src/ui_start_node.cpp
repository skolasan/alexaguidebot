#include "ros/ros.h"


int main(int argc, char **argv)
{
    ros::init(argc, argv, "ui_start_node");

	ros::NodeHandle n;



	while(ros::ok())
	{
		// Clear screen.
		int input;
		std::cout << "\033[2J\033[1;1H";


		// Print menu.
		std::cout << "MAIN MENU" << std::endl;
		std::cout << "---------------------------------" << std::endl;

		std::cout << "Options:" << std::endl;
        std::cout << "  1 - Start Mapping" << std::endl;
        std::cout << "  2 - Exit" << std::endl;
		std::cout << "---------------------------------" << std::endl;
		std::cout << "Choice: ";
		std::cin >> input;
		std::cout << std::endl;
	
		if (input == 1)
		{

            system("roslaunch ui start.launch");
		}
        else if(input == 2)
		{
			std::cout << "Exiting..." << std::endl;
			// Call exit service.
			ros::shutdown();
			return 0;
		}
		else
		{
            std::cout << "'" << input << "' is not a valid input." << std:: endl;
			std::cout << "---------------------------------" << std::endl;
			// Continue message.
			std::cout << "Press any key to continue.";
			getchar();
			getchar();
			continue;
		}


	}
	return 0;
}
