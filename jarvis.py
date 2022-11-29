import pyautogui as pt
import sys
import pyperclip as pc
from pynput.mouse import Controller, Button
from time import sleep
import psutil
import webbrowser
import os
from playwright_stealth import stealth_sync
import schedule

class WhatsUp():
	def __init__(self):
		self.speed = .7
		self.click_speed = .3

	def check_browser(self):
		browser = "firefox" in (i.name() for i in psutil.process_iter())
		if not browser:
			webbrowser.open("https://web.whatsapp.com/",new=0)
			sleep(5)

	def nav_contact(self, contact):
		sleep(5)
		# focus the firefox
		os.system('wmctrl -a firefox')
		sleep(5)
		search_position = pt.locateOnScreen("search_symbol.png", confidence=.7)
		pt.moveTo(search_position[0:2], duration=self.speed)
		pt.moveRel(-100, 10, duration=self.speed)
		pt.click(interval=self.click_speed)
		pt.doubleClick(interval=self.click_speed)
		pt.typewrite(contact)
		sleep(5)
		pt.click(pt.moveTo(pt.locateOnScreen("zong.png", confidence=.7)))
		# find inbox and write
		pt.moveTo(pt.locateOnScreen("doc.png", confidence=.7))
		pt.moveRel(100, 0, duration=self.speed)
		pt.click(interval=self.click_speed)
		pt.doubleClick(interval=self.click_speed)
		pt.typewrite(contact)
		sleep(5)
		# send
		pt.moveTo(pt.locateOnScreen("send.png", confidence=.7))
		pt.click()
	
	def main(self):
		self.check_browser()
		schedule.every().day.at("07:47").do(self.nav_contact("MyZong"))
		while True:
			schedule.run_pending()
			print("wait")
			sleep(1)

w = WhatsUp()
w.main()