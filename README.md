# EEG-Controlled-Robotic Arm
1st prototype for controlling a robotic arm with brain signals

In this project, we want to use the MUSE 2, an Electroencephalography (EEG) sensing headband device to develop a proof of concept for a mind-controlled robot.

First, we collect Raw EEG data from the Muse 2 sensor using a 3rd party app the Mind control APP. It is available on both Google Play and the APP store for around 15$. The app permits us to stream data to a laptop via UDP. Note that the sensor has 4 electrodes, and each send 5 frequency components (alpha, beta, gamma, delta, sigma) for a total of 20 input features.<br/>

We train and save a tensorflow model and then we perform real time classification of the signal. We send the results to the raspberry pi-controlled arm via TCP (right or left). The arm contains a driver board that comes up with a software library that permits to easily control the 4 servo motor.<br/>

sample code:<br/>

Collect EEG-data.py : Collect and labels data from the Muse 2 sensor using the Mindcontroll app<br/>
Gui-tcpPC.py : GUI control of the Rasp-arm via TCP, to run on laptop to test TCP connection<br/>
Rasp-Arm-tcpPI.py : TCP server listener running on Rasp-Arm<br/>
Muse-Robot-Control.py : Control Rasp-arm with Muse 2 sensor (jaw clenches and eyes blinking)<br/>
Test Classifier Model.py : runs realtime prediction on data captured from Muse 2 and sends moving signals to the robotic arm according to the result<br/>


**A Brain-Computer Interface (BCI) system that enables users to control a 4-DOF robotic arm using real-time brainwave signals.**

This project demonstrates an end-to-end pipeline: capturing raw EEG data from a **Muse 2 headband**, processing signals with **Machine Learning (TensorFlow)** on a PC, and transmitting control commands via TCP to a **Raspberry Pi** driven robotic arm.

---

## ⚙️ System Architecture

The system operates on a distributed network architecture involving three main nodes: the Sensor, the Processing Unit (PC), and the Actuator (Robot).

```mermaid
graph LR
    A[Muse 2 Headband] -- UDP Stream --> B[Laptop / PC]
    B -- TCP Socket --> C[Raspberry Pi]
    C -- PWM Signals --> D[Robotic Arm Servos]
    
    subgraph "Signal Processing (PC)"
    B1[Data Collection] --> B2[Feature Extraction]
    B2 --> B3[TensorFlow Model]
    B3 --> B4[Command Generation]
    end


