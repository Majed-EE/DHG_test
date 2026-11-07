from socket import *
import src
from sensor_msgs.msg import JointState
from proto_util import ctrl_command_pb2 as command
import time as T
import threading


class DHG_Bidirectional:
    def __init__(self, host_ip="127.0.0.1", host_port=5555):
        """
        Initialize the Haptic Glove Publisher class
        
        :param host_ip: IP address to connect to
        :param host_port: Port to connect to
        """
        # Direction Forward
        self.host_ip = host_ip
        self.host_port = host_port
        self.sock = None
        self.frame_read_worker_i = None
        self.dhg_connected = False
        # Uncomment if using ROS
        # self.pub = None
        # self.pub2 = None
        # self.Joint = None

        # for stiffness control
        self.command_write_worker_i = None
        self.new_impedance_control = None
        

        # direction Feedback
        self.cmd_dict = {}
        self.threads = []
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
    
 
    def set_command_write_worker(self):
        """
        Thread function to run the command write worker
        """
        self.command_write_worker_i = src.command_write_worker(self.sock)
        command_thread = threading.Thread(
            target=self.command_write_worker_i.worker, 
            name="Thread_command_worker"
        )
        command_thread.start()
        self.threads.append(command_thread)
        print("Command write worker thread started")

    def set_frame_read_worker(self,publish_flag=True):
            print("initialization of frame read worker")
            self.frame_read_worker_i = src.frame_read_worker(self.sock)
            print("frame read worker initialized")
            print("initialization of joint state publisher")
            self.Joint=JointState()
            self.Joint.name = ['thumb_rotate','thumb_split','thumb_bend', 'index_split','index_bend',
		    'middle_split','middle_bend', 'ring_split','ring_bend', 'last_split','last_bend']
            self.Joint.position = [0,0,0, 0,0, 0,0, 0,0, 0,0]
            print("joint state publisher initialized")
            

    
    def test_write_worker(self, stiffness, set_point):
        """
        Test worker function to send impedance control commands
        
        :param command_write_worker: Command write worker instance
        :param stiffness: Stiffness value to set
        :param set_point: Set point value to set
        """
        print("inside test worker")
        self.dex_force(set_point, stiffness, False)  # Set to False to apply forces
        self.command_write_worker_i.add_new_impedance_control(337785601,self.set_test_impedance_control())
        print("sleeping for 5 seconds to observe effect...")
        T.sleep(5)



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
        
    def connect(self):
        """
        Connect to the server
        """
        try:
            self.sock = socket.socket(AF_INET, SOCK_STREAM)
            print("Connecting to {0}:{1}".format(self.host_ip, self.host_port))
            self.sock.connect((self.host_ip, self.host_port))
            print("Connected successfully")
            self.dhg_connected = True
            return True
        except Exception as e:
            print("Connection failed: " + str(e))
            self.dhg_connected = False
            return False



    
    def publish_joint_state(self,publish_flag=True):
        """
        print("----------Publish joint state data------")
        """
        try:
           
            print("initialization of valset")
            valset=self.frame_read_worker_i.worker()
            print("valset initialized")
            # test_iter=0
            if publish_flag:
                # test_iter+=1
                print("Publishing joint state, iteration: {0}".format(test_iter))
                # if test_iter > 10:
                #     publish_flag = False
                #     break
                # for i in range(11):
                #     self.Joint.position[i]=valset[i]
                self.Joint.position = [valset[i] for i in range(11)]
                print("inside IMC 25 demo")
                print("thumb: {0}".format(valset[2]))
                print("index: {0}".format(valset[4]))
                print("middle: {0}".format(valset[6]))    
                print("ring: {0}".format(valset[8]))
                print("pinky: {0}".format(valset[10]))
                t=1
                print("sleeping for {} seconds".format(t))
                T.sleep(t)
                return [round(valset[2*i], 3) for i in range(1,6)]
            
        except Exception as e:
            print("Exception in publish_joint_state: " + str(e))
            self.stop()
            publish_flag = False


    def stop(self):
        """
        Clean up and close connections
        """
        if self.sock:
            self.sock.close()
            print("Socket connection closed")

# Example usage
# if __name__ == "__main__":
#     publisher = HapticGlovePublisher()
#     try:
#         publisher.run()
#     except KeyboardInterrupt:
#         print("Stopping publisher...")
#     finally:
#         publisher.stop()