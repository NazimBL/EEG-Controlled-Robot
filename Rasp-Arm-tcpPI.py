import Adafruit_PCA9685	# Import the library used to communicate with PCA9685
import time

pwm = Adafruit_PCA9685.PCA9685()	# Instantiate the object used to control the PWM
pwm.set_pwm_freq(50)	# Set the frequency of the PWM signal

'''
Import the socket library used for TCP communication
'''
import socket
'''
Import multi-threaded libraries
'''
import threading


#Define the flag
fun_flag = 0
"""
Define a multithreaded class
"""
class Functions(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(Functions, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()
        self.__flag.clear()

        
        

    def pause(self):
        global thread_flag
        thread_flag = 0
        self.__flag.clear()
        

    

    def resume(self):
        global thread_flag,fun_flag
        #thread_flag = 0
        #print("**********")
        self.__flag.set()


    def run(self):
        global fun_flag
        while 1:
            global fun_flag
            self.__flag.wait()
            #move servo A left or right depending on flag
            if fun_flag:
                    pwm.set_pwm(12, 0, 0)
                    time.sleep(0.5)
            else:
                    pwm.set_pwm(12, 0, 700)
                    time.sleep(0.5)
        
threadX = Functions()
threadX.start()

'''
Next is the configuration related to TCP communication, where PORT is the defined port number, you can freely choose from 0-65535, it is recommended to choose the number after 1023, 
which needs to be consistent with the port number defined by the client in the PC
'''
HOST = ''
PORT = 10223
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

'''
Start to monitor the client connection, after the client connection is successful, start to receive the information sent from the client
'''
tcpCliSock, addr = tcpSerSock.accept()

while True:
    data = ''
    
    '''
    Receive information from the client
    '''
    '''
    If the information content is on, control the steering gear to rotate
    If the information content is off, control the servo to stop rotating
    '''
    data = str(tcpCliSock.recv(BUFSIZ).decode())
    if not data:
        continue

    elif 'right' == data:
        fun_flag = 1
        threadX.resume()
        
            
    elif 'left' == data:
        fun_flag = 0
        time.sleep(1)
        threadX.pause()
    
    '''
  Finally print out the received data, and start to monitor the next message sent by the client
    '''
    print(data)