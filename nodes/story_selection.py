#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import random

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

def randomStory():
	storyNum = random.randint(1,5)
	pub = rospy.Publisher('story_number', String, queue_size=1)
	rospy.init_node('story_selection')
	#rate =rospy.Rate(10)
	while not rospy.is_shutdown():
		pub.publish(str(storyNum))
		#rate.sleep()

if __name__ == '__main__':
	try:
		randomStory()
	except rospy.ROSInterruptException:
		pass