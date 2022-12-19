###############
#1st prototype for an eeg controlled robotic arm

import argparse
from socket import *
from pythonosc import dispatcher
from pythonosc import osc_server

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

blinkcount=0

def alpha_handler(unused_addr, args, value):
    """
    Handler for alpha absolute value.
    Can be One Average or Four Float values.
    If you set the OSC Stream Brainwaves to `All values`
    at Muse Monitor, you should change the param to:
    def alpha_handler(unused_addr, args, ch1, ch2, ch3, ch4):
    """
    print("alpha value: {}".format(value))


def beta_handler(unused_addr, args, value):
    print("beta value: {}".format(value))


def delta_handler(unused_addr, args, value):
    print("delta value: {}".format(value))


def theta_handler(unused_addr, args, value):
    print("theta value: {}".format(value))


def gamma_handler(unused_addr, args, value):
    print("gamma value: {}".format(value))


def mellow_handler(unused_addr, args, value):
    print("mellow value: {}".format(value))
    return

def concen_handler(unused_addr, args, value):
    print("concentration value: {}".format(value))
    return

def blink_handler(unused_addr, args, blink):
    global blinkcount
    if blink:
        blinkcount+= 1
        if(blinkcount>7):
            print("blink 5 times")
            tcpClicSock.send(('left').encode())
            blinkcount=0

def jaw_clench_handler(unused_addr, args, jaw):
    if jaw:
        print("Jaw_Clench")
        tcpClicSock.send(('right').encode())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
                        default="0.0.0.0",
                        help="The ip to listen on")
    parser.add_argument("--port",
                        type=int,
                        default=5000,
                        help="The port to listen on")
    args = parser.parse_args()

    dispatcher = dispatcher.Dispatcher()
    #dispatcher.map("/muse/elements/alpha_absolute", alpha_handler, "EEG")
    #dispatcher.map("/muse/elements/beta_absolute", beta_handler, "EEG")
    #dispatcher.map("/muse/elements/delta_absolute", delta_handler, "EEG")
    #dispatcher.map("/muse/elements/theta_absolute", theta_handler, "EEG")
    #dispatcher.map("/muse/elements/gamma_absolute", gamma_handler, "EEG")
    dispatcher.map("/muse/elements/blink", blink_handler, "EEG")
    dispatcher.map("/muse/elements/jaw_clench", jaw_clench_handler, "EEG")
    dispatcher.map("/muse/algorithm/concentration", concen_handler, "EEG")

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    server.serve_forever()
