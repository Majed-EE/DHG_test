Experiment 1: General steps to make DHG work

Step 1: plug in the device, check if it is connected to the ubuntu VM [TODO insert picture]
Step 2: run the server HOME>Desktop>haptic_glove>dexmo_server - $sudo ./dexmo_server_1.1.6
Step 3: if the glove is connected else the debugging step is insert remove server, insert again, change laptop etc
Note: dexmo serves two purpose; 1. measure joint angle (setpoint/finger position), 2. give stiffness at a specific stepoint (stiffness param at a setpoint)
Step 4: Check if angle is being published; run
Step 5: Check if the stiffness is working; run DHG_R2L_haptic_demo.py

Experiment 2: Connect with ROS

Example 3: Connect with mppt server

Example 4: Connect with flask
