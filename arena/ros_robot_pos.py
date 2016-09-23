#!/usr/bin/python
from utils import SeekRobots
import cv2
import rospy
from std_msgs.msg import Int16MultiArray


def talker(seeker):
    pub = rospy.Publisher('robot_pos', Int16MultiArray, queue_size=1)
    rospy.init_node('vision', anonymous=True)
    rate = rospy.Rate(1) # 10hz
#    while not rospy.is_shutdown():
    pos = Int16MultiArray()
    pos.data = seeker.data()
    pub.publish(pos)
        #rate.sleep()


if __name__ == '__main__':

    a = SeekRobots()


    cv2.namedWindow('main')

    #cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture('output.avi')



    while(cap.isOpened()):
        ret,frame = cap.read()
        a.set_frame(frame)
        a.ball()
        a.home_team()
        try:
            talker(a)
        except rospy.ROSInterruptException:
            pass

        cv2.imshow('main',a.frame)
       # key = cv2.waitKey(1) & 0xFF
       # if key == ord('q'):
       #     break

