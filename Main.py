import sys
import pyautogui as pt
import pyperclip as pc
from pynput.mouse import Controller, Button
from time import sleep
import requests
import json

# create cursor
mouse = Controller()

class Whats():
    def __init__(self,speed=.5,click_speed=.3):
        self.speed = speed
        self.click_speed = click_speed
        self.name = "Gm"

    # search the name and click on it
    def nav_to_contact(self,name,exit=None):
        try:
            # return x,y axis of given element on the screen
            search_position = pt.locateOnScreen("search.png", confidence=.7)
            # move to the position of the element , at 0 index 'x' reside and at 1 'y' reside
            pt.moveTo(search_position[0:2], duration=self.speed)
            # will move to the left from current location
            # first arg for moving cursor left right and second arg for up down
            pt.moveRel(100,0, duration=self.speed)
            pt.doubleClick(interval=self.click_speed)
            pt.typewrite(name)
            sleep(1)
            pt.moveRel(0,125, duration=self.speed)
            pt.doubleClick()
            if exit:
                t = pt.locateOnScreen("exit_search.png",confidence=.7)
                pt.moveTo(t,duration=self.speed)
                pt.leftClick(interval=self.click_speed)
        except Exception as e:
            print("Error nav_to_contact ",e)

    # locate the message input field
    def locate_input(self):
        try:
            # locate input field
            input_position = pt.locateOnScreen("doc_img.png", confidence=.7)
            pt.moveTo(input_position, duration=self.speed)
            pt.moveRel(100,0,duration=self.speed)
        except Exception as e:
            print(" Error in locate_input ", e)
    
    def check_msg(self):
        green_circle_exist = pt.locateOnScreen("green_circle.png",confidence=.7)
        if green_circle_exist:
            if self.check_name(green_circle_exist):
                return True
            else:
                return False
        else:
            return False

    def check_name(self,green_circle):
        # check green_circle
        pt.moveTo(green_circle[0:2], duration=self.speed)
        pt.moveRel(-100,0, duration=self.speed)
        pt.leftClick()
        # goto profile icon
        pt.moveTo(pt.locateOnScreen("profile.png",confidence=.7),duration=self.speed)
        pt.moveRel(-300,0,duration=self.speed)
        pt.doubleClick()
        sleep(1)
        # copy name of profile
        pt.moveTo(pt.locateOnScreen("about.png",confidence=.7),duration=self.speed)
        pt.moveRel(140,-100,duration=self.speed)
        pt.tripleClick()
        pt.rightClick()
        pt.leftClick(pt.moveRel(0,20,duration=self.speed))
        profile_name = pc.paste()
        if profile_name == self.name:
            pt.moveTo(pt.locateOnScreen("exit_profile.png",confidence=.7))
            pt.leftClick(pt.moveRel(-10,0,duration=self.speed))
            return True
        else:
            return False

    # read the most recent message 
    def read_inbox(self):
        try:
            temp_pos = pt.locateOnScreen("doc_img.png",confidence=.7)
            pt.moveTo(temp_pos, duration=self.speed)
            # locate recent message
            pt.moveRel(16,-73, duration=self.speed)
            pt.tripleClick(interval=self.click_speed)
            # copy it
            pt.rightClick()
            pt.moveRel(10,-252,duration=self.speed)
            pt.rightClick()
            self.analyze_msg()
        except Exception as e:
            print(" Error read_inbox ",e)
    
    # press the send button
    def send(self):
        # send button
        button = pt.locateOnScreen("send.png", confidence=.75)
        pt.moveTo(button, duration=self.speed)
        pt.leftClick(interval=self.click_speed)

    def default_message(self):
        self.locate_input()
        pt.typewrite("Hi I'm Jarvis! I'm assistent of Mr.Ehsan \nHe Created me to serve the humanity! \nDo you want to read an inspirational quote? YES or NO\n")
        self.send()

    def analyze_msg(self):
        msg = pc.paste()
        if "yes" in msg.lower():
            self.locate_input()
            pt.typewrite("Just Give Me a Sec\n")
            self.send()
            sleep(3)
            quote = self.fetch_quote()
            pt.typewrite(f"{quote}\n")
            self.send()
        else:
            self.locate_input()
            pt.typewrite("Good Bye! Have a nice day Sir\n")
            self.send()

    def fetch_quote(self,cat=None):
        if not cat: 
            response = requests.get("https://api.quotable.io/random")
            data_dict = json.loads(response.text)
            return data_dict.get("content")


robo = Whats()
sleep(3)
robo.nav_to_contact("Gm")
robo.default_message()
sleep(1)
robo.nav_to_contact("Ehsan2",exit=True)
while True:
    if robo.check_msg():
        print("FOund")
        break
    else:
        #print("Not found")
        sleep(1)
        continue
robo.read_inbox()
print("Finished")
