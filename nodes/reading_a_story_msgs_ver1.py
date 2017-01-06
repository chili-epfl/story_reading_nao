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

# debug
import rospy
from std_msgs.msg import String
from memory.msg import Animation

REACTION_TOPIC = rospy.get_param('kids_reaction_topic', 'kids_reaction')
KEY_MAPPING = { 'f': [1], 
				'g': [1], 
				'h': [1] }

def callback(msg):
	if len(msg.data) == 0 or not KEY_MAPPING.has_key(msg.data[0]):
		return
	reac = KEY_MAPPING[msg.data[0]]
	print KEY_MAPPING[msg.data[0]]

	if reac == [1]:
		id = reaction.post.angleInterpolationBezier(animations.embarassed_pose.names, animations.embarassed_pose.times, animations.embarassed_pose.keys)
		time.sleep(2)
		story.post.say("\\rspd=80\\Sorry")
		#reaction.wait(id,0)
		#time.sleep(2)
		#reaction.post.angleInterpolationBezier(animations.scratchHead_pose.names, animations.scratchHead_pose.times, animations.scratchHead_pose.keys)
		#time.sleep(2)
		#story.setParameter("speed", 0.5)
		#story.post.say("\\rspd=70\\I \\pau=50\\ didn't \\pau=50\\ know")
	else:
		return



def say_from_file(story, filename, encoding):
	with codecs.open(filename, encoding=encoding) as fp:
		contents = fp.read()
		# warning: print contents won't work
		to_say = contents.encode("utf-8")
	story.say(to_say)



def main():
	global reaction
	global story
	global audioreaction
	story = ALProxy("ALTextToSpeech", "nao.local", 9559)
	reaction = ALProxy("ALMotion", "nao.local", 9559)
	audioreaction = ALProxy("ALAudioPlayer", "nao.local", 9559)

	rospy.init_node('reading_a_story_msgs_ver1')

	rospy.Subscriber('keys', String, callback)

	story.setLanguage('English')
	reaction.setExternalCollisionProtectionEnabled("All", True)
	# te string will be encoded
	say_from_file(story, 'fox_story_en.txt', 'ascii')
	rospy.spin()
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

	#reaction.post.angleInterpolationBezier(animations.monster_pose.names, animations.monster_pose.times, animations.monster_pose.keys)
	#time.sleep(2)
	#audioreaction.post.playFile("/home/nao/audio/wav/monsterGrowl.wav")
	""" id = reaction.post.angleInterpolationBezier(animations.embarassed_pose.names, animations.embarassed_pose.times, animations.embarassed_pose.keys)
	time.sleep(2)
	story.post.say("\\rspd=80\\Sorry")
	reaction.wait(id,0)
	time.sleep(2)
	reaction.post.angleInterpolationBezier(animations.scratchHead_pose.names, animations.scratchHead_pose.times, animations.scratchHead_pose.keys)
	time.sleep(2)
	#story.setParameter("speed", 0.5)
	story.post.say("\\rspd=70\\I \\pau=50\\ didn't \\pau=50\\ know")

	reaction.angleInterpolationBezier(animations.IdontKnow_pose.names, animations.IdontKnow_pose.times, animations.IdontKnow_pose.keys)
	time.sleep(2)	
	reaction.angleInterpolationBezier(animations.IdontKnow2_pose.names, animations.IdontKnow2_pose.times, animations.IdontKnow2_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.hesitation_pose.names, animations.hesitation_pose.times, animations.hesitation_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.hesitation2_pose.names, animations.hesitation2_pose.times, animations.hesitation2_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.hesitation3_pose.names, animations.hesitation3_pose.times, animations.hesitation3_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.thinking1_pose.names, animations.thinking1_pose.times, animations.thinking1_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.thinking2_pose.names, animations.thinking2_pose.times, animations.thinking2_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.thinking3_pose.names, animations.thinking3_pose.times, animations.thinking3_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.thinking4_pose.names, animations.thinking4_pose.times, animations.thinking4_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.thinking5_pose.names, animations.thinking5_pose.times, animations.thinking5_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.thinking6_pose.names, animations.thinking6_pose.times, animations.thinking6_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.thinking7_pose.names, animations.thinking7_pose.times, animations.thinking7_pose.keys)
	time.sleep(2)
	reaction.angleInterpolationBezier(animations.thinking8_pose.names, animations.thinking8_pose.times, animations.thinking8_pose.keys)

	#reaction.runMotion(animations.IdontKnow_pose, factorSpeed, factorAmpl)

	"""

if __name__ == "__main__":
	main()