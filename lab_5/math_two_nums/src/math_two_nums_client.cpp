#include "ros/ros.h"
#include "math_two_nums/MathTwoNums.h"
#include "std_srvs/Empty.h"

int main(int argc, char **argv)
{
	ros::init(argc, argv, "sum_two_nums_client");
	ros::NodeHandle node;

	// Setup the client for mathing two numbers.
	ros::ServiceClient mathClient =
	  node.serviceClient<math_two_nums::MathTwoNums>("math_two_nums");

	// Setup client to exit session.
	ros::ServiceClient exitClient = node.serviceClient<std_srvs::Empty>("exit");

	/***************************
	 *
	 * SETUP MODE CLIENT HERE.
	 *
	 ***************************/

	std::string mode = "ADDITION";

	while(ros::ok())
	{
		std::string input;

		// Clear screen.
		std::cout << "\033[2J\033[1;1H";

		// Print menu.
		std::cout << "MAIN MENU" << std::endl;
		std::cout << "---------------------------------" << std::endl;
		std::cout << "Current mode: " << mode << std::endl;
		std::cout << "Options:" << std::endl;
		std::cout << "  N - Enter numbers" << std::endl;
		std::cout << "  M - Enter mode" << std::endl;
		std::cout << "  E - Exit" << std::endl;
		std::cout << "---------------------------------" << std::endl;
		std::cout << "Choice: ";
		std::cin >> input;
		std::cout << std::endl;

		if (input == "N" || input == "n")
		{
			// Handle the enter numbers choice.

			// Clear screen.
			std::cout << "\033[2J\033[1;1H";

			// Print number menu.
			std::cout << "ENTER NUMBERS" << std::endl;
			std::cout << "---------------------------------" << std::endl;
			std::cout << "Current mode: " << mode << std::endl;
			std::cout << "---------------------------------" << std::endl;

			// Get the first number.
			std::cout << "Enter first number: ";
			std::cin >> input;
			std::cout << std::endl;

			// Convert first number to a float.
			float first;
			try
			{
				first = std::stof(input);
			}
			catch (...)
			{
				std::cout << "'" << input << "'  is not a number" << std::endl;
				std::cout << "---------------------------------" << std::endl;

				// Continue message.
				std::cout << "Press any key to continue.";
				getchar();
				getchar();
				continue;
			}

			// Get the second number.
			std::cout << "Enter second number: ";
			std::cin >> input;
			std::cout << std::endl;

			// Convert second number to a float.
			float second;
			try
			{
				second = std::stof(input);
			}
			catch (...)
			{
				std::cout << "'" << input << "'  is not a number" << std::endl;
				std::cout << "---------------------------------" << std::endl;

				// Continue message.
				std::cout << "Press any key to continue.";
				getchar();
				getchar();
				continue;
			}

			// Setup the service request.
			math_two_nums::MathTwoNums srv;
			srv.request.a = first;
			srv.request.b = second;

			// Call the service request.
			if (mathClient.call(srv))
			{
				std::cout << "Result: " << srv.response.result << std::endl;
			}
			else
			{
				std::cout << "Failed to call service math_two_nums";
				return 1;
			}

			std::cout << "---------------------------------" << std::endl;

			// Continue message.
			std::cout << "Press any key to continue.";
			getchar();
			getchar();
			continue;
		}
		else if (input == "M" || input == "m")
		{
			// Handle the enter mode choice.

			// Clear screen.
			std::cout << "\033[2J\033[1;1H";

			// Print mode menu.
			std::cout << "MAIN MENU" << std::endl;
			std::cout << "---------------------------------" << std::endl;
			std::cout << "Current mode: " << mode << std::endl;
			std::cout << "Options:" << std::endl;
			std::cout << "  A - Addition" << std::endl;
			std::cout << "  S - Subtraction" << std::endl;
			std::cout << "  M - Multiplication" << std::endl;
			std::cout << "  D - Division" << std::endl;
			std::cout << "  E - Exit" << std::endl;
			std::cout << "---------------------------------" << std::endl;
			std::cout << "Enter mode: ";
			std::cin >> input;
			std::cout << std::endl;

			// Check if the mode is valid.
			if (input == "A" || input == "a")
			{
				mode == "ADDITION";
			}
			else if (input == "S" || input == "s")
			{
				mode = "SUBTRACTION";
			}
			else if (input == "M" || input == "m")
			{
				mode == "MULTIPLICATION";
			}
			else if (input == "D" || input == "d")
			{
				mode == "DIVISION";
			}
			else if (input == "E" || input == "e")
			{
				std::cout << "Exiting..." << std::endl;

				// Call exit service.
				std_srvs::Empty exitSrv;
				exitClient.call(exitSrv);

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

			/********************************
			 *
			 * HANDLE SETTING THE MODE HERE.
			 *
			 ********************************/

			std::cout << "Mode set to " << mode << std::endl;
			std::cout << "---------------------------------" << std::endl;

			// Continue message.
			std::cout << "Press any key to continue.";
			getchar();
			getchar();
			continue;
		}
		else if (input == "E" || input == "e")
		{
			std::cout << "Exiting..." << std::endl;

			// Call exit service.
			std_srvs::Empty exitSrv;
			exitClient.call(exitSrv);

			return 0;
		}
		else
		{
			std::cout << "'" << input << "' is not a valid choice." << std:: endl;
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
