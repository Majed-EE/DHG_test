
from socket import *
import threading
import src
from proto_util import ctrl_command_pb2 as command
import time
from datetime import datetime

import numpy as np

import logging
import os

file_name=__file__
file_name=file_name[:-3]+"_log.log"
logging.basicConfig(
    filename=file_name,
    level=logging.INFO,
    format='%(asctime)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logging.info("file name: %s",file_name)



threads=[]
global act_time_stamp, press_time_stamp, n_index, array_n,cmd_dict,yn,joint_name,active_joint,points
# act_time_stamp is the actual time stamp
t_Start = time.time() # reference time



array_n=0

cmd_dict={}
joint_name=["Thumb","Index","Middle","Ring","Pinky"]

print("info for the active joint: ")
print("default cmd dict: ")

def dex_force(set_point, stiffness, rest=True): # works same as before
    global cmd_dict, active_joint
    if not rest:
        for x in range (len(joint_name)):
                if stiffness>0:
                    cmd_dict[joint_name[x]]={"Stiffness":stiffness,"SetPoint":set_point}
                else:
                    cmd_dict[joint_name[x]]={"Stiffness":0,"SetPoint":0} # relax condition

    else:
        for x in range (len(joint_name)):
            cmd_dict[joint_name[x]]={"Stiffness":0,"SetPoint":0} # relax condition
        return False
    print(cmd_dict)
dex_force(0,0,True) # initial the cmd_dict

def set_test_impedance_control():
    global cmd_dict
    new_impedance_control = command.ImpedanceControl()
    new_impedance_control.Thumb.Stiffness = cmd_dict["Thumb"]["Stiffness"] #0.5  # 0-1,stand for hardness of the force,0 stand for no force
    new_impedance_control.Thumb.SetPoint =  cmd_dict["Thumb"]["SetPoint"] #0.3  # 0-1,stand for position of the force,sign stand for direction,positive number for inward,minus number for outward
    new_impedance_control.Index.Stiffness = cmd_dict["Index"]["Stiffness"] #1
    new_impedance_control.Index.SetPoint =  cmd_dict["Index"]["SetPoint"] #1
    new_impedance_control.Middle.Stiffness = cmd_dict["Middle"]["Stiffness"]#0.5
    new_impedance_control.Middle.SetPoint = cmd_dict["Middle"]["SetPoint"] #-0.8
    new_impedance_control.Ring.Stiffness = cmd_dict["Ring"]["Stiffness"] #0.5
    new_impedance_control.Ring.SetPoint =  cmd_dict["Ring"]["SetPoint"] #0.5
    new_impedance_control.Pinky.Stiffness = cmd_dict["Pinky"]["Stiffness"] #0.5
    new_impedance_control.Pinky.SetPoint =  cmd_dict["Pinky"]["SetPoint"] #0.5
    new_impedance_control.has_index = True  # true stand for the command cannot be ignore,false stand for the command can be ignore
    return new_impedance_control



def test_worker(command_write_worker,stiffness,set_point):
    
    global cmd_dict
    print("inside test worker")
    dex_force(set_point,stiffness,True)
    new_impedance_control = set_test_impedance_control()
    command_write_worker.add_new_impedance_control(337785601,new_impedance_control)
    
    time.sleep(5)



#break


# connect to server

host_ip = "127.0.0.1"
host_port = 55555
sock = socket(AF_INET, SOCK_STREAM)
sock.connect((host_ip, host_port))
print("changing")

try:

	command_write_worker_i = src.command_write_worker(sock)
	command_write_worker_t = threading.Thread(target=command_write_worker_i.worker,name="Thread_command_worker")
	command_write_worker_t.start()
        threads.append(command_write_worker_t)

	test_worker(command_write_worker_i)
	print("################## Ending loop #######################")
        print("graceful shutdown test")

	print("################## Temporal Resolution calcultaion #####################")
	# Temporal Resolution
	

	sock.close()
	print("total number of thread {}".format(len(threads)))
	for thread in threads:
		print("inside thread  {}".format(thread.name))
		if thread.is_alive():
			print("thread is alive name: {}".format(thread.name))
			thread.join()
except KeyboardInterrupt:
	print("keyboard interrupt")
	for thread in threads:
		print("inside thread  {}".format(thread.name))
		if thread.is_alive():
			print("thread is alive name: {}".format(thread.name))
			thread.join()

finally:
        # Close the socket
        sock.close()
        print("Socket disconnected.")







import socket
from socket import AF_INET, SOCK_STREAM
import time
import threading
# import src  # Uncomment if using src module

class ImpedanceControlManager:
    def __init__(self, host_ip="127.0.0.1", host_port=55555):
        """
        Initialize the Impedance Control Manager
        
        :param host_ip: IP address to connect to
        :param host_port: Port to connect to
        """
        self.host_ip = host_ip
        self.host_port = host_port
        self.sock = None
        self.command_write_worker_i = None
        self.threads = []
        self.new_impedance_control = None
        
        # Initialize command dictionary and joint names
        self.cmd_dict = {}
        self.joint_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        

        print("default cmd dict: ")
        
        # Initialize cmd_dict
        self.dex_force(0, 0, True)
    
    def dex_force(self, set_point, stiffness, rest=True):
        """
        Works same as before - set force parameters for all joints
        
        :param set_point: Set point value for joints
        :param stiffness: Stiffness value for joints
        :param rest: If True, relax all joints
        """
        if not rest:
            for x in range(len(self.joint_names)):
                if stiffness > 0:
                    self.cmd_dict[self.joint_names[x]] = {
                        "Stiffness": stiffness, 
                        "SetPoint": set_point
                    }
                else:
                    self.cmd_dict[self.joint_names[x]] = {
                        "Stiffness": 0, 
                        "SetPoint": 0
                    }  # relax condition
        else:
            for x in range(len(self.joint_names)):
                self.cmd_dict[self.joint_names[x]] = {
                    "Stiffness": 0, 
                    "SetPoint": 0
                }  # relax condition
            return False
        
        print(self.cmd_dict)
    
    def set_test_impedance_control(self):
        """
        Create impedance control command from current cmd_dict
        """

        
        self.new_impedance_control = command.ImpedanceControl()
        
        # Set values from cmd_dict
        self.new_impedance_control.Thumb.Stiffness = self.cmd_dict["Thumb"]["Stiffness"]
        self.new_impedance_control.Thumb.SetPoint = self.cmd_dict["Thumb"]["SetPoint"]
        self.new_impedance_control.Index.Stiffness = self.cmd_dict["Index"]["Stiffness"]
        self.new_impedance_control.Index.SetPoint = self.cmd_dict["Index"]["SetPoint"]
        self.new_impedance_control.Middle.Stiffness = self.cmd_dict["Middle"]["Stiffness"]
        self.new_impedance_control.Middle.SetPoint = self.cmd_dict["Middle"]["SetPoint"]
        self.new_impedance_control.Ring.Stiffness = self.cmd_dict["Ring"]["Stiffness"]
        self.new_impedance_control.Ring.SetPoint = self.cmd_dict["Ring"]["SetPoint"]
        self.new_impedance_control.Pinky.Stiffness = self.cmd_dict["Pinky"]["Stiffness"]
        self.new_impedance_control.Pinky.SetPoint = self.cmd_dict["Pinky"]["SetPoint"]
        self.new_impedance_control.has_index = True  # True = command cannot be ignored

        return self.new_impedance_control
    
 
    def command_worker_thread(self):
        """
        Thread function to run the command write worker
        """
        self.command_write_worker_i = src.command_write_worker(self.sock)
        command_thread = threading.Thread(
            target=self.command_write_worker_i.worker, 
            name="Thread_command_worker"
        )
        command_thread.start()
        threads.append(command_thread)
        print("Command write worker thread started")



    
    def test_worker(self, stiffness, set_point):
        """
        Test worker function to send impedance control commands
        
        :param command_write_worker: Command write worker instance
        :param stiffness: Stiffness value to set
        :param set_point: Set point value to set
        """
        print("inside test worker")
        self.dex_force(set_point, stiffness, False)  # Set to False to apply forces
        
        # self.set_test_impedance_control()
        self.command_write_worker_i.add_new_impedance_control(337785601,self.set_test_impedance_control())
        print("sleeping for 5 seconds to observe effect...")
        time.sleep(5)




    def stop(self):
        """
        Clean up and stop all threads
        """
        # Add any cleanup logic here
        if self.sock:
            self.sock.close()
            print("Socket connection closed")
        
        print("Stopped ImpedanceControlManager")

# Example usage
if __name__ == "__main__":
    impedance_manager = ImpedanceControlManager(host_ip="127.0.0.1", host_port=55555)
    
    try:
        # Run test with custom parameters
        impedance_manager.run_test(stiffness=0.7, set_point=0.4)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        impedance_manager.stop()