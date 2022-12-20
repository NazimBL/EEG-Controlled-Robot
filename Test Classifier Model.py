# this part of code is used to test the machine learning model
# it is created and modifiid by Yibo Li & Nazim Belabbaci

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer
import numpy as np
import tensorflow as tf
from nltk import flatten

from socket import *

# *********************  we define the parameters here for all function to use  *********************
alpha_freq = [-1,-1,-1,-1]
beta_freq = [-1,-1,-1,-1]
delta_freq = [-1,-1,-1,-1]
theta_freq = [-1,-1,-1,-1]
gamma_freq = [-1,-1,-1,-1]

all_freq = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
samples_collection = []

sample_num = 0
exp_samples = 60
threshold = 0.6                                     # default in Edge Impulse is 0.6

IP = "0.0.0.0"
PORT = 5000

#rasp address
SERVER_IP = '192.168.5.174'

'''
Next is the configuration related to TCP communication, where PORT is the defined port number, 
you can freely choose from 0-65535, it is recommended to choose the number after 1023, 
which needs to be consistent with the port number defined by the server in the Raspberry Pi
'''
SERVER_PORT = 10223
BUFSIZ = 1024
ADDR = (SERVER_IP, SERVER_PORT)
tcpClicSock = socket(AF_INET, SOCK_STREAM)
tcpClicSock.connect(ADDR)

# *********** Initiates TensorFlow Lite ***********
def initiate_tf():
    global classifier, input_details, output_details
    path = "Models/ei-lslsls0001_3-nn_3-classifier-tensorflow-lite-float32-model.lite"

    # Load TFLite model and allocate tensors.
    classifier = tf.lite.Interpreter(model_path = path, experimental_preserve_all_tensors=True)

    # Get input and output tensors.
    input_details = classifier.get_input_details()
    output_details = classifier.get_output_details()

    # Allocate tensors
    classifier.allocate_tensors()

    # Printing input and output details for debug purposes in case anything is not working
    print(input_details)
    print(output_details)

# handle alpha frequency channel
def alpha_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq

    if (len(args) == 5):
        all_freq[0] = args[1]
        all_freq[1] = args[2]
        all_freq[2] = args[3]
        all_freq[3] = args[4]

# handle beta frequency channel
def beta_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq

    if (len(args) == 5):
        all_freq[4] = args[1]
        all_freq[5] = args[2]
        all_freq[6] = args[3]
        all_freq[7] = args[4]

# handle delta frequency channel
def delta_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq

    if (len(args) == 5):
        all_freq[8] = args[1]
        all_freq[9] = args[2]
        all_freq[10] = args[3]
        all_freq[11] = args[4]

# handle theta frequency channel
def theta_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq

    if (len(args) == 5):
        all_freq[12] = args[1]
        all_freq[13] = args[2]
        all_freq[14] = args[3]
        all_freq[15] = args[4]

# handle gamma frequency channel
def gamma_handler(address: str,*args):
    global alpha_freq, beta_freq, delta_freq, theta_freq, gamma_freq
    global sample_num, exp_samples, samples_collection

    if (len(args) == 5):
        all_freq[16] = args[1]
        all_freq[17] = args[2]
        all_freq[18] = args[3]
        all_freq[19] = args[4]

        samples_collection.append(all_freq)
        sample_num = sample_num + 1
        
        if sample_num == exp_samples:               # Collected all samples...
            print("*" * 50)
            for all_sample in samples_collection:
                print(all_sample)

            samples_collection = flatten(samples_collection)
            prediction()
            sample_num = 0
            samples_collection.clear()
            samples_collection = []

# ******** prediction ********
def prediction():
    global choice

    input_samples = np.array(samples_collection, dtype=np.float32)
    input_samples = np.expand_dims(input_samples, axis=0)

    input_index = input_details[0]['index']
    output_index = output_details[0]['index']

    classifier.set_tensor(input_index, input_samples)
    classifier.invoke()

    output_data = classifier.get_tensor(output_index)
    activtiy_1 = output_data[0][0]
    activtiy_2 = output_data[0][1]
    print(activtiy_1)
    print(activtiy_2)

    # checking if over confidence threshold
    if activtiy_1 >= threshold:
        choice = "activtiy_1"
        tcpClicSock.send(('right').encode())
        # Please do something here, e.g., tcp or other action
    elif activtiy_2 >= threshold:
        choice = "activtiy_2"
        tcpClicSock.send(('left').encode())
        # Please do something here, e.g., tcp or other action
    else:
        choice = "no action"
        # Please do something here, e.g., tcp or other action

    print(f"Activtiy_1:{activtiy_1:.4f} - Activtiy_2:{activtiy_2:.4f}     {choice}    ")


# ====================== For Muse Communication ==========================
def get_dispatcher():
    dispatcher = Dispatcher()
    dispatcher.map("/muse/elements/delta_absolute", delta_handler,0)
    dispatcher.map("/muse/elements/theta_absolute", theta_handler,1)
    dispatcher.map("/muse/elements/alpha_absolute", alpha_handler,2)
    dispatcher.map("/muse/elements/beta_absolute" , beta_handler,3)
    dispatcher.map("/muse/elements/gamma_absolute", gamma_handler,4)
    return dispatcher

def start_blocking_server(ip, port):
    server = BlockingOSCUDPServer((ip, port), dispatcher)
    server.serve_forever()

def dispatch():
    global dispatcher
    dispatcher = get_dispatcher()
    start_blocking_server(IP, PORT)

if __name__ == "__main__":
    prediction()
    dispatch()
