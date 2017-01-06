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

"""
KEY_MAPPING = { 'f': [1], 
				'g': [1], 
				'h': [1],
				'b': [2],
				'n': [2],
				'm': [2] 
				}

def mistakeDetected(msg):
	""" Determin if the user has detected a mistake in reading the story

	"""
	if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]
	#reactToTheMistake(reac)
	reactionSelection(reac)


def storySelection():
	""" Select a story from the text files of each story and return it

	"""

	story.setLanguage('English')
	#storyNum = random.randint(1,5)
	storyNum = 3
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


def reactionSelection(reac):
	""" Select a reaction from the available reactions ater making mistake

	"""
	reaction.setExternalCollisionProtectionEnabled("All", True)

	reactionNum = random.randint(1,9)
	#reactionNum = 7
	if reactionNum == 1:
		words = "\\rspd=80\\ sorry"
		sleepTime = 3
		reactToTheMistake(reac, animations.embarassed_pose, words, sleepTime)

	if reactionNum == 2:
		words = "\\rspd=80\\ I don't know!!"		
		sleepTime = 1
		reactToTheMistake(reac, animations.scratchHead_pose, words, sleepTime, 1.0)

	if reactionNum == 3:
		words = "\\rspd=80\\ Oh!! really!!?"		
		sleepTime = 1
		reactToTheMistake(reac, animations.IdontKnow2_pose, words, sleepTime, 0.8)

	if reactionNum == 4:
		words = "\\rspd=80\\ Oh!!!"		
		sleepTime = 2
		reactToTheMistake(reac, animations.thinking5_pose, words, sleepTime, 0.9)

	if reactionNum == 5:
		words = "\\rspd=80\\ hmm!!"		
		sleepTime = 1
		reactToTheMistake(reac, animations.thinking6_pose, words, sleepTime, 0.8)

	if reactionNum == 6:
		words = "\\rspd=70\\ let me see!!"		
		sleepTime = 1
		reactToTheMistake(reac, animations.thinking7_pose, words, sleepTime, 0.8)

	if reactionNum == 7:
		words = "\\rspd=70\\ yes \\pau=700\\ you are right."		
		sleepTime = 2
		reactToTheMistake(reac, animations.thinking8_pose, words, sleepTime)


def reactToTheMistake(reac, pose, words, pause, factorSpeed = 1.0):

	if reac == [1]:
		times = changeSpeed(pose.times, factorSpeed)
		id = reaction.post.angleInterpolationBezier(pose.names, times, pose.keys)
		time.sleep(pause)
		story.post.say(words)
		reaction.wait(id,0)
		time.sleep(1)
		story.say("\\rspd=80\\wait!! \\pau=700\\ I'll try again")
		time.sleep(2)
		correctFlag = True
		#readTheTaggedStory(selectedStory, correctFlag)
		readTheTaggedStoryWithLevel(selectedStory, correctFlag)

	else:
		return


def changeSpeed(times, factor):
	for i in xrange(len(times)):
		times[i] = [x / float(factor) for x in times[i]]

	return times


def sayFromFile(story, filename, encoding):
	#with codecs.open(filename, encoding=encoding) as fp:
	#contents = filename.read()
		# warning: print contents won't work
	toSay = filename.encode("utf-8")
	story.say(toSay)

def pauseStoryReading():
	pass

def readTheStoryWithMistake():
	story.setLanguage('English')
	#story_num1 = rospy.get_param("fox_story_en")
	sayFromFile(story, story_num1, 'ascii')
	story.post.say("A red Fox \\pau=500\\ in green socks \\pau=500\\ doing tricks with orange rocks")


def readTheStoryWithoutMistake():
	time.sleep(5)
	story.setLanguage('English')
	#say_from_file(story, 'fox_story_en.txt', 'ascii')
	id = story.post.say("A red Fox \\pau=500\\ in blue socks \\pau=500\\ doing tricks with orange clocks")
	restingEnabled = True
	story.wait(id,0)
	faceTrackingEnded()

def numberOfMistakesSelection(activityLevel):

	if activityLevel == "easy":
		mistakeNum = 1

	if activityLevel == "medium":
		mistakeNum = 3

	if activityLevel == "hard":
		mistakeNum = 5

	return mistakeNum


def readTheTaggedStory(taggedStory, correctFlag):
	""" Read a story containing the tags and based on correctFlag change the tags approprietly

	"""
	
	#taggedStory = rospy.get_param("fox_story_en")
		
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

def readTheTaggedStoryWithLevel(storyContent, correctFlag, mistakeNum):
	"""

	"""

	#tagR = "=RTag"
	#tagW = "=WTag"
	#foundTags = findTheTags(tagR, tagW, storyContent)
	foundTags = tagsArray(storyContent)
	if correctFlag == True:
		for i in range(len(foundTags)):
				# remove the RTag and WTags with words
				storyContent = removeTheTag_ver2("RTag", i, storyContent, foundTags)
				storyContent = removeTheWordWithTag_ver2("WTag", i, storyContent, foundTags)
	elif correctFlag == False:
		for i in range(len(foundTags)):
			if i <= mistakeNum:
				# remove the WTags and the RTags with words
				storyContent = removeTheTag_ver2("WTag", i, storyContent, foundTags)
				storyContent = removeTheWordWithTag_ver2("RTag", i, storyContent, foundTags)
			elif i > mistakeNum:
				# remove the RTags and the WTags with words
				storyContent = removeTheTag_ver2("RTag", i, storyContent, foundTags)
				storyContent = removeTheWordWithTag_ver2("WTag", i, storyContent, foundTags)
	
	sayFromFile(story, storyContent, 'ascii')

def removeTheTagsWithLevel(foundTags, storyContent, mistakeNum):
	"""

	"""

	for i in len(foundTags):
		if i <= mistakeNum:
			removeTheTag_ver2()
		elif i > mistakeNum:
			removeTheWordWithTag_ver2()



def tagsArray(storyContent):
	"""

	"""
	tagR = "=RTag"
	tagW = "=WTag"
	tagR_word = "\w+(?=" + tagR + ")"
	tagW_word = "\w+(?=" + tagW + ")"
	foundTags = []
	while True:
		dummy = []
		dummy.append(re.search(tagR, storyContent))
		dummy.append(re.search(tagW, storyContent))
		dummy.append(re.search(tagR_word + tagR, storyContent))
		dummy.append(re.search(tagW_word + tagW, storyContent))
		test = re.search(tagR, storyContent)
		if test == None:
			break
		storyContent = storyContent[:dummy[0].start(0)] + storyContent[dummy[0].end(0):]
		foundTags.append(dummy)

	random.shuffle(foundTags)

	return foundTags

def findTheTags(tagR, tagW, storyContent):
	"""

	"""

	count = 0
	tagR_word = "\w+(?=" + tagR + ")"
	tagW_word = "\w+(?=" + tagW + ")"
	foundTags = [][tagR, tagW, tagR_word, tagW_word]


	while True:
		foundTags[count][tagR] = re.search(tagR, storyContent)
		foundTags[count][tagW] = re.search(tagW, storyContent)
		foundTags[count][tagR_word] = re.search(tagR_word + tagR, storyContent)
		foundTags[count][tagW_word] = re.search(tagW_word + tagW, storyContent)

		count += 1
		random.shuffle(foundTags)

	return foundTags


def removeTheTag(tag, storyContent):
	""" Find and remove the tag given to the function and leave the word connected to them intact

	"""
	while True:
		foundTag = re.search(tag, storyContent)
		if foundTag == None:
			break
		storyContent = storyContent[:foundTag.start(0)] + storyContent[foundTag.end(0):]

	return storyContent


def removeTheTag_ver2(tag, row, storyContent, foundTag):
	if tag == "RTag":
		col = 0
	elif tag == "WTag":
		col = 1

	storyContent = storyContent[:foundTag[row][col].start(0)] + storyContent[foundTag[row][col].end(0)]
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


def removeTheWordWithTag_ver2(tag, row, storyContent, foundTag):
	"""

	"""
	if tag == "RTag":
		col = 2
	elif tag == "WTag":
		col = 3

	storyContent = storyContent[:foundTag[row][col].start(0)] + storyContent[foundTag[row][col].end(0)]
	return storyContent


def faceTrackingStarted(faceSize):

	# First, wake up
	#reaction.wakeUp()

	# Add target to track
	targetName = "Face"
	faceWidth = faceSize
	tracker.registerTarget(targetName, faceWidth)

	# Then, start tracker
	tracker.track(targetName)

def faceTrackingEnded():

	# Stop tracker
	tracker.stopTracker()
	tracker.unregisterAllTargets()
	reaction.rest()



def main():
	global reaction
	global story
	global audioreaction
	global tracker
	global restingEnabled 
	global selectedStory
	story = ALProxy("ALTextToSpeech", "nao.local", 9559)
	reaction = ALProxy("ALMotion", "nao.local", 9559)
	audioreaction = ALProxy("ALAudioPlayer", "nao.local", 9559)
	tracker = ALProxy("ALTracker", "nao.local", 9559)

	# Face tracking activated
	facesize = 0.1
	restingEnabled = False
	rospy.init_node('story_event')
	faceTrackingStarted(facesize)

	# Select a story
	selectedStory = storySelection()
	correctFlag = False
	mistakeNum = 1
	#readTheTaggedStory(selectedStory, correctFlag)
	readTheTaggedStoryWithLevel(selectedStory, correctFlag, mistakeNum)

	rospy.Subscriber('keys', String, mistakeDetected)

	if restingEnabled == True:
		faceTrackingEnded()
	
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