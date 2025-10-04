import requests
import time
import numpy as np
Default_RS=0
current_rs=Default_RS
check=True
get_route= lambda ip,port: "http://"+str(ip)+":"+str(port)
CAS_url,CAS_port= "10.50.49.23",5000
CAS_end_point= get_route(ip=CAS_url,port=CAS_port)


def send_value(value):
    """Send a value to the Flask server"""
    try:
        # API CAS->UE
        print(f"Trig send value CAS-> CAS \nRaw data: {value}")
        response = requests.get(f"{CAS_end_point}/api/CAS_handler", params={"haptic_feedback": value}) # value -=[bool check_flag,bool ctrl_flag]

        if response.status_code == 200:
            data = response.json() # API GRC->CAS
            print(f"Response from UE->CAS {data}")
            print(f"✅ Success! haptic feedback: {data['control_value']}") # 2 - gives value of the corrected RIS
            return data
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        return None


def send_UE_trig():
    """Quickly send a value without interactive menu"""
    global haptic_feedback
    # print(f"checking for value change, Current Object status {current_rs}")
    # value = current_rs
    haptic_feedback= np.random.rand()# Generate a random value between 0 and 1

    print(f"UE generated haptic_feedback (Haptic feedback) value to CAS: {haptic_feedback}")
    control_cas_data=send_value(haptic_feedback) # check_Flag,ctrl_flag
    print(f"raw data: {control_cas_data}")
    print(f"updating > stiffness")
    control_UE=control_cas_data["ontrol_value"] # updated current_rs

if __name__ == "__main__":
    # Install requests if not already installed
    for x in range(5):
        send_UE_trig()
        print("-----sleeping for 2 sec-----")
        time.sleep(2)
 