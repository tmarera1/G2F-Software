# G2F-Software
G2F Software

Save the file in one folder on your PC. 
Connect device to PC: 

Connect NRF dev board/dongle to your PC and note down the "COM" port that it is connected to. Update that "COM" port number on line 15 of main.py. 
Update the directory location of the graphic.png on line 44 of the rough.py file. Make sure the device is turn on and the bluetooth is advertizing (LED is blinking). 
Open the terminal and navigate to the folder you saved the software files. Run "python kickstart.py" to start the program.The PC will look for the device advertizing, connect to it
and the force and cap sense data should start streaming to the screen whilst a duplicate of the data is saved into a .csv file for later processing. 
