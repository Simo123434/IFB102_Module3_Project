# QUT IFB102 Module3 Project 

## Created by Dylan Wondal 2022

### IOT Tempreature Sensor using LM35 Sensor and SMTP

This is the project for the Module 3 mini project of the QUT unit IFB102

It is a LM35 tempreature sensor connected to an arduino uno which is then plugged into a raspberry pi.

The source code is QUT.py which just need to be run on the RPI
The LM35 sensor cannot be connected straight to the RPI as it does not have a analog to digital converter so the arduino was used as a middleman

### How to run
```
pip install -r requirements.txt
```
Change all neccessary values in QUT.py outlined within the comments
```
python3 QUT.py
```
