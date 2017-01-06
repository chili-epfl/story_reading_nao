#!/usr/bin/env python

import sys, select, tty, termios
import rospy
from std_msgs.msg import String
from Tkinter import *

def storySelection(msg):
	""" Select a story from the text files of each story and return it

	"""

	if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]

	#story.setLanguage('English')
	#storyNum = random.randint(1,5)
	#storyNum = 1
	if msg.data == str(1): 
		storyString = "fox_story"

	elif storyNum == str(2):
		storyString = "elephant_story"

	elif storyNum == str(3):
		storyString = "goat_story"

	elif storyNum == str(4):
		storyString = "bear_story"

	elif storyNum == str(5):
		storyString = "chick_story"

	#storyAddress = "/home/elmira/Documents/photos/" + storyString + "_scale1.png"
	createButton(storyString)

def storySelection2(storyNum):
	""" Select a story from the text files of each story and return it

	"""

	"""if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]"""

	#story.setLanguage('English')
	#storyNum = random.randint(1,5)
	#storyNum = 1
	if storyNum == str(1): 
		storyString = "fox_story"

	elif storyNum == str(2):
		storyString = "elephant_story"

	elif storyNum == str(3):
		storyString = "goat_story"

	elif storyNum == str(4):
		storyString = "bear_story"

	elif storyNum == str(5):
		storyString = "chick_story"

	#storyAddress = "/home/elmira/Documents/photos/" + storyString + "_scale1.png"
	#createButton(storyString)

def createButton():
	# Create the new window
	root = Tk()

	# Modify root window
	root.title("Story")
	root.geometry("915x450")

	app = Frame(root)
	storyString ='fox_story'

	storyAddress1 = "/home/elmira/Documents/photos/" + str(storyString) + "_scale1.png"
	storyAddress2 = "/home/elmira/Documents/photos/" + str(storyString) + "_scale2.png"
	storyAddress3 = "/home/elmira/Documents/photos/" + str(storyString) + "_scale3.png"

	photo1 = PhotoImage(file= storyAddress1)
	photo2 = PhotoImage(file= storyAddress2)
	photo3 = PhotoImage(file= storyAddress3)

	app = Canvas()
	app.pack(side='top', fill='both', expand='yes')
	app.create_image(10, 10, image=photo1, anchor='nw')
	app.create_image(310, 10, image=photo2, anchor='nw')
	app.create_image(605, 10, image=photo3, anchor='nw')

	#app.pack()
	#app.grid()
	#ttk.Style().configure("button1", padding=6, relief="flat")
	button2 = Button(app, text="WRONG", height=3, width=15, activebackground="red", bg="grey", font="bold")
	#button1.grid(row=3, column=2)
	button2.pack(side="bottom", expand=False, padx=4, pady=4)

	button1 = Button(app, text="Start", height=2, width=10, activebackground="green", bg="grey", font="bold")
	#button2.grid(row=3, column=1)
	button1.pack(side="bottom", expand=False, padx=4, pady=4)

	#button3 = Button(app, text="Exit", height=3, width=15, activebackground="yellow", bg="grey", font="bold")
	#button3.grid(row=3, column=3)
	#button3.pack(side="bottom", expand=False, padx=4, pady=4)

	button1.bind('<Button-1>', clickButtonStart)
	button2.bind('<Button-1>', clickButtonWrong)

	root.mainloop()

def clickButtonWrong(event):
	#String = 'g'
	button_pub_wrong.publish("g")

def clickButtonStart(event):
	#String = 'g'
	button_pub_start.publish("s")

def main():
	global button_pub_start
	global button_pub_wrong

	#key_pub = rospy.Publisher('buttons', String, queue_size=1)
	rospy.init_node('button_publisher')

	#storySelection2(str(5))
	
	#rospy.Subscriber('story_number', String, storySelection)

	button_pub_start = rospy.Publisher('button_start', String, queue_size=1)
	button_pub_wrong = rospy.Publisher('button_wrong', String, queue_size=1)

	createButton()


	#createButton()
	#rospy.spin()
	rate = rospy.Rate(100)
	old_attr = termios.tcgetattr(sys.stdin)
	tty.setcbreak(sys.stdin.fileno())
	

	while not rospy.is_shutdown():
		if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
			button_pub_start.publish(sys.stdin.read(1))
		rate.sleep()
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)



if __name__ == '__main__':
	main()