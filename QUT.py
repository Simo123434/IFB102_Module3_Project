'''
QUT Module 3 Mini project
IOT Temperature Sensor with smtp
Created by Dylan Wondal
'''

# Imports
import pyfirmata
import time
import smtplib
import matplotlib.pyplot as plt
from datetime import date
import numpy as np
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders



def main(): # define main function
    # Defining variables for smtp

    sender_account = 'dylanwondalqut@outlook.com' # Email address used to send emails
    sender_pwd = 'Module3PWD!' # password for the account
    receiver_account = 'djsimpson22@outlook.com.au' # Email address used to receive emails
    server = 'smtp.office365.com' # smtp server to be uses
    port = 587 # port used to connect to the smtp server

    # Defining date variables
    today = date.today() # Today's date
    today_date = today.strftime("%B %d, %Y") # today's date in a string format


    # Defining the board for arduino
    board = pyfirmata.Arduino('/dev/ttyACM0') # Change '/dev/ttyACM0' to the port of your arduino
    
    # Starting the board and sensor
    it = pyfirmata.util.Iterator(board)
    it.start()
    time.sleep(5) # wait for the board to start up
    analog_input = board.get_pin('a:1:i') # read the analog pin of temp sensor
    
    if analog_input is None: # Check if sensor not outputting data
        print("An Error Occured, please check sensor") # print error and close file
        quit()
    else:
        while True:
            if str(time.strftime("%H:%M")) == "23:59": # Check if the time is 11:59 pm
                temps = []
                times = []
                average_temps = []
                
                with open("temps/" + str(today_date) + ".txt", "r") as h:
                    averagedata = h.readlines()
                # get the average temp from every 30 minutes and append to list in time, temp format
                    for i in range(0, len(averagedata), 30): 
                        average_temps.append(averagedata[i].split()[0] + ", " + averagedata[i].split()[1]) 
                h.close()
                with open("Av_temps/" + str(today_date) + ".txt", "a") as k:
                    for i in range(len(average_temps)):
                        k.write(average_temps[i].replace(',','') + "\n")
                k.close()
                with open("Av_temps/" + str(today_date) + ".txt", "r") as g: # Read temp data from that day 
                    data = g.readlines()
                    for line in data:
                        times.append(line.split()[0].replace(",","")) # append the time to the list
                        temps.append(line.split()[1]) # append the temp to the list
                g.close()


                plt.figure(figsize=(20, 20))
                plt.plot(times, temps) # plot the data
                plt.xlabel('Time (hh:mm)')
                plt.ylabel('Temperature (C)')
                plt.gca().invert_yaxis()
                #Change font size of the plot lines
                plt.setp(plt.gca().get_xticklabels(), fontsize=12)
                plt.setp(plt.gca().get_yticklabels(), fontsize=12)
                plt.title('Temperature Data for ' + str(today_date))
                # plt.show()
                plt.savefig('image/' + str(today_date) + ".png")
                    
            # wait 1 second to ensure image is saved
                time.sleep(1)
                        # Send email
                                            
                # Read temps file and get the highest and lowest temp
                with open("temps/" + str(today_date) + ".txt", "r") as h:
                    minmaxdata = h.readlines()
                    max_temp = max(data, key=lambda x: float(x.split()[1]))
                    min_temp = min(data, key=lambda x: float(x.split()[1]))
                h.close()
                    

                subject = str(today_date) + " Temperature Data"
                message = f'''
                The maximum temperature was: {max_temp} 
                The minimum temperature was: {min_temp} 
                Here is the graph for today's temperature data
                '''
                        
                #Begin message creation
                msg = MIMEMultipart()
                msg['From'] = sender_account
                msg['To'] = receiver_account
                msg['Subject'] = subject
                msg.attach(MIMEText(message))
                part = MIMEBase('application', "octet-stream")
                with open('image/' + str(today_date) + '.png', 'rb') as file:
                    part.set_payload(file.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition',
                                                'attachment; filename="test.png"')
                msg.attach(part)
                        
                # Send the message. 
                try:
                    smtp_server = smtplib.SMTP(server, port)
                    smtp_server.ehlo()
                    smtp_server.starttls()  # tell server we want to communicate with TLS encryption
                    smtp_server.login(sender_account, sender_pwd)
                    smtp_server.sendmail(sender_account, receiver_account, msg.as_string())
                    smtp_server.close()
                    print ("Email sent successfully!")
                except Exception as ex:
                    print ("Something went wrong….",ex)
                        
            
            with open("temps/" + str(today_date) + ".txt", "a") as f: # open file to write to
                data = analog_input.read()
                if data == None:
                    continue
                voltage = (data) * 5.0
                tempC = voltage * 100.0 
                tempC = round(tempC, 3)
                current_time = str(time.strftime("%H:%M"))
                f.write(current_time + ", " + str(tempC) + "\n")
            f.close()
                    # Wait 1 minute before recording again
            time.sleep(60)  
        
    


if __name__ == "__main__":
    main()
