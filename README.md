# **Project Proposal** #
# **Robot Name :** Alexa_guide (subject to change) #

## **Task :** Unknown territory mapping with teleoperation, and intelligent map-based navigation with voice interaction.

## **Task Description** : 
### **Part 1** : Unknown territory mapping using Teleoperation  ###
Robo_guide will be deployed in an unknown territory. It will be remotely tele-operated via keyboard aided with a GUI. We will be receiving a live video feed from the robot for feedback. We will be using the kinect sensor to image and map the environment. A slam algorithm will be running in the background, to localize and map the robot. After covering the Area of Interest (AOI), the map will be stored in the server.

### **Part 2** : Intelligent navigation towards a goal using map ###
The user interacts with our system to choose a goal point from the previous map. The robot uses the map, computes a path to the goal. 'Alexa' is the framework from Amazon for voice command recognition which we are employing. The robot guides the user through this path avoiding new obstacles if any, and reaches the goal. 

## **Sensors Used**:
1. Microsoft Kinect (Mapping and SLAM)
2. IR Sensor (Obstacle detection)
3. Web Camera (Send live image feed)
4. Microphone (Input voice commands)
5. Inbuilt encoders (Odometry)

## Technical details:

1. We use a AWS lambda to host our alexa service if you want to reuse this code please create a AWS account to host the lambda.
2. We have implemented a request response framework over mqtt. The code uses a public mqtt service make sure to change it to custom one.

https://www.youtube.com/watch?v=Oec4eM-5SjE
