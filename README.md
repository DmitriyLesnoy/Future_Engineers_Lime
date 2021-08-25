# Future_Ingeneers
progect to WRO 2021
Comand LIME, Vladivostok, category Future Ingineers

In the development of the LIME team project for the WRO competition in
the Future Engineers category was attended by Lineisky Akim -
programmer, designer, Ivan Terekhov - engineer,
electronics engineer, Glamozdin Yuri - our mentor and trainer.
                                                                                                                                                                                                                                                                                                                                     
The robot was programmed in Python version 3.9.3. The interpreter was PyCharm.
                                                                                                                
To connect the robot and the computer, the robot creates a wi-fi access point to which the computer is connected. Next, using the StartRobot application and the cv2 library, we load the program file onto the Raspberry microcomputer. He saves it to the SD card and then executes the code.
                                                                                                                                                 
As the code is executed, the Raspberry microcomputer continuously sends data packets to PyBoard with its unique number. The PyBoard microcontroller checks that the packet matches this number, in case of a packet malfunction, rejects it. Then the microcontroller already sends commands to the motor and servo

in the main program of our project, we use the cv2 libraries, regulators, RobotAPI and others.

Initially, we get an image from a 640x480 camera. Then we go straight until we find an image in a special HSV mask of blue or orange color no less than a certain number of pixels. It depends on what color we see first, we will understand in which direction we have to move in the future. After we have determined the direction of movement, we turn in the appropriate direction. If the blue line is the first, the direction of movement is counterclockwise, we turn to the left, if the orange line is the first, from the direction of movement is clockwise, we turn to the left.
                                                                                                                                                                                                   
If we need to pass a qualifying race or run a program without taking into account the signs, we have a special variable - a flag denoting qualifications.                                                                                                                                                                                                         
If it is set equal to True, the program will turn off the part responsible for reactions to road signs and will not react to them, it will just eat in a circle in the right direction.                                                                                                                                                                                                                       
                                                                                                                                                                                                                                                                                                                                                                     
Otherwise, if this qualification flag is equal to False, the robot will not change anything or disable any part of the program. He will go to the turn line, determine its color, and accordingly determine the direction of further movement, and will go 3 circles, bypassing the red signs on the right, and the green signs on the left.
                                                                                                                                                                                                                                                                                                                                       
Our algorithm for the movement of a robot with signs is built from several stages (stages).
These are: Movement to the line
         Turning stage - left or right
         Independent movement
         Finish
The first stage - movement to the line has already been mentioned above. The robot drives straight until it sees a blue or orange line. It depends on which line he sees first, he will understand in which direction he will need to move in the future.

The second stage - Independent movement is divided into 2 sub-parts: the movement regulator and the block of the regulator of rotation and steering of signs.

In the motion controller, the robot cuts out a part of the image received by the camera and according to a special HSV mask from the left or right edge, depending on the direction. In this way, we get a piece of the black line - the side along which we will go.
We define its y coordinates and outline height. Putting them together, we get a certain numerical distance of the robot from the edge - the side.
In the second part - Taxiing signs. We use HSV to find green and red signs, and then the closest to us - a larger contour. Then, knowing the direction and the color of the nearest sign, we decide in which direction we need to wrap. We add this cislo to the general error of the regulator, as a result of which the robot turns in the right direction.

The Finish, Hand Control and HSV tuning stages are pretty simple.

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

We use the Wifi network to communicate with the robot.

System requirements for working with the Future Engineers project:

1. The operating system of the computer you will be working on is Windows 10
2. Program interpreter of the python language - PyCharm.
3. Programming language - Python 3.9.
4. The presence of a browser
5. Access to the repository on Github
Installing the required components:
1) Installing PyCharm
a) Go to PyCharm's official website official website
  ![image](https://user-images.githubusercontent.com/64408062/130711781-79ee401e-7e02-49a1-920c-66a4b4726c01.png)
  
b) Next, select the Windows operating system.
c) Click the download button.
d) Next, the installation file will be downloaded
 ![image](https://user-images.githubusercontent.com/64408062/130711803-9c715735-c8d1-44ce-8397-c6d14d69ca01.png)
 
e) After installing it open it and run the file
f) Next, select the parameters you need.
2) Installing python language version 3.9
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
![image](https://user-images.githubusercontent.com/64408062/130711902-bbe2a6b4-dd43-4564-84f8-512b6933b523.png)

d) Then unzip the file to a regular folder
![image](https://user-images.githubusercontent.com/64408062/130711920-75e5f5cc-c9a7-4fbc-87e3-0bccbd82862f.png)


Starting the robot:
a) Insert the 4.2 Volt batteries into the battery compartment of the robot. Do not confuse + and - batteries to avoid consequences.
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
![image](https://user-images.githubusercontent.com/64408062/130712087-af4306a5-1003-45d9-932b-2af75b251c71.png)

f) To upload files to the Raspberry Pi, you need to open the Windows network menu in the bottom right corner
![image](https://user-images.githubusercontent.com/64408062/130712093-5f4a6bd5-bd97-4140-808f-b853595bd762.png)
 
g) Select Lime network
![image](https://user-images.githubusercontent.com/64408062/130712103-b2d6f460-d7ce-4778-bd87-20029b2cac8b.png)
 
h) Then enter the password and connect to the network
![image](https://user-images.githubusercontent.com/64408062/130712106-20039819-0590-4ad2-8c0b-9cb786571605.png)
 
i) Now go back to the PyCharm program, in the project files menu, select and open the Start Robot program
![image](https://user-images.githubusercontent.com/64408062/130712115-b267764d-245f-4b7f-857c-4658daf6621f.png)
 
j) In the right-hand buttons at the top of the screen, click the Run button
![image](https://user-images.githubusercontent.com/64408062/130712126-b69ae1cb-c19c-41aa-8f45-cc1b890994cb.png)

k) Select the Run button, in the small window that opens, select the Start robot program
![image](https://user-images.githubusercontent.com/64408062/130712135-a9f7d0f5-020c-45c7-99df-8c2fbede583f.png)
 
l) This window will open
![image](https://user-images.githubusercontent.com/64408062/130712143-b8af7443-2363-450c-a6aa-446a76d1ff79.png)

m) To load the program on the robot, click on the Load Start button and select the program to start
![image](https://user-images.githubusercontent.com/64408062/130712150-02a863d8-850f-455f-b355-e93e2cb9b61b.png)
 
n) To start starting the program on the robot, press the Start button
![image](https://user-images.githubusercontent.com/64408062/130712160-2179b031-af54-4d44-97ce-7605fc01ea9c.png)

o) To stop the program on the robot, press the Stop button
![image](https://user-images.githubusercontent.com/64408062/130712168-a8edb3db-d2c4-4bbe-83d8-ceb0b76dac9e.png)

p) To restart the program on the robot, click on the Raw button
![image](https://user-images.githubusercontent.com/64408062/130712175-67f0627e-0cf8-4469-b2ea-83fa13a14708.png)

q) To enable video broadcast from the robot, click the Video button
![image](https://user-images.githubusercontent.com/64408062/130712183-fc1096d7-6929-402b-9db0-e04596887cea.png)

r) But before using all these buttons, you need to connect to the robot using the Connect to robot button.
![image](https://user-images.githubusercontent.com/64408062/130712198-c6ae6424-90f0-4f3b-b113-6f83600f4b86.png)
 
s) Clicking on the button will open a list of robots available to you, select the first option
![image](https://user-images.githubusercontent.com/64408062/130712211-3627f600-62b9-429f-9bb0-4e4da3b389f9.png)
  
t) When the robot and computer are connected to each other, there will be an inscription:
![image](https://user-images.githubusercontent.com/64408062/130712231-f481638b-ce72-46cb-bffb-f21d47d068cd.png)

Ways to connect to individual components:
a) To connect directly to the Raspberry Pi, you need to remove the Micro SD, then connect it to the computer, or use a USB cable, micro USB to plug it into the microcomputer and then into the computer.

b) To connect directly to PyBoard, you need to connect the Micro USB cable to the microcontroller connector and to the computer. 
