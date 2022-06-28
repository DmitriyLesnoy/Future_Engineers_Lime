# Future_Engineers_LIME
project for WRO 2022 Comand LIME, Vladivostok, category Future Engineers
                  
# Programm algoritm
                  
The robot was programmed in Python version 3.9.3. The interpreter was PyCharm.
                                                                                                                
To connect the robot and the computer, take the Ethernet cable to which the computer is connected. Next, using the StartRobot application, we download the program file to the Raspberry microcomputer. It saves it to the SD card and then executes the code.

in the main program of our project, we use the cv2 libraries, regulators, GPIORobot, numpy, time and others.

Initially, we get an image from a 640x480 camera. Then we go straight until we find an image in a special HSV mask of blue or orange color that is not less than a certain number of pixels. From what color we see first, we will understand in which direction we have to move in the future. After we have determined the direction of movement, we turn in the appropriate direction. If the blue line is the first, then the direction of movement is counterclockwise, turn left, if the orange line is the first, then from the direction of movement clockwise, turn left. After qualifying, we drive along the regulator until the next turn, and in the final we dress up to the turn, taking into account the recognition and detour of signs.

In the final program, in contrast to the qualification, there are functions for recognizing signs, an algorithm for calculating the departure from them, and the logic for compiling time maps and arranging signs
In qualifying, things are a little simpler: there are no functions for signs and there is no corresponding logic for calculating the departure. We have at our disposal sensors for recognizing the black border, blue and orange lines on corners, the function of displaying telemetry data. For the most part, the qualification program is the basis for the final program, because in the final you need all the basic recognition functions and algorithms for orientation, line counting as in the qualification.

Our robot movement algorithm with signs is built from several stages (stages). These are: Start, Independent movement, manual control. In the first stage - the robot starts immediately after loading the program, where the robot aligns the torvomotor and gives a signal and downloads. After pressing the start button, the program proceeds to the second stage

The second stage - Independent movement is divided into 2 sub-parts: the traffic controller and the turn control and sign control unit.

In the motion controller, the robot cuts out a part of the image received by the camera and a special HSV mask from the left or right edge, depending on the direction. Thus, we get a piece of the black line - the side on which we will go. We define its y coordinates and the height of the outline. Adding them together, we get a certain numerical distance of the robot from the edge - the side. In the second part - Taxiing signs. With the help of HSV, we find the green and red signs, and then the closest one to us - a larger contour. Then, knowing the direction and color of the nearest sign, we decide in which direction we need to turn. We add this number to the total controller error, as a result of which the robot turns in the right direction.

The remaining stages of the algorithm: Finish, Hand Control are quite simple.

Finish - the robot travels a certain distance in time after passing 12 turns - 3 laps.

Manual control - when you press the arrows on the computer keyboard, the robot moves in the appropriate direction or turns the servo - steering wheels.

Setting up HSV. Here we can switch and watch masks of different colors. Also, here you can configure all the components and after setting or checking, save them and into a file from which values ​​for the filter will be taken in the future.

To load a specific program into the robot, we use a special program called "Start the Robot". When it starts, a special window opens with an interface for transferring files, launching the program and transferring video from the robot.
   There are several buttons in the window:
             "Start download" - downloads a specific program to the robot.
             "Start" - launches the program loaded on the robot.
             "Raw" - runs the verification program
             "Video" - launches video received in real time from the robot's camera
             "Connect to robot" - opens a menu of available robots to connect

We use the Wifi network and Ethernet link to communicate with the robot 

# Systeme queiments for working with the Future Ingeneers progrect:
       
1. Programming environment - PyCharm.
2. Programming language - Python 3.9.
3. Access to the repository on Github and the installed project folder from the repository
4. Bitvise SSH Client
6. presence of certain files on Raspberry Pi
7. The operating system of the computer you will be working on is Windows 10

Installing the required components:

  1) Installing PyCharm:
  
a) Go to PyCharm's official website official website
  ![image](https://user-images.githubusercontent.com/64408062/130711781-79ee401e-7e02-49a1-920c-66a4b4726c01.png)
  
b) Next, select the Windows operating system.
c) Click the download button.
d) Next, the installation file will be downloaded
 ![image](https://user-images.githubusercontent.com/64408062/130711803-9c715735-c8d1-44ce-8397-c6d14d69ca01.png)
 
e) After installing it open it and run the file
f) Next, select the parameters you need.

  2) Installing python language version 3.9:

a) Go to python official site
![image](https://user-images.githubusercontent.com/64408062/130711815-037e32f3-28fa-4c32-aa2f-7c8cdf1639d9.png)

b) Click on the Download button
![image](https://user-images.githubusercontent.com/64408062/130711818-e4e1a168-6aca-40c4-876d-6a86ae7e7f04.png)

c) Scroll down, you will see a list of versions that can be downloaded, select python 3.9
![image](https://user-images.githubusercontent.com/64408062/130711832-22fbb7de-7dd7-4060-b9af-20078230a964.png)

d) You will see the page of this version, scroll down and select the version for the 64-bit operating system
![image](https://user-images.githubusercontent.com/64408062/130711836-78dec598-ce76-4a57-b5db-4f0bb30ba518.png)

e) Next is the installation of the language file.
f) When it is installed, run it, select the options you want and download the language.
g) Then go to pychram, in the upper left corner there will be a File button
![image](https://user-images.githubusercontent.com/64408062/130711840-0d8f880e-082b-4df2-834f-96fa90feb252.png)

h) Then click on the Settings button 
![image](https://user-images.githubusercontent.com/64408062/130711851-316e2926-6819-4b02-af27-55947fc719c1.png)

i) Then go to this section and select the language that you installed G
![image](https://user-images.githubusercontent.com/64408062/130711858-8a8aa72c-8fae-4fef-ae64-9f9a2603bfbf.png)

  3) Installing the project folder from the Github repository:

a) You need to go to the link to the Github repository
![image](https://user-images.githubusercontent.com/64408062/130711877-10222987-3505-4b5d-99ce-d9abd88591ed.png)

b) Then click on the green Code button, then download the zip archive
![image](https://user-images.githubusercontent.com/64408062/130711889-7760187f-8e9c-4201-8ae7-df344aa634f7.png)

c) The download of the project archive should start
![image](https://user-images.githubusercontent.com/64408062/134119396-545e05f7-883c-4ea4-a549-2faed9434958.png)

d) Then unzip the file to a regular folder
![image](https://user-images.githubusercontent.com/64408062/130711920-75e5f5cc-c9a7-4fbc-87e3-0bccbd82862f.png)

  4) Installing Bitvise SSH Client:

a) Go to the official website of the program:![image](https://user-images.githubusercontent.com/64408062/134121813-e6b47f4c-e2d8-4a4e-a426-65c70268e1ca.png)

b) Click on the download button![image](https://user-images.githubusercontent.com/64408062/134121821-8c0e108c-720e-46a4-820f-70513c89bafa.png)

c) Click on the Download Bitvise SSH Client button![image](https://user-images.githubusercontent.com/64408062/134121827-dc956df4-5f0d-4971-bd74-36f514561a46.png)

d) Click on the Download Bitvise SSH Client button![image](https://user-images.githubusercontent.com/64408062/134121837-889cdd95-da75-49eb-b9ec-2d57f3d31c64.png)

e) Then the download of the installation file will start.

f) When the download is finished open the installation file and finish installing the program.  

5)Need to download RobotAPI.py , autostart.py , INGENEERS.py  files to Raspberry Pi
Detailed installation instructions at this link https://raspberrypi-ru.com/%D0%BF%D0%B5%D1%80%D0%B5%D0%B4%D0%B0%D1%87%D0%B0-%D1%84%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2-%D0%BC%D0%B0%D0%BB%D0%B8%D0%BD%D0%B0-ssh/

It is also necessary to upload files main.py, module.py to PyBoard.
To do this, you need to connect PyBoard to your computer using a Micro-USB cable. Then move your main.py and module.py files to the microcontroller


  Starting the robot:

a) Insert the 3.7 Volt accumulators 18650 into the battery compartment of the robot. Do not confuse + and - batteries to avoid consequences.

b) Press the red power button on the robot.

c) When you turn on the PyBoard microcontroller, a sound with an increase in tone will sound, wait until the Raspberry Pi microcomputer starts up, after it finishes starting it will play a melody - a double trill.

  Uploading the project to the robot:

a) Open PyCharm, click on the File button in the upper left corner.
![image](https://user-images.githubusercontent.com/64408062/130712044-5ea0ebe5-6276-4208-be29-139d3f6cd5a3.png)

b) Then click on the Open button
![image](https://user-images.githubusercontent.com/64408062/130712052-7c0dc2f4-4286-48d2-881a-6bcc5f88225d.png)

c) Next, by clicking on the folder icons in the window that opens, select the folder in which the unzipped GitHub repository of the Future Engineers project is located.
![image](https://user-images.githubusercontent.com/64408062/130712057-62ab279d-53b9-4147-8a40-5c5843165fdb.png)
 
d) By default, the folder should be in this path, you can copy and paste into the search box C: \ Users \ user \ Downloads \ Future-Ingeneers
![image](https://user-images.githubusercontent.com/64408062/130712067-68f6a56a-7542-4cd6-9a80-ab40017d7047.png)

e) You should open the project folder
![image](https://user-images.githubusercontent.com/64408062/134128473-15581f11-78e8-4f46-b510-88171a9d424c.png)

f) Connect Raspberry Pi and computer with an Ethernet cable
 
g) Now go back to the PyCharm program, in the project files menu, select and open the Start Robot program
![image](https://user-images.githubusercontent.com/64408062/130712115-b267764d-245f-4b7f-857c-4658daf6621f.png)
 
h) In the right-hand buttons at the top of the screen, click the Run button
![image](https://user-images.githubusercontent.com/64408062/130712126-b69ae1cb-c19c-41aa-8f45-cc1b890994cb.png)

i) Select the Run button, in the small window that opens, select the Start robot program
![image](https://user-images.githubusercontent.com/64408062/130712135-a9f7d0f5-020c-45c7-99df-8c2fbede583f.png)
 
j) This window will open
![image](https://user-images.githubusercontent.com/64408062/130712143-b8af7443-2363-450c-a6aa-446a76d1ff79.png)

k) To load the program on the robot, click on the Load Start button and select the program to start
![image](https://user-images.githubusercontent.com/64408062/130712150-02a863d8-850f-455f-b355-e93e2cb9b61b.png)
 
l) To start starting the program on the robot, press the Start button
![image](https://user-images.githubusercontent.com/64408062/130712160-2179b031-af54-4d44-97ce-7605fc01ea9c.png)

m) To stop the program on the robot, press the Stop button
![image](https://user-images.githubusercontent.com/64408062/130712168-a8edb3db-d2c4-4bbe-83d8-ceb0b76dac9e.png)

n) To get information of , click on the Raw button
![image](https://user-images.githubusercontent.com/64408062/130712175-67f0627e-0cf8-4469-b2ea-83fa13a14708.png)

o) To enable video broadcast from the robot, click the Video button
![image](https://user-images.githubusercontent.com/64408062/130712183-fc1096d7-6929-402b-9db0-e04596887cea.png)

p) But before using all these buttons, you need to connect to the robot using the Connect to robot button.
![image](https://user-images.githubusercontent.com/64408062/130712198-c6ae6424-90f0-4f3b-b113-6f83600f4b86.png)
 
q) Clicking on the button will open a list of robots available to you, select the first option
![image](https://user-images.githubusercontent.com/64408062/130712211-3627f600-62b9-429f-9bb0-4e4da3b389f9.png)
  
r) When the robot and computer are connected to each other, there will be an inscription:
![image](https://user-images.githubusercontent.com/64408062/130712231-f481638b-ce72-46cb-bffb-f21d47d068cd.png)

  Ways to connect to individual components and share files: 
Raspberry Pi:
  To connect to a Raspberry Pi microcomputer, you need to connect it to a monitor via an HDMI cable to display an image, and connect it to a computer via an Ethernet cable. Then, through the command line using the Ifconfig command, we get the Raspberry Pi address data. Find the Ethernet IP address. Enter the address, password, port and username into the Bitvise SSH Client program. This way we can exchange files with the Raspberry Pi. 
