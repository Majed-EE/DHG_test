from DHG_bidirectional_controller import DHG_Bidirectional


def main():
    # Create an instance of the DHG_Bidirectional class
    dhg = DHG_Bidirectional()
    sleep_time = 1  # Sleep time in seconds between iterations
    dhg.connect()
    # connect glove to the server
    try:
        if dhg.connect():
            print("Connected to the server successfully.")
            print("Publishing joint state data for 5 iterations with a sleep time of 1 second between each iteration.")
            for i in range(5):
                L2R_val = dhg.publish_joint_state(verbose=True, sleep_time=1)
                print("Iteration {i}: L2R_val = {L2R_val}".format(i=(i+1), L2R_val=L2R_val))
            print("Finished publishing joint state data. Stop the program.")
            dhg.stop()

        else:
            print("Failed to connect to the server.")
    except Exception as e:
        print("An error occurred: {e}".format(e=e))





if __name__ == "__main__":
    main()