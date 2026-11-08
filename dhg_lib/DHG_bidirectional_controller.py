from socket import *
# from dhg source code
import src
from sensor_msgs.msg import JointState 
from proto_util import ctrl_command_pb2 as command

import time as T
import threading


class DHG_Bidirectional:
    def __init__(self, host_ip="127.0.0.1", host_port=55555):
        """
        Initialize the Haptic Glove Publisher class
        
        :param host_ip: IP address to connect to
        :param host_port: Port to connect to
        """
        # Direction Forward
        self.host_ip = host_ip
        self.host_port = host_port
        self.sock = None
        self.L2R_enabled = False
        self.R2L_enabled = False
        

        self.frame_read_worker_i=None
        self.valset = None
        self.dhg_connected = False
        # Uncomment if using ROS
        # self.pub = None
        # self.pub2 = None
        self.Joint = None

        # for stiffness control
        self.command_write_worker_i = None
        self.new_impedance_control = None
        

        # direction Feedback
        self.command_read_worker_i = None
        self.cmd_dict = {}
        self.threads = []
        self.joint_names = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
        

        print("default cmd dict: ")
        
        # Initialize cmd_dict
        self.dex_force(0, 0, True)



    def dex_force(self, set_point, stiffness, rest=True):
        """
        set force parameters for all joints
        TODO: set_point and stiffness should be a list of 5 values for each joint 
        :param set_point: Set point value for joints - [0, 1] | 0 open (0 radian), 1 closed (1.57 radian) 
        :param stiffness: Stiffness value for joints - [0, 1] | 0 soft, 1 hard
        :param rest: If True, relax all joints
        """
        if not rest:
            
            if len(set_point) != 5 or len(stiffness) != 5:
                raise ValueError("set_point and stiffness must be lists of 5 values each.")
            for x in range(len(self.joint_names)):
                if stiffness[x] > 0:
                    self.cmd_dict[self.joint_names[x]] = {
                        "Stiffness": stiffness[x], 
                        "SetPoint": set_point[x]
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
    
    def _set_test_impedance_control(self):
        """
        Create impedance control command from current cmd_dict
        """

        print("Setting test impedance control with cmd_dict: {0}".format(self.cmd_dict))
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
    
 
    def _set_command_write_worker(self):
        """
        Thread function to run the command write worker
        """
        self.command_write_worker_i = src.command_write_worker(self.sock)
        command_thread = threading.Thread(
            target=self.command_write_worker_i.worker, 
            name="Thread_command_worker"
        )
        command_thread.start()
        self.R2L_enabled = True
        self.threads.append(command_thread)
        print("Command write worker thread started")



    
    def test_write_worker(self, stiffness, set_point):
        """
        Test worker function to send impedance control commands
        
        :param command_write_worker: Command write worker instance
        :param stiffness: Stiffness value to set
        :param set_point: Set point value to set
        """
        if self.command_write_worker_i is None:

            print("Command write worker is initializating...")
            try:
                self._set_command_write_worker()
                T.sleep(1)  # Sleep for 1 second to ensure the worker is ready
                print("Command write worker initialized successfully.")
                self.R2L_enabled = True
            except Exception as e:
                print("Failed to initialize command write worker: {e}".format(e=e))
                return None
        if self.R2L_enabled:
            print("inside test worker")
            self.dex_force(set_point, stiffness, False)  # Set to False to apply forces
            print("sleeping for 1 seconds to observe effect...")
            T.sleep(1)
            self.command_write_worker_i.add_new_impedance_control(337785601,self._set_test_impedance_control())
            



    def initialize_ros_publisher(self):
        #TODO
        """
        Initialize ROS publishers (commented out for now)
        Uncomment if using ROS
        """
        # rospy.init_node('haptic_glove', anonymous=True)
        # self.pub = rospy.Publisher('glove_out', JointState, queue_size=10)
        # self.pub2 = rospy.Publisher('glove_out_sim', JointState, queue_size=10)
        # self.Joint = JointState()    
        # self.Joint.name = ['thumb_rotate','thumb_split','thumb_bend',
        #     'index_split','index_bend',
        #     'middle_split','middle_bend',
        #     'ring_split','ring_bend',    
        #     'last_split','last_bend']
        # self.Joint.position = [0,0,0,
        #         0,0,
        #         0,0,
        #         0,0,
        #         0,0]
        pass
        

    
    def publish_joint_state(self,verbose=True,sleep_time=1):
        """
        print("----------Publish joint state data------")
        """
        try:
            if verbose:
                print("----------Publish joint state data------")

            print("Initialization of valset")
            if self.frame_read_worker_i is None:
                print("frame_read_worker_i is None, initializing...")
                try:
                    self.frame_read_worker_i = src.frame_read_worker(self.sock)
                    self.valset = self.frame_read_worker_i.worker()
                    print("frameread_worker initialized successfully")
                    self.R2L_enabled = True
                except Exception as e:
                    print("Failed to initialize frame_read_worker: {e}".format(e=e))
                    self.R2L_enabled = False
                    return None
                self.R2L_enabled = True

            if self.R2L_enabled:
                self.valset = self.frame_read_worker_i.worker()
                self.Joint.position = [self.valset[i] for i in range(11)]
                print("thumb: {0}".format(self.valset[2]))
                print("index: {0}".format(self.valset[4]))
                print("middle: {0}".format(self.valset[6]))    
                print("ring: {0}".format(self.valset[8]))
                print("pinky: {0}".format(self.valset[10]))
                
                print("sleeping for {} seconds".format(sleep_time))
                T.sleep(sleep_time)
                return [round(self.valset[2*i], 3) for i in range(1,6)]
            else:
                print("R2L is not enabled. Cannot publish joint state data.")
                return None
            
        except Exception as e:
            print("Exception in publish_joint_state: " + str(e))
            self.R2L_enabled = False
            self.stop()
            




    def connect(self):
        """
        Connect to the server
        """
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            print("Connecting to {0}:{1}".format(self.host_ip, self.host_port))
            self.sock.connect((self.host_ip, self.host_port))
            print("Connected successfully")
            self.dhg_connected = True
            self.frame_read_worker_i=src.frame_read_worker(self.sock)
            self.R2L_enabled = True
            self.Joint = JointState()
            self.Joint.name = ['thumb_rotate','thumb_split','thumb_bend',
            'index_split','index_bend',
            'middle_split','middle_bend',
            'ring_split','ring_bend',	
            'last_split','last_bend']
            # self.Joint.name = ['thumb_rotate','thumb_split','thumb_bend',
            return True
        except Exception as e:
            print("Connection failed: " + str(e))
            self.dhg_connected = False
            return False














    def stop(self):
        """
        Clean up and close connections
        """
        if self.sock:
            self.sock.close()
            print("Socket connection closed")
            self.dhg_connected = False

# Example usage
# if __name__ == "__main__":
#     publisher = HapticGlovePublisher()
#     try:
#         publisher.run()
#     except KeyboardInterrupt:
#         print("Stopping publisher...")
#     finally:
#         publisher.stop()