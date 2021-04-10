import sys, os, time, math
sys.path.insert(0, os.path.abspath("C:/leaplib"))
import Leap

controller = Leap.Controller()
while(True):
    frame = controller.frame()
    hands = frame.hands
    if(hands[0].is_valid):
        print((hands[0].palm_position[1]-200)/100)
    time.sleep(1)
