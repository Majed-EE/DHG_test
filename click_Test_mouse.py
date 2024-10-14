### works but does not close

from datetime import datetime
from pynput.mouse import Listener
import sys
global click_current
click_times=10
click_current=0
def on_click(x, y, button, pressed):
    global click_current
    try:
        if pressed:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            click_current=click_current+1
            print("hi")
            print(f"Current click {click_current} Mouse clicked at ({x}, {y}) at: {timestamp}")
    except KeyboardInterrupt:
            print("\nExiting program.")
            sys.exit()
            
        

def main():
    global click_current
    print("Click anywhere on the screen to timestamp. Press 'q' to quit.")
    with Listener(on_click=on_click) as listener:
    # try:q
        
        
        # else:
        listener.join()
if __name__ == "__main__":
    main()