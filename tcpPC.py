'''
Import the socket library used for TCP communication
'''
from socket import *

'''
Python uses Tkinter to quickly create GUI applications and instantiate them while importing
'''
import tkinter as tk

def lights_on():
    '''
    Call this method to send the command'on' to control the rotation of the servo
    '''
    tcpClicSock.send(('on').encode())

def lights_off():
    '''
    Call this method to send the command'off' to control the rotation of the servo
    '''
    tcpClicSock.send(('off').encode())

'''
Enter the IP address of the Raspberry Pi here
'''
SERVER_IP = '192.168.111.174'	

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

'''
The following is part of the GUI
'''
root = tk.Tk()	# Define a window
root.title('Lights')	# The title of the window
root.geometry('175x55')	# The size of the window, the middle x is the English letter x
root.config(bg='#000000')	# Define the background color of the window

'''
Use Tkinter's Button method to define a button, the button is on the root window, the name on the button is'ON', the text color of the button is #E1F5FE, 
and the background color of the button is #0277BD. When the button is pressed, calls lights_on( )function
'''
btn_on = tk.Button(root, width=8, text='ON', fg='#E1F5FE', bg='#0277BD', command=lights_on)

'''
Choose a location to place this button
'''
btn_on.place(x=15, y=15)

'''
Define another button in the same way. The difference is that the text on the button is changed to'OFF'. 
When the button is pressed, the lights_off() function is called
'''
btn_off = tk.Button(root, width=8, text='OFF', fg='#E1F5FE', bg='#0277BD', command=lights_off)

btn_off.place(x=95, y=15)

'''
Finally open the message loop
'''
root.mainloop()