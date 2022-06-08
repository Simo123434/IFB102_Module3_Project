# QUT IFB102 Module3 Project

## Created by Dylan Wondal 2022

### IOT Tempreature Sensor using LM35 Sensor and SMTP

This is the project for the Module 3 mini project of the QUT unit IFB102

It is a LM35 tempreature sensor connected to an arduino uno which is then plugged into a raspberry pi.

The source code is QUT.py which just need to be run on the RPI
The LM35 sensor cannot be connected straight to the RPI as it does not have a analog to digital converter so the arduino was used as a middleman

### Features

1. Records Temperature every 1 minute and write to the file within temps folder
2. Once it reaches the time set by the user (default 11:59PM), it will send an email from the sender_account to the receiver_account with the max and min temp recorded as well as a graph for that day. The graph uses the avearge temp from every 30 minutes from the temp file.

### How to run

```python
pip install -r requirements.txt
```

Change all neccessary values in QUT.py outlined within the comments

```python
python3 QUT.py
```
