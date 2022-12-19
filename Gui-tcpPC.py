'''
Import the socket library used for TCP communication
'''
from socket import *
'''
Python uses Tkinter to quickly create GUI applications and instantiate them while importing
'''
import tkinter as tk

def move_right():
    '''
    Call this method to send the command'right' to control the rotation of the servo
    '''
    tcpClicSock.send(('right').encode())

def move_left():
    '''
    Call this method to send the command'left' to control the rotation of the servo
    '''
    tcpClicSock.send(('left').encode())

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

btn_right = tk.Button(root, width=8, text='Right', fg='#E1F5FE', bg='#0277BD', command=move_right)
btn_right.place(x=15, y=15)


btn_left = tk.Button(root, width=8, text='Left', fg='#E1F5FE', bg='#0277BD', command=move_left)
btn_off.place(x=95, y=15)

root.mainloop()
