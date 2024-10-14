# works perfectly for keybord input but i guess some problem in case of running it on ubuntu 16
import keyboard
from datetime import datetime
import time
def main():
    print("Press any key to timestamp. Press 'q' to quit.")
    while True:
        key = keyboard.read_event(suppress = True)
        if key.event_type=="up":
                
            print(key)
            if key.name == 'q':  # Exit if 'q' is pressed
                break
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print("Key pressed at:", timestamp)
        else:
            continue

if __name__ == "__main__":
    main()