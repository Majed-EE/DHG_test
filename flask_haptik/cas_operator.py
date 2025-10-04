# Example: Generate a random numpy array of shape (3, 2)
random_array = np.random.rand(3, 2)
print(f"Random numpy array of shape (3, 2):\n{random_array}")
from flask import Flask, request, render_template, jsonify
import time
import numpy as np



################################################### CAS database ############################################################
global operator_ctrl_array, haptic_feedback_array, dhg_data_array

ref_time=time.time()

# RIS_summary={"RIS_ISAC_mem":[[0,0]], "RIS_GRC_mem":[[0,0]],"RIS_obj_mem":[[0,0]]} # each array contain [flag,time of change]


app = Flask(__name__)





#################################### Request sender to UE ##################################



get_route= lambda ip,port: "http://"+str(ip)+":"+str(port)

CAS_url,CAS_port= "10.50.49.23",5000

CAS_end_point= get_route(ip=CAS_url,port=CAS_port)


# ######################### API continiously store value from glove #####################

# test 1: connect glove to CAS
def dummy_dhg():
    return np.asarray


################################# Request sender to GRC 1 #######################################



@app.route('/')
def index():
    """Main page that displays the last value and allows input"""
    print("main page debug")
    return render_template('index.html', last_value=None)


################################################### ISAC to CAS (red line) ####################33
@app.route('/api/CAS_handler', methods=['GET'])
def print_value():
    """GET endpoint that prints the value from query parameters"""
    global operator_ctrl_array, haptic_feedback_array
    print("UE -> CAS haptic feedback")
    # print(f"previous rs: {current_rs}")
    # Get value from query parameter
    haptic_fb = request.args.get('haptic_feedback') # api  ISAC->CAS -> value contains what True
    # trigger value
    # updating currnt_rs
    print(f"type(haptic_fb): {type(haptic_fb)}")
    if haptic_fb is not None:
        print(f"📨 Received GET value UE-CAS, haptic_feedback-> {haptic_fb}")
        # haptic_fb=haptic_fb_data["haptic_feedback"]
        current_time=time.time()-ref_time
        ctrl_operator= round(np.random.rand(),2) # Generate a random value between 0 and 1

        print(f"Sending control CAS->UE: {ctrl_operator}")

        return jsonify({
            "status": "success",
            "control_value": ctrl_operator
        })

        
    else:
        return jsonify({
            "status": "error",
            "message": "No value provided. Use ?value=your_value"
        }), 400
    



if __name__ == '__main__':
    print(" Starting Flask server...")
    print(" Available endpoints:")
    print("   - GET /                 (Web interface)")
    print("   - GET  /api/CAS_handler  (ISAC object detection)")
    print(f"\n Server running at {CAS_end_point}")

    app.run(debug=True, host='0.0.0.0', port=5000)