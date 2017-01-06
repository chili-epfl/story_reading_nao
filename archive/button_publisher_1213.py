#!/usr/bin/env python

import sys, select, tty, termios
import rospy
from std_msgs.msg import String
from Tkinter import *

def storySelection():
	""" Select a story from the text files of each story and return it

	"""

	story.setLanguage('English')
	storyNum = random.randint(1,5)
	storyNum = 1
	if storyNum == 1: 	
		selectedStory = rospy.get_param("fox_story_en")

	elif storyNum == 2:
		selectedStory = rospy.get_param("elephant_story_en")

	elif storyNum == 3:
		selectedStory = rospy.get_param("goat_story_en")

	elif storyNum == 4:
		selectedStory = rospy.get_param("bear_story_en")

	elif storyNum == 5:
		selectedStory = rospy.get_param("chick_story_en")

	return selectedStory


def createButton():
	# Create the new window
	root = Tk()

	# Modify root window
	root.title("Story")
	root.geometry("915x430")

	app = Frame(root)


	photo1 = PhotoImage(file= r"/home/elmira/Documents/Fox_story_scale1.png")
	photo2 = PhotoImage(file= r"/home/elmira/Documents/Fox_story_scale2.png")
	photo3 = PhotoImage(file= r"/home/elmira/Documents/Fox_story_scale3.png")

	app = Canvas()
	app.pack(side='top', fill='both', expand='yes')
	app.create_image(10, 10, image=photo1, anchor='nw')
	app.create_image(310, 10, image=photo2, anchor='nw')
	app.create_image(605, 10, image=photo3, anchor='nw')

	#app.pack()
	#app.grid()
	#ttk.Style().configure("button1", padding=6, relief="flat")
	button1 = Button(app, text="WRONG", height=3, width=15, activebackground="red", bg="grey", font="bold")
	button1.grid(row=1, column=1)
	button1.pack(side="bottom", expand=False, padx=4, pady=4)

	button1.bind('<Button-1>', clickButton)
	root.mainloop()

def clickButton(event):
	#String = 'g'
	button_pub.publish("g")

def main():
	global button_pub
	#key_pub = rospy.Publisher('buttons', String, queue_size=1)
	rospy.init_node('button_publisher')
	button_pub = rospy.Publisher('buttons', String, queue_size=1)

	createButton()
	rate = rospy.Rate(100)
	#old_attr = termios.tcgetattr(sys.stdin)
	#tty.setcbreak(sys.stdin.fileno())
	'''

	while not rospy.is_shutdown():
		if select.select([sys.stdin], [], [], 0)[0] == [sys.stdin]:
			button_pub.publish(sys.stdin.read(1))
		rate.sleep()
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_attr)'''



if __name__ == '__main__':
	main()