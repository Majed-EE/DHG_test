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
                print("Iteration {i+1}: L2R_val = {L2R_val}".format(i=i, L2R_val=L2R_val))
            print("Finished publishing joint state data. Stop the program.")

            print("R2L haptic feedback")
            stiffness_range = [x for x in range(0, 1, 0.1)]  # Stiffness values from 0 to 1
            for stiffness in stiffness_range:
                try:
                    dhg.test_worker(stiffness=stiffness, set_point=0.5)  # Example values for stiffness and set_point
                except Exception as e:
                    print("An error occurred while testing stiffness {stiffness}: {e}".format(stiffness=stiffness, e=e))
    except Exception as e:
        print("An error occurred: {e}".format(e=e))


    

if __name__ == "__main__":
    main()