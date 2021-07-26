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