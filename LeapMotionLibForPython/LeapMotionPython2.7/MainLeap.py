import sys
sys.path.insert(0, "lib")

import Leap, sys

class LeapEventListener(Leap.Listener):

    def __init__(self):
        super(LeapEventListener, self).__init__()  #Initialize like a normal listener
     
    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")
        controller.enable_gesture(Leap.Gesture.Type.TYPE_SWIPE)
        controller.config.set("Gesture.Swipe.MinLength", 200.0)
        controller.config.save()

    def on_disconnect(self, controller):
        # Note: not dispatched when running in a debugger.
        print("Disconnected")

    def on_frame(self, controller):
        print ("Frame available")
        frame = controller.frame()
        #Process frame data

def main():
    # create a sample listener and controller
    listener = LeapEventListener()
    controller = Leap.Controller()

    # 
    controller.add_listener(listener)

    # keep process running until Enter is pressed
    
    print("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        # Remove the sample listener when done
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()