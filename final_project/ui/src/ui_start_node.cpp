#include "ros/ros.h"
#include <unistd.h>

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
        std::cout << "  2 - Save the built Map" << std::endl;
        std::cout << "  3 - Start Navigation" << std::endl;
        std::cout << "  4 - Exit" << std::endl;
		std::cout << "---------------------------------" << std::endl;
		std::cout << "Choice: ";
		std::cin >> input;
		std::cout << std::endl;
	
		if (input == 1)
		{

            system("roslaunch ui start.launch")&;
		}
		 else if(input == 2)
		{
			system("rosrun map_server map_saver -f /tmp/my_map")&;
		}
		 else if(input == 3)
		{
			if (access("/tmp/my_map.yaml", F_OK ) != -1 ) 
			{ 
        	system("roslaunch turtlebot_navigation amcl_demo.launch map_file:=/tmp/my_map.yaml")&;
			system("roslaunch ui rviz.launch")&;
        } 
        else 
        { 
        std::cout<<"ERROR:file does not exist. Complete operations associated with Input 1 and 2 first"<<std::endl;
             }

		}
        else if(input == 4)
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
