#!/usr/bin/python
from arena.utils import SeekRobots
import cv2
import rospy
from std_msgs.msg import Int16MultiArray


def talker(seeker):
    rospy.init_node('vision', anonymous=True)
    rate = rospy.Rate(1) # 10hz
#    while not rospy.is_shutdown():
        #rate.sleep()


if __name__ == '__main__':

    a = SeekRobots()

    rospy.init_node('vs', anonymous=True)

    cv2.namedWindow('main')

    #cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture('output.avi')

    pub1 = rospy.Publisher('robot_position1', Int16MultiArray, queue_size=1)
    pub2 = rospy.Publisher('robot_position2', Int16MultiArray, queue_size=1)
    pub3 = rospy.Publisher('robot_position3', Int16MultiArray, queue_size=1)
    pubball = rospy.Publisher('ball_position', Int16MultiArray, queue_size=1)

    pos1    = Int16MultiArray()
    pos2    = Int16MultiArray()
    pos3    = Int16MultiArray()
    posball = Int16MultiArray()
    while(cap.isOpened()):

        ret,frame = cap.read()
        a.set_frame(frame)
        a.ball()
        a.home_team()
        cv2.imshow('main',a.frame)
        try:
            pos1.data = a.robo_pos(1)
            pub1.publish(pos1)

            pos2.data = a.robo_pos(2)
            pub2.publish(pos2)
            
            pos3.data = a.robo_pos(3)
            pub3.publish(pos3)

            posball.data = a.ball_pos()
            pubball.publish(posball)

        except rospy.ROSInterruptException:
            pass


