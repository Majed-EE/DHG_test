from DHG_bidirectional_controller import DHG_Bidirectional
import time as T

def main():
    # Create an instance of the DHG_Bidirectional class
    dhg = DHG_Bidirectional()
    T.sleep(1)  # Sleep for 1 second before attempting to connect
    # connect glove to the server
    try:
        if dhg.connect():
            print("Connected to the server successfully.")
            print("Publishing joint state data for 5 iterations with a sleep time of 1 second between each iteration.")
            for i in range(5):
                L2R_val = dhg.publish_joint_state(verbose=True, sleep_time=1)
                print("Iteration {i}: L2R_val = {L2R_val}".format(i=i, L2R_val=L2R_val))
            print("Finished publishing joint state data. Stop the program.")

            print("R2L haptic feedback")
            stiffness_range = [x/10 for x in range(0, 10)]  # Stiffness values from 0 to 1
            for stiffness in stiffness_range:
                try:
                    stiffness=5*[stiffness] 
                    set_point=5*[0.2]	
                    print("setpoint: {set_point}/nstiffness: {stiffness}".format(set_point=set_point,stiffness=stiffness))
                    dhg.test_write_worker(stiffness=stiffness, set_point=set_point)  # Example values for stiffness and set_point
                except Exception as e:
                    dhg.stop()  # Ensure the worker is stopped in case of an error
                    print("An error occurred while testing stiffness {stiffness}: {e}".format(stiffness=stiffness, e=e))
    except Exception as e:
        dhg.stop()  # Ensure the worker is stopped in case of an error
        print("An error occurred: {e}".format(e=e))


    

if __name__ == "__main__":
    main()