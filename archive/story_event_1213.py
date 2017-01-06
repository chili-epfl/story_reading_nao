#!/usr/bin/env python
# -*- encoding: UTF-8 -*-



import animations.embarassed_pose
import animations.scratchHead_pose
import animations.IdontKnow_pose
import animations.IdontKnow2_pose
import animations.hesitation_pose
import animations.hesitation2_pose
import animations.hesitation3_pose
import animations.thinking1_pose
import animations.thinking2_pose
import animations.thinking3_pose
import animations.thinking4_pose
import animations.thinking5_pose
import animations.thinking6_pose
import animations.thinking7_pose
import animations.thinking8_pose
import animations.monster_pose

from naoqi import ALProxy
import codecs
import time
import re
import random

# debug
import rospy
from std_msgs.msg import String
from memory.msg import Animation

reaction_states = { "low": [1, 2, 3, 4, 5],
				  	"medium": [6, 7, 8, 9, 10],
				  	"high": [11, 12, 13, 14, 15] }


mistake_level_states = { "low": [1],
						 "medium": [3],
						 "high": [5]}

story_selection_state = {}

""" Recieve the key stroke from key publisher node
	[1]: tell the robot made a mistake in reading the story
	[2]: tell the robot to choose a new story and repeat the process
	[3]: tell the robot to stop the tracker and go to resting mode

"""
KEY_MAPPING = { 'f': [1], 
				'g': [1], 
				'h': [1],
				'b': [2],
				'n': [2],
				'm': [2],
				'e': [3],
				'r': [3],
				't': [3]  
				}


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


def numberOfMistakesSelection(activityLevel):
	""" based on the activity level it decides how many mistakes robot is supposed to make 

	"""

	if activityLevel == "easy":
		mistakeNum = 1

	elif activityLevel == "medium":
		mistakeNum = 3

	elif activityLevel == "hard":
		mistakeNum = 5

	return mistakeNum



def readTheTaggedStory(taggedStory, correctFlag):
	""" Read a story containing the tags and based on correctFlag change the tags approprietly

	"""
			
	if correctFlag == True:

		tag = "=RTag"
		taggedStory = removeTheTag(tag, taggedStory)
		tag = "=WTag"
		taggedStory = removeTheWordWithTag(tag, taggedStory)

	elif correctFlag == False:
		tag = "=WTag"
		taggedStory = removeTheTag(tag, taggedStory)
		tag = "=RTag"
		taggedStory = removeTheWordWithTag(tag, taggedStory)
	
	sayFromFile(story, taggedStory, 'ascii')


def readTheTaggedStoryWithLevel(storyContent, correctFlag, mistakeNum = 0):
	""" Read a story containing the tags and based on correctFlag change the tags approprietly
	number of mistakes decides how many of the wrong tags should be removed

	"""

	if correctFlag == True:
		storyContent = removeTheTag("=RTag", storyContent)
		storyContent = removeTheWordWithTag("=WTag", storyContent)

	elif correctFlag == False:
		
		for i in range(mistakeNum):
			c_w, c_r = 0, 0
			availNum = len(re.findall("=WTag", storyContent))
			ranNum = random.randint(0, availNum - 1 - c_w)
			
			for m_w in re.finditer(r"=WTag", storyContent):				
				if c_w == ranNum:
					storyContent = storyContent[:m_w.start(0)] + storyContent[m_w.end(0):]
					break
				c_w += 1
			
			for m_r in re.finditer("\w+(?=" + "=RTag" + ")" +"=RTag", storyContent):
				if c_r == c_w:
					storyContent = storyContent[:m_r.start(0)] + storyContent[m_r.end(0):]
					break
				c_r += 1

		storyContent = removeTheTag("=RTag", storyContent)
		storyContent = removeTheWordWithTag("=WTag", storyContent)

	sayFromFile(story, storyContent, 'ascii')


def sayFromFile(story, filename, encoding):
	"""

	"""
	#with codecs.open(filename, encoding=encoding) as fp:
	#contents = filename.read()
		# warning: print contents won't work
	toSay = filename.encode("utf-8")
	story.say(toSay)


def removeTheTag(tag, storyContent):
	""" Find and remove the tag given to the function and leave the word connected to them intact

	"""
	while True:
		foundTag = re.search(tag, storyContent)
		if foundTag == None:
			break
		storyContent = storyContent[:foundTag.start(0)] + storyContent[foundTag.end(0):]

	return storyContent


def removeTheWordWithTag(tag, storyContent):
	""" Find and remove the tag given to the function and remove the tag and the word connected to it as well

	"""
	while True:
		tagWithWord = "\w+(?=" + tag + ")"
		foundTag = re.search(tagWithWord + tag, storyContent)
		if foundTag == None:
			break
		storyContent = storyContent[:foundTag.start(0)] + storyContent[foundTag.end(0):]

	return storyContent


def mistakeDetected(msg):
	""" Determin if the user has detected a mistake in reading the story
		with checking if certain keys have been pressed

	"""
	
	if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]
	#reactToTheMistake(reac)
	reactionSelection(reac)


def reactionSelection(reac):
	""" Select a reaction from the available reactions ater making mistake

	"""
	
	reaction.setExternalCollisionProtectionEnabled("All", True)
	reactionNum = random.randint(1,9)
	reactionNum = 7

	if reactionNum == 1:
		wordsBefore = "\\rspd=80\\ sorry"
		sleepTime = 3
		wordsAfter = "\\rspd=80\\wait!! \\pau=700\\ I'll try again"
		reactToTheMistake(reac, animations.embarassed_pose, wordsBefore, wordsAfter, sleepTime)

	if reactionNum == 2:
		wordsBefore = "\\rspd=60\\ hmm!! \\pau=300\\ \\rspd=80\\ I didn't know!!"		
		sleepTime = 2
		wordsAfter = "\\rspd=80\\ let me try again"
		reactToTheMistake(reac, animations.scratchHead_pose, wordsBefore, wordsAfter, sleepTime, 1.0)

	if reactionNum == 3:
		wordsBefore = "\\rspd=80\\ Oh!! really!!?"		
		sleepTime = 1
		wordsAfter = "\\rspd=80\\ then, I'll read it again"
		reactToTheMistake(reac, animations.IdontKnow2_pose, wordsBefore, wordsAfter, sleepTime, 0.8)

	if reactionNum == 4:
		wordsBefore = "\\rspd=80\\ Oh!!!"		
		sleepTime = 2
		wordsAfter = "\\rspd=80\\ wait!!! I'll try again"
		reactToTheMistake(reac, animations.thinking5_pose, wordsBefore, wordsAfter, sleepTime, 0.9)

	if reactionNum == 5:
		wordsBefore = "\\rspd=80\\ hmm!!"		
		sleepTime = 1
		wordsAfter = "\\rspd=80\\ I need to read it again"
		reactToTheMistake(reac, animations.thinking6_pose, wordsBefore, wordsAfter, sleepTime, 0.8)

	if reactionNum == 6:
		wordsBefore = "\\rspd=70\\ let me see!!"		
		sleepTime = 2
		wordsAfter = "\\rspd=70\\ you are right!! \\rspd=90\\ \\pau=200\\ let me read it again"
		reactToTheMistake(reac, animations.thinking7_pose, wordsBefore, wordsAfter, sleepTime, 0.8)

	if reactionNum == 7:
		wordsBefore = "\\rspd=70\\ yeaah!!! \\pau=700\\ you are right."		
		sleepTime = 2
		wordsAfter = "\\rspd=80\\ I'll try again"
		reactToTheMistake(reac, animations.thinking8_pose, wordsBefore, wordsAfter, sleepTime)


def reactToTheMistake(reac, pose, wordsBefore, wordsAfter, pause, factorSpeed = 1.0):
	""" If the keys pressed are due to detection of mistake, the robot reacts.
		The reaction is a physical movement and certain words which shows robot's remorse

	"""

	if reac == [1]:
		times = changeSpeed(pose.times, factorSpeed)
		id = reaction.post.angleInterpolationBezier(pose.names, times, pose.keys)
		time.sleep(pause)
		story.post.say(wordsBefore)
		reaction.wait(id,0)
		time.sleep(1)
		story.say(wordsAfter)
		time.sleep(2)
		correctFlag = True
		#readTheTaggedStory(selectedStory, correctFlag)
		readTheTaggedStoryWithLevel(selectedStory, correctFlag)

	else:
		return


def changeSpeed(times, factor):
	""" It changes the speed of predefined times for each pose movement

	"""

	for i in xrange(len(times)):
		times[i] = [x / float(factor) for x in times[i]]

	return times


def pauseStoryReading():
	pass


def readTheStoryWithMistake():
	""" Simple test of robot reading a string containing mistakes

	"""

	story.setLanguage('English')
	#story_num1 = rospy.get_param("fox_story_en")
	sayFromFile(story, story_num1, 'ascii')
	story.post.say("A red Fox \\pau=500\\ in green socks \\pau=500\\ doing tricks with orange rocks")


def readTheStoryWithoutMistake():
	""" Simple test of robot reading a string with correct story

	"""

	time.sleep(5)
	story.setLanguage('English')
	#say_from_file(story, 'fox_story_en.txt', 'ascii')
	id = story.post.say("A red Fox \\pau=500\\ in blue socks \\pau=500\\ doing tricks with orange clocks")
	restingEnabled = True
	story.wait(id,0)
	faceTrackingEnded()


def faceTrackingStarted(faceSize):
	""" Robot starts to track the users face

	"""

	# First, wake up
	reaction.wakeUp()

	# Add target to track
	targetName = "Face"
	faceWidth = faceSize
	tracker.registerTarget(targetName, faceWidth)

	# Then, start tracker
	tracker.track(targetName)


def faceTrackingEnded(msg):
	""" Robot stops to track the users face and go into resting mode after certain keys are pressed

	"""
	if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]

	# Stop tracker
	if reac == [3]:
		tracker.stopTracker()
		tracker.unregisterAllTargets()
		reaction.rest()

def repeatTheStoryReading(msg):
	"""

	"""
	if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]

	if reac ==[2]:
		# Select a story and activity level
		selectedStory = storySelection()
		correctFlag = False
		activityLevel = rospy.get_param('actlevel', 'medium')
		mistakeNum = numberOfMistakesSelection(activityLevel)

		#readTheTaggedStory(selectedStory, correctFlag)
		readTheTaggedStoryWithLevel(selectedStory, correctFlag, mistakeNum)


def main():
	
	global story
	story = ALProxy("ALTextToSpeech", "nao.local", 9559)
	
	global reaction
	reaction = ALProxy("ALMotion", "nao.local", 9559)
	
	global audioreaction
	audioreaction = ALProxy("ALAudioPlayer", "nao.local", 9559)
	
	global tracker
	tracker = ALProxy("ALTracker", "nao.local", 9559)

	# Initialize the node
	rospy.init_node('story_event')

	# Face tracking activated
	facesize = 0.1
	global restingEnabled 
	restingEnabled = False
	faceTrackingStarted(facesize)

	# Select a story and activity level
	global selectedStory
	selectedStory = storySelection()
	correctFlag = False
	activityLevel = rospy.get_param('actlevel', 'medium')
	mistakeNum = numberOfMistakesSelection(activityLevel)

	#readTheTaggedStory(selectedStory, correctFlag)
	readTheTaggedStoryWithLevel(selectedStory, correctFlag, mistakeNum)

	rospy.Subscriber('keys', String, mistakeDetected)

	rospy.Subscriber('keys', String, faceTrackingEnded)

	rospy.Subscriber('keys', String, repeatTheStoryReading)
	
	try:
		while True:
			time.sleep(1)
    	except restingEnabled == True:
        	print
        	print "Interrupted by user, shutting down"
        	myBroker.shutdown()
        	sys.exit(0)



if __name__ == "__main__":


	main()