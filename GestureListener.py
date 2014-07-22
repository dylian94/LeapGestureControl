import os
import ConfigParser
import Leap

from Leap import CircleGesture, SwipeGesture


class GestureListener(Leap.Listener):
    def __init__(self):
        super(GestureListener, self).__init__()

        self.config = ConfigParser.ConfigParser()

        self.gestures_stopped = {
            "circleleft": 0,
            "circleright": 0,
            "keytap": 0,
            "screentap": 0,
            "swipeleft": 0,
            "swiperight": 0,
            "swipeup": 0,
            "swipedown": 0
        }
        self.gestures_started = {
            "circleleft": 0,
            "circleright": 0,
            "keytap": 0,
            "screentap": 0,
            "swipeleft": 0,
            "swiperight": 0,
            "swipeup": 0,
            "swipedown": 0
        }
        self.gestures = [
            "circleleft",
            "circleright",
            "keytap",
            "screentap",
            "swipeleft",
            "swiperight",
            "swipeup",
            "swipedown"
        ]

    def on_init(self, controller):
        self.read_config()

        print "Initialized"

    def read_config(self):
        self.config.read("./gesture_commands.cfg")

        print("Configuration loaded")

        for section in self.config.sections():
            print("\n" + section + ":\n")
            for option in self.config.options(section):
                value = self.config.get(section, option)
                print("  " + option + ": " + value)

    def on_connect(self, controller):
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        # controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):

        frame = controller.frame()

        for gesture in frame.gestures():

            number_of_pointables = len(gesture.pointables)

            if number_of_pointables != 0 and gesture.is_valid and (gesture.state == Leap.Gesture.STATE_START or gesture.state == Leap.Gesture.STATE_STOP):

                gestures = None

                if gesture.state == Leap.Gesture.STATE_START:
                    gestures = self.gestures_started
                elif gesture.state == Leap.Gesture.STATE_STOP:
                    gestures = self.gestures_stopped

                if gesture.type == Leap.Gesture.TYPE_CIRCLE:
                    circle = CircleGesture(gesture)

                    if circle.pointable.direction.angle_to(circle.normal) > Leap.PI / 4:
                        gestures["circleleft"] += number_of_pointables
                    else:
                        gestures["circleright"] += number_of_pointables

                elif gesture.type == Leap.Gesture.TYPE_KEY_TAP:
                    self.gestures_started["keytap"] += number_of_pointables
                    gestures["keytap"] += number_of_pointables

                elif gesture.type == Leap.Gesture.TYPE_SCREEN_TAP:
                    gestures["screentap"] += number_of_pointables

                elif gesture.type == Leap.Gesture.TYPE_SWIPE:

                    swipe = SwipeGesture(gesture)

                    left = 0
                    right = 0
                    up = 0
                    down = 0

                    horizontal_movement = swipe.direction[0]
                    vertical_movement = swipe.direction[1]

                    movement = None

                    if horizontal_movement != abs(horizontal_movement):
                        left = abs(horizontal_movement)
                    elif horizontal_movement != 0:
                        right = horizontal_movement

                    if vertical_movement != abs(vertical_movement):
                        down = abs(vertical_movement)
                    elif vertical_movement != 0:
                        up = vertical_movement

                    if left > right and left > up and left > down:
                        movement = "left"

                    elif right > left and right > up and right > down:
                        movement = "right"

                    elif up > down and up > left and up > right:
                        movement = "up"

                    elif down > up and down > left and down > right:
                        movement = "down"

                    gestures["swipe" + movement] += 1

        for gesture_name in self.gestures:
            if self.gestures_started.get(gesture_name) != 0 and self.gestures_started.get(gesture_name) == self.gestures_stopped.get(gesture_name):

                self.execute(gesture_name, str(self.gestures_started.get(gesture_name)))

                self.gestures_started[gesture_name] = 0
                self.gestures_stopped[gesture_name] = 0

            elif self.gestures_started.get(gesture_name) > 5 or self.gestures_stopped.get(gesture_name) >= 5:

                self.gestures_started[gesture_name] = 0
                self.gestures_stopped[gesture_name] = 0

    def execute(self, command_name, number_of_pointables):

        command = "Not defined in config!"

        if self.config.has_option(command_name, number_of_pointables):

            command = self.config.get(command_name, number_of_pointables)
            os.system(command)

        print("")
        print("Gesture: " + command_name)
        print("Pointables: " + number_of_pointables)
        print("Command: " + command)