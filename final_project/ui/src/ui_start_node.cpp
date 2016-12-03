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
		//std::cout << "\033[2J\033[1;1H";


		// Print menu.
		std::cout << "MAIN MENU original" << std::endl;
		std::cout << "---------------------------------" << std::endl;

		std::cout << "Options:" << std::endl;
        std::cout << "  1  - Start Mapping:INSTRUCTIONS TO BEGIN" << std::endl;
		std::cout << "  	11 - Start Mapping:Launch specific files and nodes on the ODROID" << std::endl;
		std::cout << "  	12 - Start Mapping:Launch specific files and nodes on the PC" << std::endl;
        std::cout << "  2  - Save the built Map on the ODROID" << std::endl;
        std::cout << "  3  - Start Navigation:INSTRUCTIONS TO BEGIN NAVIGATION" << std::endl;
        std::cout << "  	31 - Start Navigation:Launch specific files and nodes on the ODROID" << std::endl;
        std::cout << "  	32 - Start Navigation:Launch specific files and nodes on the PC" << std::endl;
        std::cout << "  4  - Exit" << std::endl;
		std::cout << "---------------------------------" << std::endl;
		std::cout << "Choice: ";
		std::cin >> input;
		std::cout<<""<<std::endl;

	
		if (input ==1)
		{
			std::cout<<"Firslty set the Master and Hostname on both the machines"<<std::endl;
			std::cout<<"To begin Mapping follow steps 11 and 12"<<std::endl;
			std::cout<<"For performing step 11 first ssh into the odroid "<<std::endl;
			std::cout<<"After ssh, launch this menu and select 11 option"<<std::endl;
			std::cout<<"This would launch specific set of files/nodes on the ODROID"<<std::endl;
			std::cout<<"After this  select option 12 in the PC"<<std::endl;
			std::cout<<"This would launch specific set of files/nodes on the PC"<<std::endl;
			std::cout<<"After mapping choose option 2 on the ODROID to save the built map there"<<std::endl;
            std::cout<<""<<std::endl;
		}
		 else if(input ==11)
		{ 
			system("export TURTLEBOT_3D_SENSOR=kinect &");
			system("roslaunch ui start.launch &") ;
		}
		else if(input ==12)
		{ 
			system("roslaunch turtlebot_rviz_launchers view_navigation.launch &") ;
		}
		 else if(input ==2)
		{ 
			system("rosrun map_server map_saver -f /tmp/my_map &") ;
		}
		else if (input ==3)
		{
			std::cout<<"Before starting Navigation, complete the previous steps and its subparts to generate a map of the environment where to wnat to navigate"<<std::endl;
			std::cout<<"After buiding the maps mark the zones and specify the zones on the code"<<std::endl;
			std::cout<<"Now To begin Navigation to any of the marked zones follow steps 31 and 32"<<std::endl;
			std::cout<<"For performing step 31 first ssh into the odroid "<<std::endl;
			std::cout<<"After ssh, launch this menu and select 31 option"<<std::endl;
			std::cout<<"This would launch specific set of files/nodes on the ODROID"<<std::endl;
			std::cout<<"After this select option 32 in the PC"<<std::endl;
			std::cout<<"This would launch specific set of files/nodes on the PC"<<std::endl;
			std::cout<<""<<std::endl;
            
		}
		 else if(input ==31)
		{
			
			if (access("/tmp/my_map.yaml", F_OK ) != -1 ) 
			{ 
        	system("roslaunch turtlebot_navigation amcl_demo.launch map_file:=/tmp/my_map.yaml &") ;
        	system("roslaunch ui rviz.launch &") ;
        } 
        else 
        { 
        std::cout<<"ERROR:the map file does not exist. Complete optionas 1 and 2  first to map the enivronment where you want to navigate"<<std::endl;
             }

		}
		 else if(input ==32)
		{ 
			system("roslaunch turtlebot_rviz_launchers view_navigation.launch --screen &") ;
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
