from socket import *
import src
from sensor_msgs.msg import JointState
import time as T
# import rospy
# from sensor_msgs.msg import JointState

class DHG_Publisher:
    def __init__(self, host_ip="127.0.0.1", host_port=5555):
        """
        Initialize the Haptic Glove Publisher class
        
        :param host_ip: IP address to connect to
        :param host_port: Port to connect to
        """
        self.host_ip = host_ip
        self.host_port = host_port
        self.sock = None
        self.frame_read_worker_i = None
        # Uncomment if using ROS
        # self.pub = None
        # self.pub2 = None
        # self.Joint = None
        
    def initialize_ros_publisher(self):
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
            print("initialization of framere read worker")
            self.frame_read_worker_i = src.frame_read_worker(self.sock)
            print("frame read worker initialized")
            print("initialization of joint state publisher")
            self.Joint=JointState()
            self.Joint.name = ['thumb_rotate','thumb_split','thumb_bend', 'index_split','index_bend',
		    'middle_split','middle_bend', 'ring_split','ring_bend', 'last_split','last_bend']
            self.Joint.position = [0,0,0, 0,0, 0,0, 0,0, 0,0]
            print("joint state publisher initialized")
            
            # Initialize frame read worker if available
            # self.frame_read_worker_i = src.frame_read_worker(self.sock)
            
            return True
        except Exception as e:
            print("Connection failed: " + str(e))
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