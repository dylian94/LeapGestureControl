import sys
import Leap

from GestureListener import GestureListener

def main():

    listener = GestureListener()

    controller = Leap.Controller()

    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    print "Adding Listener."
    controller.add_listener(listener)

    print "Press Enter to quit..."
    sys.stdin.readline()

    controller.remove_listener(listener)

main()
