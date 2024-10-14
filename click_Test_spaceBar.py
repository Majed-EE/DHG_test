
# wors perfectly for spacebar 
from datetime import datetime


def main():
    print("Press 'Enter' to record a timestamp. Press 'q' to quit.")
    while True:
        user_input = input()
        if user_input == 'q':
            break
        elif user_input == '':
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            print("Timestamp recorded at:", timestamp)

if __name__ == "__main__":
    main()