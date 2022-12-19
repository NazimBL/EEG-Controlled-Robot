# EEG-Controlled-Robot
1st prototype for controlling a robotic arm with brain signals

In this project, we want to use the MUSE 2, an Electroencephalography (EEG) sensing headband device to develop a proof of concept for a mind-controlled robot.

First, we collect Raw EEG data from the Muse 2 sensor using a 3rd party app the Mind control APP. It is available on both Google Play and the APP store for around 15$. The app permits us to stream data to a laptop via UDP. Note that the sensor has 4 electrodes, and each send 5 frequency components (alpha, beta, gamma, delta, sigma) for a total of 20 input features.

We train and save a tensorflow model and then we perform real time classification of the signal and send the results to the raspberry pi-controlled arm via TCP (1 right and 0 for left). The arm contains a driver board that comes up with a software library that permits to easily control the 4 servo motor.

##########
sample code:
Collect EEG-data.py : Collect and labels data from the Muse 2 sensor using the Mindcontroll app
Gui-tcpPC.py : GUI control of the Rasp-arm via TCP, to run on laptop to test TCP connection
Rasp-Arm-tcpPI.py : TCP server listener running on Rasp-Arm
Muse-Robot-Control.py : Control Rasp-arm with Muse 2 sensor (jaw clenches and eyes blinking)



