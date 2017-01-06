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
import argparse

# debug
import rospy
from std_msgs.msg import String
from memory.msg import Animation

REACTION_TOPIC = rospy.get_param('kids_reaction_topic', 'kids_reaction')
KEY_MAPPING = { 'f': [1], 
				'g': [1], 
				'h': [1] }

def mistakeDetected(msg):
	if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]
	reactToTheMistake(reac)



def say_from_file(story, filename, encoding):
	#with codecs.open(filename, encoding=encoding) as fp:
	#contents = filename.read()
		# warning: print contents won't work
	to_say = filename.encode("utf-8")
	story.say(to_say)

def pauseStoryReading():
	pass

def readTheStoryWithMistake():
	story.setLanguage('English')
	story_num1 = rospy.get_param("fox_story_en")
	say_from_file(story, story_num1, 'ascii')
	story.post.say("A red Fox \\pau=500\\ in green socks \\pau=500\\ doing tricks with orange rocks")


def readTheStoryWithoutMistake():
	time.sleep(5)
	story.setLanguage('English')
	#say_from_file(story, 'fox_story_en.txt', 'ascii')
	id = story.post.say("A red Fox \\pau=500\\ in blue socks \\pau=500\\ doing tricks with orange clocks")
	restingEnabled = True
	story.wait(id,0)
	faceTrackingEnded()


def reactToTheMistake(reac):
	reaction.setExternalCollisionProtectionEnabled("All", True)
	if reac == [1]:
		id = reaction.post.angleInterpolationBezier(animations.embarassed_pose.names, animations.embarassed_pose.times, animations.embarassed_pose.keys)
		time.sleep(3)
		story.post.say("\\rspd=80\\Sorry")
		reaction.wait(id,0)
		story.say("\\rspd=80\\wait!! \\pau=700\\ I'll try again")
		readTheStoryWithoutMistake()
		
		#time.sleep(2)
		#reaction.post.angleInterpolationBezier(animations.scratchHead_pose.names, animations.scratchHead_pose.times, animations.scratchHead_pose.keys)
		#time.sleep(2)
		#story.setParameter("speed", 0.5)
		#story.post.say("\\rspd=70\\I \\pau=50\\ didn't \\pau=50\\ know")
	else:
		return

def faceTrackingStarted(faceSize):

	# First, wake up
	reaction.wakeUp()

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

	story = ALProxy("ALTextToSpeech", "nao.local", 9559)
	reaction = ALProxy("ALMotion", "nao.local", 9559)
	audioreaction = ALProxy("ALAudioPlayer", "nao.local", 9559)
	tracker = ALProxy("ALTracker", "nao.local", 9559)
	"""
	parser = argparse.ArgumentParser()
	parser.add_argument("--facesize", type=float, default=0.1,
						help="Face width.")
	args = parser.parse_args()
	"""
	facesize = 0.1
	restingEnabled = False
	rospy.init_node('story_event')
	faceTrackingStarted(facesize)
	readTheStoryWithMistake()

	rospy.Subscriber('keys', String, mistakeDetected)

	if restingEnabled == True:
		faceTrackingEnded()
	

	#story.setLanguage('English')
	#reaction.setExternalCollisionProtectionEnabled("All", True)
	# te string will be encoded
	#say_from_file(story, 'fox_story_en.txt', 'ascii')
	#rospy.spin()
	#factorSpeed = 1.0
	#factorAmpl = 1.0
	try:
		while True:
			time.sleep(1)
    	except KeyboardInterrupt:
        	print
        	print "Interrupted by user, shutting down"
        	myBroker.shutdown()
        	sys.exit(0)



if __name__ == "__main__":


	main()