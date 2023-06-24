# Winkly
Winkly is a tool to get the position of a sound source (in our case a snap) on a circle around 2 microphones.

## Backend
The backend (```server.py```) has to be started with python3 on a Raspberry Pi with connected I2S MEMS Microphone IM69D130 board. When started with flag ```-s``` the backend is sending the data to the first client that connects to it. 
To suppress the same output on the console of the Raspberry Pi you can use the flag ```--silent```.
The data that is sent is the angle of incidence in 1000 degrees, so to use it you have to divide by 1000.
This is automatically done by our frontend.


## Frontend
The frontend (```client.py```) has to be started on a PC with connected monitor. After you specify the IP address of the backend server a GUI will open with a visual representation of our data.